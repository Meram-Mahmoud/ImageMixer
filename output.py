import logging
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPainterPath
from PyQt5.QtCore import Qt
import cv2
import numpy as np
from scipy.fft import ifft2, ifftshift

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ImageMixer/logging/output_widget.log"),
        logging.StreamHandler()
    ]
)

class Output(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.width, self.height, self.radius = 250, 350, 15

        self.output_image_real = None
        self.output_image_img = None
        self.output_image_mag = None
        self.output_image_phase = None

        self.components = None
        self.mode = None
        self.selected_comp = None
        logging.info("Output widget initialized")
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
        logging.info("Port initialized with original image label")
        
    def add_image_components(self):
        logging.debug("Adding image components with mode: %s", self.mode)
        try:
            if self.mode == 'mp':
                for comp, item in zip(self.components, self.selected_comp):
                    if 'magnitude' in comp and 'phase' in comp:
                        if item == "Magnitude":
                            if self.output_image_mag is None:
                                self.output_image_mag = comp['magnitude']
                            else:
                                self.output_image_mag += comp['magnitude']
                        elif item == "Phase":
                            if self.output_image_phase is None:
                                self.output_image_phase = comp['phase']
                            else:
                                self.output_image_phase += comp['phase']
                                self.output_image_phase = (self.output_image_phase + np.pi) % (2 * np.pi) - np.pi
                        else: 
                            logging.warning("Unsupported item: %s", item)
            else: 
                for comp, item in zip(self.components, self.selected_comp):
                    if 'real' in comp and 'imaginary' in comp:
                        if item == "Real":
                            if self.output_image_real is None:
                                self.output_image_real = comp["real"]
                            else:
                                self.output_image_real += comp["real"]
                        elif item == "Imaginary":
                            if self.output_image_img is None:
                                self.output_image_img = comp["imaginary"]
                            else:
                                self.output_image_img += comp["imaginary"]
                        else: 
                            logging.warning("Unsupported item: %s", item)
            self.ifft()
        except Exception as e:
            logging.error("Error in add_image_components: %s", e)
    
    def get_rounded_pixmap(self, pixmap, size, radius):
        logging.debug("Generating rounded pixmap")
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

    def set_data(self, new_data, mode, comp):
        logging.info("Setting data with mode: %s", mode)
        self.output_image_real = None
        self.output_image_img = None
        self.output_image_mag = None
        self.output_image_phase = None
        self.components = new_data
        self.mode = mode
        self.selected_comp = comp
        self.add_image_components()

    def ifft(self):
        logging.debug("Performing inverse FFT")
        try:
            if self.mode == 'mp':  # Magnitude-Phase mode
                if self.output_image_mag is None:
                    self.output_image_mag = np.ones_like(self.output_image_phase)
                if self.output_image_phase is None:
                    self.output_image_phase = np.ones_like(self.output_image_mag)

                complex_spectrum = self.output_image_mag * np.exp(1j * self.output_image_phase)
                reconstructed_image = ifft2(ifftshift(complex_spectrum)).real

            elif self.mode == 'ri':  # Real-Imaginary mode
                if self.output_image_real is None:
                    self.output_image_real = np.zeros_like(self.output_image_img)
                if self.output_image_img is None:
                    self.output_image_img = np.zeros_like(self.output_image_real)

                complex_spectrum = self.output_image_real + 1j * self.output_image_img
                reconstructed_image = np.abs(ifft2(ifftshift(complex_spectrum)))
            
            reconstructed_image = cv2.normalize(reconstructed_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            self.display(reconstructed_image)

        except Exception as e:
            logging.error("Error in ifft: %s", e)


    def display(self, image):
        logging.debug("Displaying image")
        try:
            height, width = image.shape
            byte_data = image.tobytes()
            qimage = QImage(image.data, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qimage)
            pixmap = self.get_rounded_pixmap(pixmap, self.original_image_label.size(), self.radius)
            self.original_image_label.setPixmap(pixmap)
            logging.info("Image displayed successfully")
        except Exception as e:
            logging.error("Error in display: %s", e)
