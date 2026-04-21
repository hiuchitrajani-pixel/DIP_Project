# 🌟 Automatic CLAHE with Dual Gamma Correction

> Smarter contrast enhancement — block by block, gamma by gamma.

---

## 📖 About the Project

Standard histogram equalization makes the whole image brighter equally — but that's not how our eyes work. Dark corners need more boosting, bright patches need protection, and textures need sharper detail.

**Automatic CLAHE with Dual Gamma Correction** solves this by:
- Processing the image **block by block** (not as a whole)
- Setting a **smart clip point** for each block based on its texture
- Applying **two gamma corrections** — one to boost luminance, one to protect bright regions

This project is a Python implementation of the research paper:
> *"Automatic Contrast-Limited Adaptive Histogram Equalization With Dual Gamma Correction"*  
> Yakun Chang, Cheolkon Jung, et al. — **IEEE Access, 2018**  
> DOI: [10.1109/ACCESS.2018.2797872](https://doi.org/10.1109/ACCESS.2018.2797872)

---

## 💡 How Does It Work?

### The Full Pipeline

```
📸 Input Image
        ↓
[Step 1]  Convert to Grayscale / Y channel (YCrCb)
[Step 2]  Divide image into 32×32 blocks
[Step 3]  For each block:
            → Content-Adaptive Clip Point      Eq.(8)
            → Clip and redistribute histogram
            → CDF-based remapping              Eq.(4), Eq.(5)
            → First Gamma Correction (γ1)      Eq.(10), Eq.(11), Eq.(12)
            → Second Gamma Correction (γ2)     Eq.(13), Eq.(17), Eq.(18)
            → Apply dual gamma mapping
[Step 4]  Bilinear interpolation between blocks Eq.(6), Eq.(7)
[Step 5]  Merge enhanced channel back
[Step 6]  Color restoration
        ↓
🌟 Enhanced Output Image
```

---

## 🗂️ Project Structure

```
clahe-dual-gamma/
│
├── clahe_dual_gamma.py       # 🧠 Core algorithm — all steps implemented
├── metrics.py                # 📊 Quality evaluation metrics (TV, AMBE, EME, CQE)
├── main.py                   # 🚀 Run the full pipeline here
├── requirements.txt          # 📦 Python dependencies
│
├── sample_input.jpg          # 🌑 Your low-light input image (add this)
├── enhanced_output.jpg       # 🌟 Enhanced result (auto-generated)
├── results_comparison.png    # 🖼️  Side-by-side comparison (auto-generated)
└── histogram_comparison.png  # 📈 RGB histogram plots (auto-generated)
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/dip-lab.git
cd dip-lab/clahe-dual-gamma
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add Your Image
```
sample_input.jpg
```

### 4. Run the Enhancement
```bash
python main.py
```

---

## 📊 Quality Metrics

| Metric | Type | Better When |
|--------|------|-------------|
| TV (Total Variation) | NR | Lower ↓ (less noise) |
| AMBE | FR | Balanced (not too high, not too low) |
| EME | NR | Higher ↑ (better enhancement) |
| CQE | NR | Higher ↑ (color, sharpness, contrast) |

---

## 📚 Reference

```bibtex
@article{chang2018clahe,
  title   = {Automatic Contrast-Limited Adaptive Histogram Equalization
             With Dual Gamma Correction},
  author  = {Chang, Yakun and Jung, Cheolkon and Ke, Peng and
             Song, Hyoseob and Hwang, Jungmee},
  journal = {IEEE Access},
  volume  = {6},
  pages   = {11782--11792},
  year    = {2018},
  doi     = {10.1109/ACCESS.2018.2797872}
}
```

---

## 👨‍💻 Developed By

**Group — ECL 415: Digital Image Processing Lab**  
Department of Electronics & Communication Engineering  
IIIT Nagpur

| Name                  | Roll No     |
|-----------------------|-------------|
| Kuldeep Saini         | BT23ECI009  |
| Uchit Rajani          | BT23ECI010  |
| Satyam Nishad         | BT23ECI027  |
| Krishna Singh Thakur  | BT22ECE002  |

---

## 📝 License

Academic project — ECL-415 Digital Image Processing Lab Exam, April 2026.

---

> *"Every dark corner deserves its own light."* 🌟