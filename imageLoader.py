import sys
from PyQt5.QtWidgets import QApplication, QLabel, QFileDialog, QHBoxLayout, QWidget, QComboBox, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QEvent
import cv2
from ftViewer import FourierTransformViewer
from loader import ImageLoader

class ImageUploader(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.width, self.height, self.radius = 250, 350, 15

        # Variables for brightness and contrast control
        self.brightness = 0  # Starting brightness (no change)
        self.contrast = 1    # Starting contrast (no change)
        self.is_dragging = False  # To track mouse dragging

        self.image = None
        self.image_ft = FourierTransformViewer()

        # Main vertical layout
        main_column = QVBoxLayout(self)

        # Create the upper and lower row layouts
        upper_row = QHBoxLayout()
        lower_row = QHBoxLayout()

        # Original Image Section
        self.original_image_label = QLabel(self)
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_image_label.setStyleSheet("border-radius: 10px; border: 2px solid #11361e;")
        self.original_image_label.setFixedSize(self.width, self.height)
        pixmap = QPixmap("ImageMixer/icons/coloredUpload.png")
        self.original_image_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio)) 
        self.image_loader = ImageLoader(self.original_image_label)

        # Add components to upper_row
        upper_row.addWidget(self.image_ft.slider, 1)
        upper_row.addSpacing(40)
        upper_row.addWidget(self.image_ft.component_combo, 1)

        # Container widget for the upper_row layout
        container_widget = QWidget(self)
        container_widget.setLayout(upper_row)
        container_widget.setFixedWidth(570)  # Set the desired width

        # Add original image and transformed image to lower_row
        lower_row.addWidget(self.original_image_label)
        lower_row.addWidget(self.image_ft.ft_image_label)

        # Add the container_widget and lower_row to the main layout
        main_column.addWidget(container_widget, alignment=Qt.AlignHCenter)
        main_column.addLayout(lower_row)

        # Set the layout for the main window
        self.setLayout(main_column)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.type() == QEvent.MouseButtonDblClick:
            self.image = self.image_loader.upload_image()
            self.image_ft.setData(cv2.resize(self.image, (self.width, self.height)))
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

            self.image_ft.setData(self.image)

    def get_component(self):
        return self.image_ft.magnitude


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ImageUploader()
#     window.setWindowTitle("Image Upload and Fourier Transform")
#     window.resize(850, 850)  # Resize window to fit both images
#     window.show()
#     sys.exit(app.exec_())
