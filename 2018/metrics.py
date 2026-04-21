import numpy as np
import cv2


def compute_tv(image):                                                 # NR Metric: Total Variation (Eq.19)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float64)
    diff_x = np.abs(gray[:, 1:] - gray[:, :-1])                      # horizontal differences
    diff_y = np.abs(gray[1:, :] - gray[:-1, :])                      # vertical differences
    return (diff_x.sum() + diff_y.sum()) / ((gray.shape[0]-1) * (gray.shape[1]-1))  # lower = less noise


def compute_ambe(original, enhanced):                                  # FR Metric: AMBE (Eq.20)
    o = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY).astype(np.float64)
    e = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY).astype(np.float64)
    return abs(np.mean(o) - np.mean(e)) / 255.0                       # normalized, balanced is better


def compute_eme(image, k1=32, k2=32, c=0.0001):                       # NR Metric: EME (Eq.21)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float64)
    h, w = gray.shape
    bh, bw = h // k1, w // k2
    if bh == 0 or bw == 0:
        return 0.0
    score = 0.0
    count = 0
    for i in range(k1):
        for j in range(k2):
            block = gray[i*bh:(i+1)*bh, j*bw:(j+1)*bw]
            Imax, Imin = block.max(), block.min()
            if Imin + c > 0:
                score += 20 * np.log((Imax + c) / (Imin + c))         # Eq.(21)
                count += 1
    return score / count if count > 0 else 0.0                        # higher = better quality


def compute_cqe(image, k1=32, k2=32):                                 # NR Metric: CQE (Eq.22-25)
    img = image.astype(np.float64)
    b, g, r = img[:,:,0], img[:,:,1], img[:,:,2]

    alpha_c = r - g                                                    # Eq.(23): red-green opponent
    beta_c  = 0.5*(r + g) - b                                         # Eq.(23): yellow-blue opponent
    col_score = (0.02 * np.log(np.var(alpha_c) / (abs(np.mean(alpha_c)) + 1e-6) + 1e-6) +
                 0.02 * np.log(np.var(beta_c)  / (abs(np.mean(beta_c))  + 1e-6) + 1e-6))  # Eq.(23)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float64)
    h, w = gray.shape
    bh, bw = max(h // k1, 1), max(w // k2, 1)
    con_score, shar_score, count = 0.0, 0.0, 0
    for i in range(k1):
        for j in range(k2):
            block = gray[i*bh:(i+1)*bh, j*bw:(j+1)*bw]
            Imax, Imin = block.max() + 1e-6, block.min() + 1e-6
            con_score  += (np.log(Imax + Imin) / np.log(Imax - Imin + 1e-6)) ** 0.5    # Eq.(24)
            shar_score += np.log(Imax / Imin + 1e-6)                                    # Eq.(25)
            count += 1
    con_score  /= max(count, 1)
    shar_score /= max(count, 1)

    return 0.33 * col_score + 0.33 * shar_score + 0.34 * con_score    # Eq.(22): higher = better


def compute_all_metrics(original, enhanced):                           # Compute all 4 metrics
    return {
        "TV (Total Variation)" : compute_tv(enhanced),                # NR — lower is better
        "AMBE"                 : compute_ambe(original, enhanced),    # FR — balanced is better
        "EME"                  : compute_eme(enhanced),               # NR — higher is better
        "CQE"                  : compute_cqe(enhanced),               # NR — higher is better
    }