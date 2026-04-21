import numpy as np
import cv2
from skimage.measure import shannon_entropy
from skimage.metrics import peak_signal_noise_ratio as psnr_metric
from skimage.metrics import structural_similarity as ssim_metric


def compute_entropy(image):                                             # NR Metric: Entropy
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return shannon_entropy(gray)                                        # higher = more detail


def compute_ambe(original, enhanced):                                  # FR Metric: AMBE
    o = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY).astype(np.float64)
    e = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY).astype(np.float64)
    return abs(np.mean(o) - np.mean(e))                                # lower = better brightness preservation


def compute_psnr(original, enhanced):                                  # FR Metric: PSNR
    o = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    e = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
    return psnr_metric(o, e, data_range=255)                           # higher = less distortion


def compute_ssim(original, enhanced):                                  # FR Metric: SSIM
    o = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    e = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
    return ssim_metric(o, e, data_range=255)                           # higher = better structural similarity


def compute_spatial_frequency(image):                                  # NR Metric: Spatial Frequency
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float64)
    rf = np.sqrt(np.mean(np.diff(gray, axis=1) ** 2))                  # row frequency
    cf = np.sqrt(np.mean(np.diff(gray, axis=0) ** 2))                  # column frequency
    return np.sqrt(rf**2 + cf**2)                                      # higher = sharper image


def compute_cpp(image):                                                # NR Metric: CPP
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float64)
    lap = cv2.Laplacian(gray, cv2.CV_64F)                              # local contrast
    return np.sum(np.abs(lap)) / gray.size                             # higher = better contrast


def compute_mig(image):                                                # NR Metric: MIG
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float64)
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)                    # horizontal gradient
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)                    # vertical gradient
    return np.mean(np.sqrt(gx**2 + gy**2))                             # higher = stronger edges


def compute_mutual_information(original, enhanced):                    # FR Metric: Mutual Information
    o = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY).flatten().astype(np.float64)
    e = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY).flatten().astype(np.float64)
    hist2d, _, _ = np.histogram2d(o, e, bins=256, range=[[0,255],[0,255]])
    pxy = hist2d / hist2d.sum()                                        # joint probability
    px = pxy.sum(axis=1)                                               # original probability
    py = pxy.sum(axis=0)                                               # enhanced probability
    pxpy = px[:, None] * py[None, :]
    nz = pxy > 0
    return float(np.sum(pxy[nz] * np.log2(pxy[nz] / pxpy[nz])))       # higher = more shared information


def compute_all_metrics(original, enhanced):                           # Compute all metrics
    return {
        "Entropy": compute_entropy(enhanced),                          # NR
        "AMBE": compute_ambe(original, enhanced),                      # FR
        "PSNR (dB)": compute_psnr(original, enhanced),                 # FR
        "SSIM": compute_ssim(original, enhanced),                      # FR
        "Spatial Frequency": compute_spatial_frequency(enhanced),      # NR
        "CPP": compute_cpp(enhanced),                                  # NR
        "MIG": compute_mig(enhanced),                                  # NR
        "Mutual Information": compute_mutual_information(original, enhanced),  # FR
    }