import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft2, ifft2, ifftshift

# Load the original image
image = plt.imread('ImageMixer/images/FB_IMG_1579124180609.jpg')  # Replace with your image path
if image.ndim == 3:
    image = np.mean(image, axis=2)  # Convert to grayscale if the image is colored

# Step 1: Perform the Fourier Transform
fft_image = fft2(image)

# Step 2: Extract the magnitude and discard the phase
magnitude = np.abs(fft_image)
phase = np.angle(fft_image)

# Step 3: Reconstruct the image using the magnitude and a random phase
new_phase = np.mean(phase)
new_mag = np.ones_like(phase)
reconstructed_fft = magnitude * np.exp(1j * new_phase)
reconstructed_image = np.abs(ifft2(reconstructed_fft))

# Plot the original and the reconstructed image using magnitude only
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(image, cmap='gray')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title("Reconstructed Image (Magnitude Only)")
plt.imshow(reconstructed_image, cmap='gray')
plt.axis('off')

plt.show()
