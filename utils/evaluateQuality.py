import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np

def evaluate_ssim(panorama, original):

    pano_gray = cv2.cvtColor(panorama, cv2.COLOR_BGR2GRAY)
    original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

    ssim_score = ssim(pano_gray, original_gray)

    print(ssim_score)

def evaluate_rmse(panorama, original):
    mse = np.mean((original - panorama) ** 2)
    rmse = np.sqrt(mse)

    print(rmse)

    max_channel_diff = 255
    num_channels = 3

    max_rmse_rgb = np.sqrt(num_channels * max_channel_diff ** 2)
    print(max_rmse_rgb)



if __name__ == '__main__':
    panorama = cv2.imread("evaluation/remove-anything/3.png")
    original = cv2.imread("evaluation/remove-anything/4.png")
    evaluate_ssim(panorama, original)
    evaluate_rmse(panorama, original)