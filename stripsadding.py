import os
import cv2
import numpy as np
import random
from tqdm import tqdm
import zipfile

# Paths
clean_dataset_path = r"C:\Users\peddi\OneDrive\Desktop\uc_merced_dataset"  # folder of clean images
output_path = r"C:\Users\peddi\OneDrive\Desktop\EuroSAT_with_stripes"

os.makedirs(output_path, exist_ok=True)

# Function to add stripe noise
def add_stripe_noise(image, intensity=0.3, stripe_width=3):
    noisy = image.copy().astype(np.float32) / 255.0
    cols = noisy.shape[1]
    # randomly place stripes
    for c in range(0, cols, stripe_width*random.randint(5,15)):
        noisy[:, c:c+stripe_width] += intensity * np.random.uniform(0.5, 1.5)
    noisy = np.clip(noisy, 0, 1)
    return (noisy * 255).astype(np.uint8)

# Iterate over dataset
for root, _, files in os.walk(clean_dataset_path):
    for file in tqdm(files):
        if file.lower().endswith(('.jpg', '.png', '.jpeg', '.tif')):
            img_path = os.path.join(root, file)
            img = cv2.imread(img_path)

            if img is None:
                continue

            # Resize for consistency
            img = cv2.resize(img, (256, 256))

            # Save original
            save_folder_clean = os.path.join(output_path, "clean")
            os.makedirs(save_folder_clean, exist_ok=True)
            cv2.imwrite(os.path.join(save_folder_clean, file), img)

            # Save noisy (with stripes)
            noisy_img = add_stripe_noise(img)
            save_folder_noisy = os.path.join(output_path, "noisy")
            os.makedirs(save_folder_noisy, exist_ok=True)
            cv2.imwrite(os.path.join(save_folder_noisy, file), noisy_img)

print("Dataset with stripes generated at:", output_path)

# Optional: zip the dataset for portability
zip_path = output_path + ".zip"
with zipfile.ZipFile(zip_path, 'w') as zipf:
    for root, _, files in os.walk(output_path):
        for file in files:
            filepath = os.path.join(root, file)
            zipf.write(filepath, os.path.relpath(filepath, output_path))

print("Zipped dataset at:", zip_path)

