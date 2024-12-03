import numpy as np
import cv2
import matplotlib.pyplot as plt

# Load the image in grayscale
image = cv2.imread(r"C:\Users\HP\OneDrive\Documents\GitHub\equalizerrrr for data\ImageMixer\images\IMG_20200410_220644_467.jpg", cv2.IMREAD_GRAYSCALE)

# Perform Fourier Transform
f_transform = np.fft.fft2(image)
f_transform_shifted = np.fft.fftshift(f_transform)

# Extract Fourier components
magnitude = np.abs(f_transform_shifted)
phase = np.angle(f_transform_shifted)
real_part = np.real(f_transform_shifted)
imaginary_part = np.imag(f_transform_shifted)

# Modify Components

# 1. Modified Magnitude (Scale up all frequencies)
modified_magnitude = magnitude * 0.5

# 2. Modified Phase (Shift phase by a constant)
modified_phase = phase + np.pi / 1

# 3. Modified Real Part (Add constant to real part)
modified_real = real_part + 100

# 4. Modified Imaginary Part (Zero out imaginary part)
modified_imaginary = np.zeros_like(imaginary_part)

# Combine modified components into a single complex Fourier Transform
# Use the modified magnitude and phase to create a complex array
modified_complex = modified_magnitude * np.exp(1j * modified_phase)

# Combine the modified real and imaginary parts into the Fourier array
final_complex = modified_real + 1j * modified_imaginary

# Reconstruct the image from the final Fourier coefficients
f_inverse_shifted = np.fft.ifftshift(final_complex)
reconstructed_image = np.fft.ifft2(f_inverse_shifted).real

# Plotting
plt.figure(figsize=(8, 6))

# Original Image
plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(image, cmap='gray')
plt.axis('off')

# Reconstructed Image with modified components
plt.subplot(1, 2, 2)
plt.title("Reconstructed with Modified Components")
plt.imshow(reconstructed_image, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()