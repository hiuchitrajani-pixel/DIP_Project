import numpy as np
import cv2
from skimage.measure import shannon_entropy


def fuzzify(channel):                                                   # Step 1: Fuzzification
    ch = channel.astype(np.float64)
    t_min, t_max = ch.min(), ch.max()
    if t_max == t_min:
        return np.zeros_like(ch), t_min, t_max
    mu = (ch - t_min) / (t_max - t_min)                                # Eq.(7)
    return mu, t_min, t_max


def apply_ifg(mu, phi):                                                 # Step 2: New IFG
    k = (phi + 1.0) ** 3
    mu_prime = (mu * (1.0 + k)) / (1.0 + mu * k)                      # Eq.(14)
    nu_prime = (1.0 - mu) / (1.0 + 2.0 * mu * k + mu * (k ** 2))     # Eq.(15)
    pi = 1.0 - mu_prime - nu_prime                                     # Eq.(16)
    return mu_prime, nu_prime, pi


def compute_ifi(mu_prime, pi):                                          # Step 3: IFI formation
    return np.clip(mu_prime + pi, 0.0, 1.0)                            # Eq.(17)


def apply_her(ifi):                                                     # Step 4: HER (Algorithm 1)
    L = np.log1p(ifi)
    L_illum = cv2.GaussianBlur(L.astype(np.float32), (0, 0), 15).astype(np.float64)
    R = L - L_illum                                                     # Eq.(6)
    L_u8 = cv2.normalize(L_illum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    L_eq = cv2.equalizeHist(L_u8).astype(np.float64) / 255.0
    M = L_eq + R                                                        # Eq.(5)
    return np.clip(np.expm1(M), 0.0, None)


def optimize_phi(mu, t_min, t_max):                                    # Step 5: Phi optimization
    best_entropy = -np.inf
    best_ifi_phi = None
    best_phi = 0.01

    for phi in np.arange(0.01, 1.01, 0.01):
        mu_prime, nu_prime, pi = apply_ifg(mu, phi)
        ifi = compute_ifi(mu_prime, pi)
        ifi_phi = apply_her(ifi)
        img_u8 = cv2.normalize(ifi_phi, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        ent = shannon_entropy(img_u8)                                   # Eq.(4)

        if ent > best_entropy:
            best_entropy = ent
            best_ifi_phi = ifi_phi
            best_phi = phi

    print(f"    Optimal phi={best_phi:.2f} | Entropy={best_entropy:.4f}")
    return best_ifi_phi, best_phi


def defuzzify(ifi_phi, t_min, t_max):                                  # Step 6: Defuzzification
    S = ifi_phi * (t_max - t_min) + t_min                              # Eq.(18)
    return np.clip(S, 0, 255).astype(np.uint8)


def ifi_her_enhance(image_bgr):                                        # Full pipeline
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    enhanced_channels = []

    for idx, name in enumerate(["R", "G", "B"]):
        print(f"  Processing {name} channel...")
        channel = image_rgb[:, :, idx].astype(np.float64)
        mu, t_min, t_max = fuzzify(channel)                            # Step 1
        best_ifi_phi, _ = optimize_phi(mu, t_min, t_max)              # Steps 2-5
        enhanced = defuzzify(best_ifi_phi, t_min, t_max)              # Step 6
        enhanced_channels.append(enhanced)

    enhanced_rgb = np.stack(enhanced_channels, axis=2)
    return cv2.cvtColor(enhanced_rgb, cv2.COLOR_RGB2BGR)