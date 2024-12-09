from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPainterPath
from PyQt5.QtCore import Qt
import cv2
import numpy as np

class Output(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.width, self.height, self.radius = 250, 350, 15
        self.output_image = None
        self.components = None
        self.port()

    def port(self):
        # Main horizontal layout
        layout = QHBoxLayout(self)

        # Original Image Section
        self.original_image_label = QLabel(self)
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_image_label.setStyleSheet("""border-radius: 10px;
                                                border: 2px solid #11361e;""")
        self.original_image_label.setFixedSize(self.width, self.height)

        layout.addWidget(self.original_image_label)

    def add_image_components(self):
        for comp in self.components:
            if comp is None:
                continue
            if self.output_image is None:
                self.output_image = comp
            else: 
                self.output_image += comp
        self.ifft()
        # print(self.output_image)
    
    def get_rounded_pixmap(self, pixmap, size, radius):
        pixmap = pixmap.scaled(size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        rounded_pixmap = QPixmap(size)
        rounded_pixmap.fill(Qt.transparent)
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, size.width(), size.height(), radius, radius)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        return rounded_pixmap
    
    def set_data(self, new_data):
        self.components = new_data
        self.add_image_components()
        # print(self.components)

    def ifft(self):
        if self.output_image is not None:
            # print(self.output_image)
            phase = np.zeros_like(self.output_image)
            complex_spectrum = self.output_image * np.exp(1j * phase)
            reconstructed_image = np.fft.ifft2(np.fft.ifftshift(complex_spectrum)).real
            reconstructed_image = cv2.normalize(reconstructed_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            # print(reconstructed_image.shape)
            self.dispaly(reconstructed_image)

    def dispaly(self, image):
        height, width = image.shape
        byte_data = image.tobytes()
        qimage = QImage(image.data, width, height, width, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimage)
        pixmap = self.get_rounded_pixmap(pixmap, self.original_image_label.size(), self.radius)
        self.original_image_label.setPixmap(pixmap)