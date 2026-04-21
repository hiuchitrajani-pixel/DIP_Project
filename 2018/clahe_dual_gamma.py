import numpy as np
import cv2


def compute_adaptive_clip_point(block, R=255, P=1.5, alpha=100, c=1e-6):  # Step 3a: Content-Adaptive Clip Point
    M   = block.size
    N   = int(block.max()) - int(block.min()) + 1
    if N == 0:
        N = 1
    avg = np.mean(block) + c                                           # Eq.(8): mean of block
    std = np.std(block)                                                # Eq.(8): std dev (textureness)
    lmax = int(block.max())
    clip = (M / N) * (1 + P * (lmax / R) + alpha * (std / avg))       # Eq.(8): adaptive clip point
    return max(1, int(clip))


def redistribute_histogram(hist, clip_point):                          # clip and redistribute histogram
    excess = 0
    clipped = np.copy(hist)
    for i in range(len(clipped)):
        if clipped[i] > clip_point:
            excess += clipped[i] - clip_point
            clipped[i] = clip_point
    redistribution = excess // 256
    clipped += redistribution                                          # spread excess evenly
    return clipped


def compute_cdf_mapping(hist, lmax_prime):                             # Eq.(4), Eq.(5): CDF remapping
    cdf = np.cumsum(hist).astype(np.float64)
    cdf /= cdf[-1] + 1e-6                                             # normalize CDF
    T = cdf * lmax_prime                                               # Eq.(5): mapping function
    return np.clip(T, 0, 255).astype(np.uint8)


def compute_gamma1(L, L_max, L_ref_cdf=0.75):                         # Eq.(10), Eq.(11), Eq.(12): First Gamma
    cdf_vals = np.cumsum(np.bincount(L.flatten(), minlength=256)).astype(np.float64)
    cdf_vals /= cdf_vals[-1]
    L_star_idx = np.searchsorted(cdf_vals, L_ref_cdf)                 # Eq.(10): L* at CDF=0.75
    L_star = max(L_star_idx, 1)
    W_en = (L_max / L_star) ** (1 - 0.5)                              # Eq.(10): enhancement weight
    lmax_prime = int(np.clip(np.mean(L) * W_en, 1, 255))             # Eq.(11)
    return lmax_prime


def compute_gamma2_map(lmax=255):                                      # Eq.(13), Eq.(17), Eq.(18): Second Gamma
    l = np.arange(256, dtype=np.float64)
    e = np.e
    cdf_uniform = l / 255.0
    pdf_w = 1.0 - cdf_uniform
    pdf_w = (pdf_w - pdf_w.min()) / (pdf_w.max() - pdf_w.min() + 1e-6)
    cdf_w = np.cumsum(pdf_w); cdf_w /= cdf_w[-1]
    gamma1 = np.log(e + cdf_uniform)    / 8.0                         # Eq.(17): gamma1 increasing function
    gamma2 = 1.0 + cdf_w / 2.0                                        # Eq.(18): gamma2 increasing function
    T_g2 = lmax * np.power(l / (lmax + 1e-6), gamma2)                 # Eq.(13): second gamma map
    return np.clip(T_g2, 0, 255).astype(np.uint8)


def process_block(block, R=255, P=1.5, alpha=100, D_threshold=50):    # Full per-block pipeline
    hist = np.bincount(block.flatten(), minlength=256)

    clip_point  = compute_adaptive_clip_point(block, R, P, alpha)     # Eq.(8)
    hist_clipped = redistribute_histogram(hist, clip_point)

    L_max      = 255
    lmax_prime = compute_gamma1(block, L_max)                         # Eq.(10)-(12)
    T1         = compute_cdf_mapping(hist_clipped, lmax_prime)        # Eq.(4), (5)
    T1_applied = T1[block]                                            # apply first gamma mapping

    # Apply second gamma correction if block has large dynamic range
    dyn_range  = int(block.max()) - int(block.min())
    if dyn_range > D_threshold:                                        # Eq.(13): check threshold
        T2     = compute_gamma2_map(lmax=255)
        result = np.maximum(T1_applied, T2[block])                    # take max of T1 and T2
    else:
        result = T1_applied

    return result


def apply_bilinear_interpolation(blocks_out, h, w, bh, bw):           # Eq.(6), Eq.(7): bilinear interpolation
    out = np.zeros((h, w), dtype=np.float64)
    nb_h = (h + bh - 1) // bh
    nb_w = (w + bw - 1) // bw

    for i in range(nb_h):
        for j in range(nb_w):
            y0, y1 = i * bh, min((i + 1) * bh, h)
            x0, x1 = j * bw, min((j + 1) * bw, w)
            out[y0:y1, x0:x1] = blocks_out[i][j][:y1-y0, :x1-x0]

    return np.clip(out, 0, 255).astype(np.uint8)


def clahe_dual_gamma_enhance(image_bgr, block_size=32):               # Full pipeline
    ycrcb     = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
    Y, Cr, Cb = cv2.split(ycrcb)

    h, w      = Y.shape
    bh, bw    = block_size, block_size
    nb_h      = (h + bh - 1) // bh
    nb_w      = (w + bw - 1) // bw

    print(f"  Processing {nb_h}x{nb_w} blocks of size {block_size}x{block_size}...")

    blocks_out = []
    for i in range(nb_h):
        row_blocks = []
        for j in range(nb_w):
            y0, y1 = i * bh, min((i + 1) * bh, h)
            x0, x1 = j * bw, min((j + 1) * bw, w)
            block   = Y[y0:y1, x0:x1].copy()
            enhanced_block = process_block(block)                      # per-block dual gamma CLAHE
            row_blocks.append(enhanced_block)
        blocks_out.append(row_blocks)

    Y_enhanced = apply_bilinear_interpolation(blocks_out, h, w, bh, bw)  # Eq.(6), (7)

    enhanced_ycrcb = cv2.merge([Y_enhanced, Cr, Cb])                  # keep original colors
    return cv2.cvtColor(enhanced_ycrcb, cv2.COLOR_YCrCb2BGR)