import sys
from PyQt5.QtWidgets import QApplication, QLabel, QFileDialog, QHBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPainterPath
from PyQt5.QtCore import Qt, QEvent
import cv2
import numpy as np

class ImageUploader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create the layout for the window
        layout = QHBoxLayout(self)
        self.width, self.height, self.radius = 250, 350, 15
        # Create the original image display QLabel
        self.original_image_label = QLabel(self)
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_image_label.setStyleSheet("border-radius: 10px; border: 2px solid #73917b;")
        self.original_image_label.setFixedSize(self.width, self.height)  # Rectangle size
        pixmap = QPixmap("ImageMixer/icons/coloredUpload.png")
        self.original_image_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio))  # Adjust size as needed
        self.image = None
        
        # Create the FT image display QLabel
        self.ft_image_label = QLabel(self)
        self.ft_image_label.setAlignment(Qt.AlignCenter)
        self.ft_image_label.setStyleSheet("border-radius: 10px; border: 2px solid #73917b;")
        self.ft_image_label.setFixedSize(self.width, self.height)  # Same size as the original image label
        self.ftImage = None
        
        # Add labels to the layout
        layout.addWidget(self.original_image_label)
        layout.addSpacing(10)  # 30px space between the original image and FT image
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
            pixmap = self.get_rounded_pixmap(pixmap, self.original_image_label.size(), self.radius)
            self.original_image_label.setPixmap(pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio))

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

        # Convert QImage to QPixmap
        pixmap_ft = QPixmap.fromImage(qimage_ft)

        # Apply rounded corners to the FT pixmap
        rounded_ft_pixmap = self.get_rounded_pixmap(pixmap_ft, self.ft_image_label.size(), self.radius)

        # Display the rounded FT pixmap in the second QLabel
        self.ft_image_label.setPixmap(rounded_ft_pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio))
    
    # Changing the style of the image to match the size of the rectangle
    def get_rounded_pixmap(self, pixmap, size, radius):
        # Resize the pixmap to fit the QLabel
        pixmap = pixmap.scaled(size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        # Create a transparent pixmap with the QLabel's size
        rounded_pixmap = QPixmap(size)
        rounded_pixmap.fill(Qt.transparent)

        # Create a QPainter to draw the rounded pixmap
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        # Create a rounded rectangle path
        path = QPainterPath()
        path.addRoundedRect(0, 0, size.width(), size.height(), radius, radius)

        # Set the clip path and draw the pixmap
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        return rounded_pixmap



# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ImageUploader()
#     window.setWindowTitle("Image Upload and Fourier Transform")
#     window.resize(850, 850)  # Resize window to fit both images
#     window.show()
#     sys.exit(app.exec_())
