import cv2
import matplotlib.pyplot as plt
import os, time
from algo import ifi_her_enhance
from metrics import compute_all_metrics

INPUT_IMAGE = "sample_input.jpg"                                       # input low-light image
OUTPUT_IMAGE = "enhanced_output.jpg"                                   # output enhanced image


def main():
    if not os.path.exists(INPUT_IMAGE):                                # check input image
        print(f"[ERROR] Place a low-light image as '{INPUT_IMAGE}'")
        return

    print("=" * 55)
    print("  IFI-HER: Low-light Image Enhancement")
    print("  DOI: 10.1109/ACCESS.2025.3545258")
    print("=" * 55)

    original = cv2.imread(INPUT_IMAGE)                                 # read input image
    print(f"\n[INFO] Image: {INPUT_IMAGE} | Shape: {original.shape}")

    print("\n[STEP] Running IFI-HER...")
    t0 = time.time()
    enhanced = ifi_her_enhance(original)                               # run full enhancement pipeline
    print(f"\n[INFO] Done in {time.time()-t0:.2f}s")

    cv2.imwrite(OUTPUT_IMAGE, enhanced)                                # save enhanced image
    print(f"[INFO] Saved → {OUTPUT_IMAGE}")

    print("\n[STEP] Quality Metrics:")
    metrics = compute_all_metrics(original, enhanced)                  # compute all metrics
    print("-" * 42)
    for k, v in metrics.items():
        print(f"  {k:<26} {v:.4f}")
    print("-" * 42)

    orig_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)               # convert original to RGB
    enh_rgb = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)                # convert enhanced to RGB

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))                    # comparison plot
    fig.suptitle("IFI-HER: Low-light Image Enhancement", fontsize=16, fontweight="bold")
    axes[0].imshow(orig_rgb); axes[0].set_title("Original"); axes[0].axis("off")
    axes[1].imshow(enh_rgb); axes[1].set_title("Enhanced (IFI-HER)"); axes[1].axis("off")
    plt.tight_layout()
    plt.savefig("results_comparison.png", dpi=150, bbox_inches="tight")  # save comparison plot
    print("[INFO] Saved → results_comparison.png")

    fig2, ax2 = plt.subplots(2, 3, figsize=(15, 8))                   # histogram plot
    fig2.suptitle("RGB Histograms: Original vs Enhanced", fontsize=14, fontweight="bold")

    for i, (c, lbl) in enumerate(zip(["red", "green", "blue"], ["Red", "Green", "Blue"])):
        ax2[0, i].hist(orig_rgb[:, :, i].flatten(), bins=256, color=c, alpha=0.7)   # original histogram
        ax2[0, i].set_title(f"Original - {lbl}"); ax2[0, i].set_xlim([0, 256])

        ax2[1, i].hist(enh_rgb[:, :, i].flatten(), bins=256, color=c, alpha=0.7)    # enhanced histogram
        ax2[1, i].set_title(f"Enhanced - {lbl}"); ax2[1, i].set_xlim([0, 256])

    plt.tight_layout()
    plt.savefig("histogram_comparison.png", dpi=150, bbox_inches="tight")  # save histogram plot
    print("[INFO] Saved → histogram_comparison.png")

    print("\n[DONE] All outputs generated!")


if __name__ == "__main__":
    main()