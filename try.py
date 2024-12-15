import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft2, ifft2, ifftshift

# Load the original image
image1 = plt.imread('ImageMixer/images/FB_IMG_1579124180609.jpg')  # Replace with your image path
if image1.ndim == 3:
    image1 = np.mean(image1, axis=2)  # Convert to grayscale if the image is colored

image2 = plt.imread('ImageMixer/images/IMG_20200410_220644_467.jpg')  # Replace with your image path
if image2.ndim == 3:
    image2 = np.mean(image2, axis=2)  # Convert to grayscale if the image is colored

# Step 1: Perform the Fourier Transform
fft_image1 = fft2(image1)
fft_image2 = fft2(image2)

# Step 2: Extract the magnitude and discard the phase
magnitude1 = np.abs(fft_image1)
phase1 = np.angle(fft_image1)
magnitude2 = np.abs(fft_image2)
phase2 = np.angle(fft_image2)

# Step 3: Reconstruct the image using the magnitude and a random phase

new_phase = 1*phase1+1*phase2
new_mag = 1*magnitude1+1*magnitude2
new_phase = np.where(new_phase< -np.pi, 
                    new_phase+ np.pi, 
                    new_phase)
new_phase = np.where(new_phase> np.pi, 
                    new_phase- np.pi, 
                    new_phase)

reconstructed_fft = new_mag/2 * np.exp(1j * new_phase)
reconstructed_image = np.abs(ifft2(ifftshift(reconstructed_fft)))

# Plot the original and the reconstructed image using magnitude only
plt.figure(figsize=(10, 5))

plt.subplot(1, 3, 1)
plt.title("Original Image")
plt.imshow(image1, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title("Original Image")
plt.imshow(image2, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.title("Reconstructed Image (Magnitude Only)")
plt.imshow(reconstructed_image, cmap='gray')
plt.axis('off')

plt.show()
