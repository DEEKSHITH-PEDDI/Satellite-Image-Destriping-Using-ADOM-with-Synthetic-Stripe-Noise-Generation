# Satellite Image Destriping Using ADOM with Synthetic Stripe Noise Generation

## Table of Contents
1. Overview
2. Objectives
3. Features
4. Project Structure
5. Software Requirements
6. Installation
7. Methodology
8. Workflow
9. Algorithm
10. Mathematical Model
11. Input and Output
12. How to Run
13. Applications
14. Advantages
15. Limitations
16. Future Enhancements
17. Conclusion
18. Authors
19. License

---

# Overview

Satellite images are widely used in remote sensing, agriculture, environmental monitoring, urban planning, and disaster management. One common problem affecting the quality of satellite imagery is **stripe noise**, which appears as unwanted vertical lines caused by detector inconsistencies, calibration errors, or sensor malfunction.

Because publicly available paired datasets containing both striped images and their corresponding clean images are limited, this project creates **synthetic stripe noise** from clean satellite images and then removes it using the **Alternating Direction Optimization Method (ADOM)**.

The project consists of two major phases:

1. Synthetic Stripe Noise Generation
2. Stripe Removal using ADOM

---

# Objectives

- Generate synthetic stripe noise on clean satellite images.
- Create paired clean and noisy datasets.
- Remove stripe noise using ADOM.
- Recover high-quality satellite images.
- Provide a reproducible pipeline for satellite image destriping.

---

# Features

- Artificial stripe noise generation
- Batch image processing
- ADOM optimization
- FFT-based optimization
- Stripe component extraction
- Destriped image reconstruction
- Supports PNG, JPG, JPEG, BMP, TIFF images

---

# Project Structure

```text
Satellite-Image-Destriping/
│
├── stripsadding.py
├── stripe_to_sameimage.py
├── input/
├── output/
├── clean/
├── noisy/
├── README.md
└── requirements.txt
```

---

# Software Requirements

- Python 3.9+
- NumPy
- OpenCV
- ImageIO
- tqdm

Install dependencies:

```bash
pip install numpy opencv-python imageio tqdm
```

---

# Methodology

## Step 1: Dataset Collection

Clean satellite images are collected from datasets such as UC Merced or EuroSAT. These images serve as the ground truth.

## Step 2: Image Preprocessing

- Read each image.
- Resize to 256 × 256 pixels.
- Store images in a standard format.

## Step 3: Synthetic Stripe Noise Generation

The `stripsadding.py` script:

- Reads clean images.
- Randomly selects image columns.
- Adds vertical stripe noise with configurable width and intensity.
- Saves:
  - Clean images
  - Noisy (striped) images

This creates paired data for evaluation.

## Step 4: Image Normalization

Images are normalized to the range [0,1] before optimization for numerical stability.

## Step 5: Stripe Removal using ADOM

The `stripe_to_sameimage.py` script:

- Reads striped images.
- Converts RGB images to grayscale.
- Computes image gradients.
- Applies soft thresholding and group soft thresholding.
- Uses FFT for efficient optimization.
- Iteratively estimates stripe noise.
- Reconstructs the clean image.

## Step 6: Output Generation

For every image:

- `*_destriped.png` – recovered image.
- `*_stripe.png` – extracted stripe component.

---

# Workflow

```text
Clean Satellite Images
        │
        ▼
Image Preprocessing
        │
        ▼
Synthetic Stripe Generation
        │
        ▼
Striped Images
        │
        ▼
Image Normalization
        │
        ▼
ADOM Optimization
        │
        ▼
Stripe Estimation
        │
        ▼
Image Reconstruction
        │
        ▼
Recovered Image + Stripe Component
```

---

# Algorithm

ADOM separates the observed image into a clean image and stripe component.

Major operations:

- Gradient computation
- Soft thresholding
- Group soft thresholding
- FFT optimization
- Dual variable update
- Convergence checking

The algorithm iterates until convergence or the maximum number of iterations.

---

# Mathematical Model

Observed image:

O = D + S

Where:

- O = Observed striped image
- D = Clean image
- S = Stripe component

Recovered image:

D = O − S

---

# Input and Output

## Input

- Clean satellite images for stripe generation.
- Striped satellite images for destriping.

## Output

- Destriped satellite image.
- Estimated stripe image.

---

# How to Run

## Generate Synthetic Stripes

```bash
python stripsadding.py
```

## Run Stripe Removal

```bash
python stripe_to_sameimage.py
```

Outputs are stored inside the `output` folder.

---

# Applications

- Remote Sensing
- Agriculture
- GIS
- Environmental Monitoring
- Disaster Management
- Land Cover Mapping

---

# Advantages

- Easy to use
- Generates paired datasets
- Fast optimization using FFT
- Batch processing
- Adjustable stripe intensity

---

# Limitations

- Uses synthetic stripe noise.
- Mainly designed for vertical stripes.
- Converts images to grayscale during destriping.

---

# Future Enhancements

- RGB destriping
- Real satellite stripe datasets
- Deep learning-based methods
- GUI application
- PSNR, SSIM and RMSE evaluation
- High-resolution image support

---

# Conclusion

This project presents a complete pipeline for satellite image destriping. Synthetic stripe noise is first generated on clean satellite images to create a paired dataset. The ADOM optimization algorithm then estimates and removes stripe noise, producing restored images while preserving important image details. The methodology enables objective evaluation because the original clean image is available for comparison.

---


# License

This project is intended for educational and research purposes.
