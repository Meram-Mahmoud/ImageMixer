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
modified_magnitude = magnitude * 0.1

# 2. Modified Phase (Shift phase by a constant)
modified_phase = phase + np.pi / 2

# 3. Modified Real Part (Add constant to real part)
modified_real = real_part + 500

# 4. Modified Imaginary Part (Zero out imaginary part)
modified_imaginary = np.zeros_like(imaginary_part)

# Reconstruct Images
def reconstruct_from_components(mag, ph):
    complex_array = mag * np.exp(1j * ph)
    f_inverse_shifted = np.fft.ifftshift(complex_array)
    return np.fft.ifft2(f_inverse_shifted).real

def reconstruct_from_real_imag(real, imag):
    complex_array = real + 1j * imag
    f_inverse_shifted = np.fft.ifftshift(complex_array)
    return np.fft.ifft2(f_inverse_shifted).real

# Reconstructed Images
image_modified_magnitude = reconstruct_from_components(modified_magnitude, phase)
image_modified_phase = reconstruct_from_components(magnitude, modified_phase)
image_modified_real = reconstruct_from_real_imag(modified_real, imaginary_part)
image_modified_imaginary = reconstruct_from_real_imag(real_part, modified_imaginary)

# Plotting
plt.figure(figsize=(15, 10))

# Original Image
plt.subplot(2, 3, 1)
plt.title("Original Image")
plt.imshow(image, cmap='gray')
plt.axis('off')

# Modified Magnitude
plt.subplot(2, 3, 2)
plt.title("Modified Magnitude")
plt.imshow(image_modified_magnitude, cmap='gray')
plt.axis('off')

# Modified Phase
plt.subplot(2, 3, 3)
plt.title("Modified Phase")
plt.imshow(image_modified_phase, cmap='gray')
plt.axis('off')

# Modified Real Part
plt.subplot(2, 3, 4)
plt.title("Modified Real Part")
plt.imshow(image_modified_real, cmap='gray')
plt.axis('off')

# Modified Imaginary Part
plt.subplot(2, 3, 5)
plt.title("Modified Imaginary Part")
plt.imshow(image_modified_imaginary, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()