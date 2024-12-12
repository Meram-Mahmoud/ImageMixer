from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPainterPath
from PyQt5.QtCore import Qt
import cv2
import numpy as np

class Output(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.width, self.height, self.radius = 250, 350, 15

        self.output_image_real = None
        self.output_image_img = None
        self.output_image_mag = None
        self.output_image_phase = None

        self.components = None
        self.mode = None
        self.port()

    def port(self):
        # Main horizontal layout
        layout = QHBoxLayout(self)

        # Original Image Section
        self.original_image_label = QLabel(self)
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_image_label.setStyleSheet("""border-radius: 10px;
                                                border: 2px solid #11361e;
                                                background: #cdd1cf;""")
        self.original_image_label.setFixedSize(self.width, self.height)

        layout.addWidget(self.original_image_label)

    def add_image_components(self):
        print(self.components)
        if self.mode == 'mp':
            for comp in self.components:
                if 'magnitude' in comp and 'phase' in comp:
                    if self.output_image_mag is None:
                        self.output_image_mag = comp['magnitude']
                    else:
                        self.output_image_mag += comp['magnitude']

                    if self.output_image_phase is None:
                        self.output_image_phase = comp['phase']
                    else:
                        self.output_image_phase += comp['phase']
        else: 
            for comp in self.components:
                if 'real' in comp and 'imaginary' in comp:
                    if self.output_image_real is None:
                        self.output_image_real = comp["real"]
                    else:
                        self.output_image_real += comp["real"]
                    
                    if self.output_image_img is None:
                        self.output_image_img = comp["imaginary"]
                    else:
                        self.output_image_img += comp["imaginary"]
        
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
    
    def set_data(self, new_data, mode):
        self.output_image_real = None
        self.output_image_img = None
        self.output_image_mag = None
        self.output_image_phase = None
        self.components = new_data
        self.mode = mode
        self.add_image_components()
        # print(self.components)

    def ifft(self):
        # Phase/Magnitude mode
        if self.mode == 'mp':
            # print(self.output_image)
            if self.output_image_phase is None:
                self.output_image_phase = np.zeros_like(self.output_image_mag)
            elif self.output_image_mag is None:
                self.output_image_mag = np.zeros_like(self.output_image_phase)

            complex_spectrum = self.output_image_mag * np.exp(1j * self.output_image_phase)
            reconstructed_image = np.fft.ifft2(np.fft.ifftshift(complex_spectrum)).real
            reconstructed_image = cv2.normalize(reconstructed_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            # print(reconstructed_image.shape)
            
        # Real/Imaginary mode
        else:
            if self.output_image_img is None:
                self.output_image_img = np.zeros_like(self.output_image_real)
            if self.output_image_real is None:
                self.output_image_real = np.zeros_like(self.output_image_img)

            total_elements = self.output_image_real + self.output_image_img
            reconstructed_image = np.fft.ifft2(total_elements)
            reconstructed_image = np.abs(reconstructed_image)

        self.display(reconstructed_image)

    def display(self, image):
        height, width = image.shape
        byte_data = image.tobytes()
        qimage = QImage(image.data, width, height, width, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimage)
        pixmap = self.get_rounded_pixmap(pixmap, self.original_image_label.size(), self.radius)
        self.original_image_label.setPixmap(pixmap)