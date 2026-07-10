# Satellite Image Destriping Using ADOM with Synthetic Stripe Noise Generation

## 📖 Overview

This project focuses on removing stripe noise from satellite images using the **Alternating Direction Optimization Method (ADOM)**.

Since publicly available satellite image datasets containing both **striped images** and their corresponding **clean ground truth images** are not readily available, this project first generates **synthetic stripe noise** on clean satellite images. The generated striped images are then processed using the ADOM-based destriping algorithm to recover the original image.

---

## 🚀 Features

- Generate synthetic stripe noise
- Create paired clean and noisy datasets
- Remove stripe noise using ADOM
- Batch processing of satellite images
- Save recovered images and extracted stripe components
- Easy to customize stripe intensity and width

---

## 📂 Project Structure

```
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

## 🛠 Requirements

Install the required libraries using:

```bash
pip install numpy opencv-python imageio tqdm
```

---

## 📊 Workflow

```
Clean Satellite Images
        │
        ▼
Synthetic Stripe Generation
        │
        ▼
Striped Images
        │
        ▼
ADOM Destriping Algorithm
        │
        ▼
Recovered Images
```

---

## Stage 1: Stripe Generation

Run:

```bash
python stripsadding.py
```

### Functionality

- Reads clean satellite images.
- Resizes images to **256 × 256**.
- Adds artificial vertical stripe noise.
- Saves:
  - Clean images
  - Noisy (striped) images

---

## Stage 2: Stripe Removal

Run:

```bash
python stripe_to_sameimage.py
```

### Functionality

- Reads striped images.
- Converts RGB images to grayscale.
- Applies the ADOM optimization algorithm.
- Removes stripe noise.
- Saves:
  - Destriped image
  - Estimated stripe component

---

## 📁 Input

Place the striped images inside the **input** folder.

Example:

```
input/
    image1.png
    image2.png
```

---

## 📁 Output

After execution, the output folder will contain:

```
output/
    image1_destriped.png
    image1_stripe.png
```

---

## Algorithm

The observed image is represented as:

```
Observed Image = Clean Image + Stripe Noise
```

or

```
O = D + S
```

where

- **O** = Observed image
- **D** = Destriped image
- **S** = Stripe component

The ADOM algorithm estimates the stripe component (**S**) and subtracts it from the observed image to recover the clean image.

---

## Applications

- Remote Sensing
- Satellite Image Enhancement
- Agriculture
- Environmental Monitoring
- GIS
- Disaster Management
- Land Cover Analysis

---

## Advantages

- Automatic stripe generation
- Fast optimization using FFT
- Batch image processing
- Easy to modify parameters
- Produces clean and stripe component separately

---

## Limitations

- Uses synthetic stripe noise instead of real sensor noise.
- Mainly designed for vertical stripe artifacts.
- Converts images to grayscale during destriping.

---

## Future Work

- Support real satellite stripe datasets.
- RGB image destriping.
- Deep learning-based stripe removal.
- GUI application.
- Performance evaluation using PSNR and SSIM.

---

## Authors

**Final Year Project**

**Title:** Satellite Image Destriping Using ADOM with Synthetic Stripe Noise Generation

---

## License

This project is developed for educational and research purposes.
