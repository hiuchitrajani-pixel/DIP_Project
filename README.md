🌙 IFI-HER: Low-light Image Enhancement
Bringing clarity to darkness — one pixel at a time.

📖 About the Project
Have you ever taken a photo at night or in a poorly lit room, only to end up with a dark, blurry, detail-less image? That's exactly the problem this project tackles.

IFI-HER (Intuitionistic Fuzzy Image – Histogram Equalization Retinex) is a mathematical image enhancement algorithm that intelligently brightens low-light images while preserving their natural colors and fine details — no deep learning, no massive datasets required.

This project is a Python implementation of the research paper:

"Low-light Image Enhancement via New Intuitionistic Fuzzy Generator-based Retinex Approach"
Ragavendirane M.S. & Dhanasekar S. — IEEE Access, 2025
DOI: 10.1109/ACCESS.2025.3545258

💡 How Does It Work?
The algorithm combines two powerful ideas:

1. Intuitionistic Fuzzy Sets (IFS)
Instead of treating each pixel as just bright or dark, IFS represents every pixel with three values — how much it belongs to brightness (membership), how much it doesn't (non-membership), and how uncertain we are (hesitation). This handles the natural ambiguity hiding in dark images.

2. Histogram Equalization Retinex (HER)
Inspired by how the human eye perceives light, Retinex theory separates an image into its illumination (the light source) and reflectance (actual object color). HER then improves the illumination using Histogram Equalization and recombines it — giving you a brighter image that still looks natural.

The Full Pipeline
text
📸 Dark Input Image
        ↓
[Step 1]  Fuzzification       →  Normalize pixels to [0, 1]
[Step 2]  New IFG             →  Compute membership, non-membership & hesitation
[Step 3]  IFI Formation       →  Build the Intuitionistic Fuzzy Image
[Step 4]  HER Algorithm       →  Separate light & color → enhance → recombine
[Step 5]  φ Optimization      →  Run 100 variations, pick the best using Entropy
[Step 6]  Defuzzification     →  Convert back to normal pixel values [0, 255]
        ↓
🌟 Enhanced Output Image
🗂️ Project Structure
text
ifi-her-enhancement/
│
├── ifi_her.py                # 🧠 Core algorithm — all 6 steps implemented
├── metrics.py                # 📊 Quality evaluation metrics
├── main.py                   # 🚀 Run the full pipeline here
├── requirements.txt          # 📦 Python dependencies
│
├── sample_input.jpg          # 🌑 Your low-light input image (add this)
├── enhanced_output.jpg       # 🌟 Enhanced result (auto-generated)
├── results_comparison.png    # 🖼️  Side-by-side comparison (auto-generated)
└── histogram_comparison.png  # 📈 RGB histogram plots (auto-generated)
⚙️ Setup & Installation
1. Clone the Repository
bash
git clone https://github.com/YOUR_USERNAME/dip-lab.git
cd dip-lab/ifi-her-enhancement
2. Install Dependencies
bash
pip install -r requirements.txt
3. Add Your Image
Place any low-light image in the project folder and rename it:

text
sample_input.jpg
💡 You can download free low-light test images from the LOL Dataset

4. Run the Enhancement
bash
python main.py
That's it! Your enhanced image and comparison plots will be saved automatically. ✅

📊 Quality Metrics
The algorithm is evaluated using both Full-Referral (FR) and Non-Referral (NR) metrics, as used in the original paper:

Metric	Type	Meaning	Better When
Entropy	NR	Information richness of image	Higher ↑
AMBE	FR	Brightness deviation from original	Lower ↓
PSNR	FR	Signal quality vs noise	Higher ↑
SSIM	FR	Structural similarity	Higher ↑
Spatial Frequency	NR	Overall sharpness & edge activity	Higher ↑
CPP	NR	Local contrast level	Higher ↑
MIG	NR	Mean edge gradient strength	Higher ↑
Mutual Information	FR	Shared info with original	Higher ↑
🧪 Sample Results
After running main.py, you will get:

📸 enhanced_output.jpg — the brightened image

🖼️ results_comparison.png — original vs enhanced side by side

📈 histogram_comparison.png — RGB channel distribution before & after

📦 Dependencies
text
numpy
opencv-python
scikit-image
matplotlib
scipy
Pillow
Install all at once:

bash
pip install -r requirements.txt
📚 Reference
If you use this implementation, please cite the original paper:

text
@article{ragavendirane2025ifiher,
  title   = {Low-light Image Enhancement via New Intuitionistic
             Fuzzy Generator-based Retinex Approach},
  author  = {Ragavendirane, M.S. and Dhanasekar, S.},
  journal = {IEEE Access},
  year    = {2025},
  doi     = {10.1109/ACCESS.2025.3545258}
}
👨‍💻 Developed By
Group — ECL 415: Digital Image Processing Lab
Department of Electronics & Communication Engineering
IIIT Nagpur

Name	Roll No
Kuldeep Saini	BT23ECI009
Uchit Rajani	BT23ECI010
Satyam Nishad	BT23ECI027
Krishna Singh Thakur	BT22ECE002
📝 License
This project is built for academic purposes as part of the ECL-415 Digital Image Processing Lab Exam, April 2026.

"In the middle of darkness, lies detail waiting to be found." 🌙

