import os
import numpy as np
from imageio import imread, imwrite
from glob import glob
from tqdm import tqdm

# -----------------------------
# User settings
# -----------------------------
dataset_folder = r"C:\Users\peddi\OneDrive\Desktop\input"
output_folder = r"C:\Users\peddi\OneDrive\Desktop\output"
os.makedirs(output_folder, exist_ok=True)

# ADOM parameters
lambda1 = 0.01
lambda2 = 0.01
rho1 = 1.0
rho2 = 1.0
rho3 = 1.0
max_iter = 300
tol = 1e-4

# -----------------------------
# Utility functions
# -----------------------------
def grad_x(img):
    return np.roll(img, -1, axis=1) - img

def grad_y(img):
    return np.roll(img, -1, axis=0) - img

def soft_threshold(x, thresh):
    return np.sign(x) * np.maximum(np.abs(x) - thresh, 0.0)

def group_soft_threshold_cols(M, wg_col, lambda_over_rho):
    H, W = M.shape
    C = np.zeros_like(M)
    for j in range(W):
        col = M[:, j]
        norm = np.linalg.norm(col)
        thresh = wg_col[j] * lambda_over_rho
        if norm > thresh and norm > 0:
            C[:, j] = (1 - thresh / norm) * col
        else:
            C[:, j] = 0.0
    return C

# -----------------------------
# ADOM stripe removal
# -----------------------------
def adom_singleband(O, lambda1, lambda2, rho1, rho2, rho3, tol, max_iter):
    O = O.astype(np.float64)
    H, W = O.shape
    S = np.zeros_like(O)
    A = np.zeros_like(O)
    B = np.zeros_like(O)
    C = np.zeros_like(O)
    tau1 = np.zeros_like(O)
    tau2 = np.zeros_like(O)
    tau3 = np.zeros_like(O)
    wn = np.ones((H, W), dtype=np.float64)
    wg = np.ones(W, dtype=np.float64)

    wy = 2 * np.pi * np.arange(H) / H
    wx = 2 * np.pi * np.arange(W) / W
    WX, WY = np.meshgrid(wx, wy)
    Fx = (np.exp(1j * WX) - 1.0)
    Fy = (np.exp(1j * WY) - 1.0)
    denom = rho1 * (np.conj(Fy) * Fy) + rho2 * (np.conj(Fx) * Fx) + rho3
    denom = np.where(np.abs(denom) < 1e-12, 1e-12, denom)


    gradxO = grad_x(O)
    S_prev = S.copy()

    for k in range(max_iter):
        # Auxiliary updates
        Ty = grad_y(S)
        A = soft_threshold(Ty + tau1 / rho1, 1.0 / rho1)
        Tx = grad_x(O - S)
        B = soft_threshold(Tx + tau2 / rho2, lambda1 / rho2)
        C = group_soft_threshold_cols(S + tau3 / rho3, wg, lambda2 / rho3)

        # Primal update (FFT)
        FA = np.fft.fft2(A - tau1 / rho1)
        FB = np.fft.fft2(gradxO - B + tau2 / rho2)
        FC = np.fft.fft2(C - tau3 / rho3)
        P = rho1 * np.conj(Fy) * FA + rho2 * np.conj(Fx) * FB + rho3 * FC
        S = np.real(np.fft.ifft2(P / denom))

        # Dual updates
        tau1 = tau1 + rho1 * (grad_y(S) - A)
        tau2 = tau2 + rho2 * (grad_x(O - S) - B)
        tau3 = tau3 + rho3 * (S - C)

        # Convergence
        rel = np.linalg.norm(S - S_prev) / (np.linalg.norm(S_prev) + 1e-12)
        S_prev = S.copy()
        if rel < tol:
            break

    D = O - S
    return D, S


# -----------------------------
# Batch processing
# -----------------------------
IMAGE_EXTS = ['.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp']
image_files = []

# Case-insensitive search
for ext in IMAGE_EXTS:
    image_files.extend(glob(os.path.join(dataset_folder, f"*{ext}")))
    image_files.extend(glob(os.path.join(dataset_folder, f"*{ext.upper()}")))

image_files = sorted(image_files)
print("Found images:", image_files)

if len(image_files) == 0:
    raise FileNotFoundError(f"No images found in folder: {dataset_folder}")

for fpath in tqdm(image_files, desc="Processing images"):
    img = imread(fpath)
    if img.ndim == 3:
        img = np.mean(img[..., :3], axis=2)  # grayscale

    mn, mx = img.min(), img.max()
    O_norm = (img - mn) / (mx - mn) if mx > mn else img - mn

    D, S = adom_singleband(O_norm, lambda1, lambda2, rho1, rho2, rho3, tol, max_iter)

    D_out = D * (mx - mn) + mn
    S_out = S * (mx - mn)

    base = os.path.basename(fpath)
    name, _ = os.path.splitext(base)
    imwrite(os.path.join(output_folder, f"{name}_destriped.png"), np.clip(D_out, 0, 255).astype(np.uint8))
    imwrite(os.path.join(output_folder, f"{name}_stripe.png"), np.clip(S_out, 0, 255).astype(np.uint8))

print(f"Done. Results saved in {output_folder}")


