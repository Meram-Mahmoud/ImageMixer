import sys
from PyQt5.QtWidgets import QApplication, QLabel, QFileDialog, QHBoxLayout, QWidget, QComboBox, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPainterPath
from PyQt5.QtCore import Qt, QEvent
import cv2
from ftViewer import FourierTransformViewer
from loader import ImageLoader
import numpy as np

class ImageUploader(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.width, self.height, self.radius = 250, 350, 15

        # Variables for brightness and contrast control
        self.brightness = 0  # Starting brightness (no change)
        self.contrast = 1    # Starting contrast (no change)
        self.is_dragging = False  # To track mouse dragging

        self.image=None
        self.image_ft=FourierTransformViewer()

        # Main horizontal layout
        layout = QHBoxLayout(self)

        # Original Image Section
        self.original_image_label = QLabel(self)
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_image_label.setStyleSheet("border-radius: 10px; border: 2px solid #11361e;")
        self.original_image_label.setFixedSize(self.width, self.height)  # Rectangle size
        pixmap = QPixmap("ImageMixer/icons/coloredUpload.png")
        self.original_image_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio))  # Adjust size as needed
        layout.addWidget(self.original_image_label)

        self.image_loader = ImageLoader(self.original_image_label)

        #layout.addWidget(self.image_loader.image_label)

        layout.addSpacing(20)  # Space between original image and FT section

        ft_layout = QVBoxLayout()  # Vertical layout for ComboBox and FT image
        ft_layout.addWidget(self.image_ft.component_combo)  # Add FourierTransformViewer ComboBox
        ft_layout.addWidget(self.image_ft.ft_image_label)  # Add FourierTransformViewer FT Image
        layout.addLayout(ft_layout)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.type() == QEvent.MouseButtonDblClick:
            self.image=self.image_loader.upload_image()
            self.image_ft.setData(cv2.resize(self.image, (self.width, self.height)))
            # print("doneeeeee in the imageUploader class , MAGNITUDE HERE:")
            # print(self.image_ft.magnitude)
        elif event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.last_pos = event.pos()  # Remember the mouse position

    def mouseMoveEvent(self, event):
        # Handle mouse dragging (adjust brightness/contrast)
        if self.is_dragging:
            dx = event.x() - self.last_pos.x()  # Horizontal movement (contrast)
            dy = event.y() - self.last_pos.y()  # Vertical movement (brightness)
            self.last_pos = event.pos()  # Update the last position
            
            # Update contrast and brightness
            self.contrast += dx * 0.01  # Sensitivity for contrast
            self.brightness += dy * 0.1  # Sensitivity for brightness
            
            # Apply the changes to the image
            self.image_loader.update_image()

    def mouseReleaseEvent(self, event):
        # Stop dragging when mouse button is released
        if event.button() == Qt.LeftButton:
            self.is_dragging = False

            
    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.bmp)")
        
        if file_path:
            img_bgr = cv2.imread(file_path)
            img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            self.image = cv2.resize(img_gray, (self.width, self.height))

            # Convert the grayscale image to QImage
            height, width = img_gray.shape
            qimage = QImage(img_gray.data, width, height, width, QImage.Format_Grayscale8)

            # Convert QImage to QPixmap and set it in the QLabel
            pixmap = QPixmap.fromImage(qimage)
            pixmap = self.image_loader.get_rounded_pixmap(pixmap, self.image_loader.image_label.size(), self.radius)
            self.image_loader.image_label.setPixmap(pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio))

            #self.fft()

            self.image_ft.setData(self.image)
            # print("doneeeeee in the imageUploader class , MAGNITUDE HERE:")
            # print(self.image_ft.magnitude)

    def get_component(self):
        return self.image_ft.magnitude


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ImageUploader()
#     window.setWindowTitle("Image Upload and Fourier Transform")
#     window.resize(850, 850)  # Resize window to fit both images
#     window.show()
#     sys.exit(app.exec_())
