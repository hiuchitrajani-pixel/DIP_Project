# 📊 DIP Lab — Comparative Study of Low-light Image Enhancement

> ECL-415: Digital Image Processing Lab | IIIT Nagpur | April 2026

---

## 📖 Overview

This repository contains Python implementations of **two research papers** on low-light image enhancement, done as part of the ECL-415 Digital Image Processing Lab Exam 2026.

Both algorithms tackle the same core problem — making dark images brighter and clearer — but use **completely different approaches**. This comparative study evaluates how they perform against each other using standard image quality metrics.

---

## 📂 Repository Structure

```
dip-lab/
│
├── ifi-her-enhancement/          # Paper 1 — IFI-HER Algorithm
│   ├── ifi_her.py
│   ├── metrics.py
│   ├── main.py
│   └── requirements.txt
│
├── clahe-dual-gamma/             # Paper 2 — Automatic CLAHE + Dual Gamma
│   ├── clahe_dual_gamma.py
│   ├── metrics.py
│   ├── main.py
│   └── requirements.txt
│
└── README.md                     # ← You are here (Comparative study overview)
```

---

## 📄 Paper 1 — IFI-HER

**Title:** Low-light Image Enhancement via New Intuitionistic Fuzzy Generator-based Retinex Approach

**Authors:** Ragavendirane M.S. & Dhanasekar S.

**Published in:** IEEE Access, 2025

**DOI:** [10.1109/ACCESS.2025.3545258](https://doi.org/10.1109/ACCESS.2025.3545258)

### Core Idea

IFI-HER uses **Intuitionistic Fuzzy Sets (IFS)** to model pixel uncertainty, then applies a **Retinex-based Histogram Equalization (HER)** to separate and enhance image illumination.

### Algorithm Pipeline

```
Input Image
    ↓
Step 1 → Fuzzification                 (Eq.7)   Normalize pixels to [0,1]
Step 2 → New IFG                       (Eq.14-16) Compute membership, non-membership, hesitation
Step 3 → IFI Formation                 (Eq.17)  Build Intuitionistic Fuzzy Image
Step 4 → HER Algorithm                 (Algo.1) Separate illumination → HE → recombine
Step 5 → Optimize φ using Entropy      (Eq.4)   100 iterations, pick best result
Step 6 → Defuzzification               (Eq.18)  Convert back to [0,255]
    ↓
Enhanced Output
```

### Key Characteristics
- Based on **fuzzy set theory** — handles pixel uncertainty mathematically
- Works on **RGB channel → YCrCb Y-channel** (luminance only)
- Selects best enhancement parameter (φ) automatically using Shannon Entropy
- Slower (100 iterations per channel) but mathematically principled

---

## 📄 Paper 2 — Automatic CLAHE with Dual Gamma Correction

**Title:** Automatic Contrast-Limited Adaptive Histogram Equalization With Dual Gamma Correction

**Authors:** Yakun Chang, Cheolkon Jung, Peng Ke, Hyoseob Song, Jungmee Hwang

**Published in:** IEEE Access, 2018

**DOI:** [10.1109/ACCESS.2018.2797872](https://doi.org/10.1109/ACCESS.2018.2797872)

### Core Idea

This method divides the image into **32×32 blocks** and applies CLAHE with a **content-adaptive clip point** and **dual gamma correction** (γ1 + γ2) to simultaneously boost luminance and control over-enhancement.

### Algorithm Pipeline

```
Input Image
    ↓
Step 1 → Divide into 32×32 blocks
Step 2 → Per-block content-adaptive clip point  (Eq.8)
Step 3 → Histogram clipping + redistribution
Step 4 → CDF remapping                          (Eq.4, 5)
Step 5 → First gamma correction γ1              (Eq.10-12)
Step 6 → Second gamma correction γ2 (if needed) (Eq.13, 17-18)
Step 7 → Bilinear interpolation between blocks   (Eq.6, 7)
    ↓
Enhanced Output
```

### Key Characteristics
- Block-by-block local processing — better at preserving details in mixed lighting
- Automatically adapts clip point based on block texture (mean + std deviation)
- Dual gamma prevents over-enhancement in bright regions while boosting dark ones
- Very fast — more than 35 frames/sec at 1024×682 resolution

---

## ⚖️ Side-by-Side Comparison

| Feature | IFI-HER (Paper 1) | CLAHE Dual Gamma (Paper 2) |
|---|---|---|
| **Core theory** | Intuitionistic Fuzzy Sets + Retinex | Adaptive CLAHE + Gamma Correction |
| **Processing domain** | Full image (Y channel) | Block-wise (32×32 tiles) |
| **Parameter selection** | Automatic via entropy (100 iterations) | Adaptive per block via texture |
| **Handles bright highlights** | Moderate | Better (γ2 prevents over-enhancement) |
| **Handles very dark regions** | Very good (fuzzy uncertainty) | Good (γ2 boosts dark blocks) |
| **Color preservation** | YCrCb (luminance only) | YCrCb (luminance only) |
| **Speed** | Slow (~1-2 min for one image) | Fast (35+ fps) |
| **Published** | IEEE Access 2025 | IEEE Access 2018 |

---

## 📊 Evaluation Metrics

### Paper 1 — IFI-HER Metrics

| Metric | Type | Better When |
|--------|------|-------------|
| Entropy | NR | Higher ↑ |
| AMBE | FR | Lower ↓ |
| PSNR | FR | Higher ↑ |
| SSIM | FR | Higher ↑ |
| Spatial Frequency | NR | Higher ↑ |
| CPP | NR | Higher ↑ |
| MIG | NR | Higher ↑ |
| Mutual Information | FR | Higher ↑ |

### Paper 2 — Automatic CLAHE Metrics

| Metric | Type | Better When |
|--------|------|-------------|
| TV (Total Variation) | NR | Lower ↓ (less noise) |
| AMBE | FR | Balanced |
| EME | NR | Higher ↑ |
| CQE | NR | Higher ↑ |

---

## 🚀 How to Run

### Paper 1 — IFI-HER
```bash
cd ifi-her-enhancement
pip install -r requirements.txt
python main.py
```

### Paper 2 — Automatic CLAHE
```bash
cd clahe-dual-gamma
pip install -r requirements.txt
python main.py
```

> 💡 In both cases, rename your dark input image to `sample_input.jpg` and place it inside the respective folder.

---

## 📚 References

1. Ragavendirane M.S. & Dhanasekar S., *"Low-light Image Enhancement via New Intuitionistic Fuzzy Generator-based Retinex Approach"*, IEEE Access, 2025. DOI: [10.1109/ACCESS.2025.3545258](https://doi.org/10.1109/ACCESS.2025.3545258)

2. Yakun Chang et al., *"Automatic Contrast-Limited Adaptive Histogram Equalization With Dual Gamma Correction"*, IEEE Access, 2018. DOI: [10.1109/ACCESS.2018.2797872](https://doi.org/10.1109/ACCESS.2018.2797872)

---

## 👨‍💻 Developed By

**Group — ECL 415: Digital Image Processing Lab**  
Department of Electronics & Communication Engineering  
IIIT Nagpur | April 2026

| Name                  | Roll No     |
|-----------------------|-------------|
| Kuldeep Saini         | BT23ECI009  |
| Uchit Rajani          | BT23ECI010  |
| Satyam Nishad         | BT23ECI027  |
| Krishna Singh Thakur  | BT22ECE002  |

---

> *"Two papers. One problem. Different solutions."* 📊