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

        self.image_ft=FourierTransformViewer()
        self.image_loader = ImageLoader()

        # Main horizontal layout
        layout = QHBoxLayout(self)

        layout.addWidget(self.image_loader.image_label)

        # # Original Image Section
        # self.original_image_label = QLabel(self)
        # self.original_image_label.setAlignment(Qt.AlignCenter)
        # self.original_image_label.setStyleSheet("border-radius: 10px; border: 2px solid #01240e;")
        # self.original_image_label.setFixedSize(self.width, self.height)  # Rectangle size
        # pixmap = QPixmap("ImageMixer/icons/coloredUpload.png")
        # self.original_image_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio))  # Adjust size as needed
        # layout.addWidget(self.original_image_label)

        layout.addSpacing(20)  # Space between original image and FT section


        ft_layout = QVBoxLayout()  # Vertical layout for ComboBox and FT image
        ft_layout.addWidget(self.image_ft.component_combo)  # Add FourierTransformViewer ComboBox
        ft_layout.addWidget(self.image_ft.ft_image_label)  # Add FourierTransformViewer FT Image
        layout.addLayout(ft_layout)

        # # Fourier Transform Section (ComboBox + Rectangle)
        # ft_layout = QVBoxLayout()  # Vertical layout for ComboBox and FT image

        # # ComboBox
        # self.component_combo = QComboBox(self)
        # self.component_combo.addItem("Choose Component")
        # self.component_combo.addItem("Magnitude")
        # self.component_combo.addItem("Phase")
        # self.component_combo.addItem("Real")
        # self.component_combo.addItem("Imaginary")
        # self.component_combo.setStyleSheet("""
        #     QComboBox {
        #         background-color: #01240e;
        #         color: #ffffff;
        #         border: 1px solid #888888;
        #         border-radius: 5px;
        #         padding: 5px;
        #     }
        #     QComboBox QAbstractItemView {
        #         background: #ffffff;
        #         selection-background-color: #01240e;
        #         selection-color: #ffffff;
        #         border: 1px solid #888888;
        #     }
        # """)
        # self.component_combo.currentIndexChanged.connect(self.plot_fourier)
        # ft_layout.addWidget(self.component_combo)  # Add ComboBox to the vertical layout

        # # FT Image Rectangle
        # self.ft_image_label = QLabel(self)
        # self.ft_image_label.setAlignment(Qt.AlignCenter)
        # self.ft_image_label.setStyleSheet("border-radius: 10px; border: 2px solid #01240e;")
        # self.ft_image_label.setFixedSize(self.width, self.height)  # Same size as the original image label
        # ft_layout.addWidget(self.ft_image_label)  # Add FT image to the vertical layout

        # layout.addLayout(ft_layout)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.type() == QEvent.MouseButtonDblClick:
            self.upload_image()
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

    # def update_image(self):
    #     # Apply the current window/level (brightness/contrast) to the image
    #     if self.image is not None:
    #         adjusted_image = cv2.convertScaleAbs(self.image, alpha=self.contrast, beta=self.brightness)
            
    #         # Convert the adjusted image to QImage for display
    #         height, width = adjusted_image.shape
    #         qimage = QImage(adjusted_image.data, width, height, width, QImage.Format_Grayscale8)
            
    #         # Convert QImage to QPixmap and set it in the QLabel
    #         pixmap = QPixmap.fromImage(qimage)
    #         pixmap = self.get_rounded_pixmap(pixmap, self.original_image_label.size(), self.radius)
    #         self.original_image_label.setPixmap(pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio))
            
    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.bmp)")
        
        if file_path:
            img_bgr = cv2.imread(file_path)
            img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            self.image = img_gray

            # Convert the grayscale image to QImage
            height, width = img_gray.shape
            qimage = QImage(img_gray.data, width, height, width, QImage.Format_Grayscale8)

            # Convert QImage to QPixmap and set it in the QLabel
            pixmap = QPixmap.fromImage(qimage)
            pixmap = self.image_loader.get_rounded_pixmap(pixmap, self.image_loader.image_label.size(), self.radius)
            self.image_loader.image_label.setPixmap(pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio))

            #self.fft()

            self.image_ft.setData(self.image)
            print("doneeeeee in the imageUploader class , MAGNITUDE HERE:")
            print(self.image_ft.magnitude)

    
    # Changing the style of the image to match the size of the rectangle
    # def get_rounded_pixmap(self, pixmap, size, radius):
    #     # Resize the pixmap to fit the QLabel
    #     pixmap = pixmap.scaled(size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

    #     # Create a transparent pixmap with the QLabel's size
    #     rounded_pixmap = QPixmap(size)
    #     rounded_pixmap.fill(Qt.transparent)

    #     # Create a QPainter to draw the rounded pixmap
    #     painter = QPainter(rounded_pixmap)
    #     painter.setRenderHint(QPainter.Antialiasing)
    #     painter.setRenderHint(QPainter.SmoothPixmapTransform)

    #     # Create a rounded rectangle path
    #     path = QPainterPath()
    #     path.addRoundedRect(0, 0, size.width(), size.height(), radius, radius)

    #     # Set the clip path and draw the pixmap
    #     painter.setClipPath(path)
    #     painter.drawPixmap(0, 0, pixmap)
    #     painter.end()

    #     return rounded_pixmap



# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ImageUploader()
#     window.setWindowTitle("Image Upload and Fourier Transform")
#     window.resize(850, 850)  # Resize window to fit both images
#     window.show()
#     sys.exit(app.exec_())
