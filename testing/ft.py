import numpy as np
import cv2
import matplotlib.pyplot as plt

# Load the image in grayscale
image = cv2.imread('ImageMixer/images/FB_IMG_1579124180609.jpg', cv2.IMREAD_GRAYSCALE)

# Compute the 2D Fourier Transform
f_transform = np.fft.fft2(image)
f_shift = np.fft.fftshift(f_transform)  # Shift the zero frequency component to the center

# Compute the magnitude spectrum (2D result)
magnitude_spectrum = np.log1p(np.abs(f_shift))  # Use log1p for better numerical stability

# Normalize the result to display as an image
magnitude_spectrum = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# Plot the original image and the 2D Fourier magnitude spectrum
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(image, cmap='gray')

plt.subplot(1, 2, 2)
plt.title("2D Fourier Transform (Magnitude)")
plt.imshow(magnitude_spectrum, cmap='gray')
plt.show()
