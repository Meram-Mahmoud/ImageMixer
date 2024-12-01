import sys
from PyQt5.QtWidgets import QApplication, QLabel, QFileDialog, QHBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QEvent
import cv2
import numpy as np

class ImageUploader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create the layout for the window
        layout = QHBoxLayout(self)
        
        # Create the original image display QLabel
        self.original_image_label = QLabel(self)
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_image_label.setStyleSheet("background-color: lightgray; border: 1px solid gray;")
        self.original_image_label.setFixedSize(300, 400)  # Rectangle size
        pixmap = QPixmap("ImageMixer/icons/upload.png")  # Replace with your icon file path
        self.original_image_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio))  # Adjust size as needed
        self.image = None
        
        # Create the FT image display QLabel
        self.ft_image_label = QLabel(self)
        self.ft_image_label.setAlignment(Qt.AlignCenter)
        self.ft_image_label.setStyleSheet("background-color: lightgray; border: 1px solid gray;")
        self.ft_image_label.setFixedSize(300, 400)  # Same size as the original image label
        self.ftImage = None
        
        # Add labels to the layout
        layout.addWidget(self.original_image_label)
        layout.addSpacing(30)  # 30px space between the original image and FT image
        layout.addWidget(self.ft_image_label)
        
        # Set the layout for the window
        self.setLayout(layout)
    
    def mousePressEvent(self, event):
        # Handle double-click event to open file dialog
        if event.button() == Qt.LeftButton and event.type() == QEvent.MouseButtonDblClick:
            self.upload_image()
            
    def upload_image(self):
        # Open file dialog to select an image
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.bmp)")
        
        if file_path:
            # Load the image using OpenCV
            img_bgr = cv2.imread(file_path)

            # Convert the image to grayscale
            img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

            # Store the image for FFT processing
            self.image = img_gray

            # Convert the grayscale image to QImage
            height, width = img_gray.shape
            qimage = QImage(img_gray.data, width, height, width, QImage.Format_Grayscale8)

            # Convert QImage to QPixmap and set it in the QLabel
            pixmap = QPixmap.fromImage(qimage)
            self.original_image_label.setPixmap(pixmap.scaled(300, 400, Qt.KeepAspectRatio))

            # Compute the Fourier Transform and display it
            self.fft()

    def fft(self):
        # Compute the 2D Fourier Transform
        f_transform = np.fft.fft2(self.image)
        f_shift = np.fft.fftshift(f_transform)  # Shift the zero frequency component to the center

        # Compute the magnitude spectrum (2D result)
        ft_image = np.log1p(np.abs(f_shift))  # Use log1p for better numerical stability

        # Normalize the result to display as an image
        self.ftImage = cv2.normalize(ft_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        # Convert FT image to QImage for displaying
        height, width = self.ftImage.shape
        qimage_ft = QImage(self.ftImage.data, width, height, width, QImage.Format_Grayscale8)

        # Convert FT QImage to QPixmap and display in the second QLabel
        ft_pixmap = QPixmap.fromImage(qimage_ft)
        self.ft_image_label.setPixmap(ft_pixmap.scaled(300, 400, Qt.KeepAspectRatio))


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ImageUploader()
#     window.setWindowTitle("Image Upload and Fourier Transform")
#     window.resize(850, 850)  # Resize window to fit both images
#     window.show()
#     sys.exit(app.exec_())
