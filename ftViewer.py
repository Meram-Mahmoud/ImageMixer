import logging
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QWidget, QComboBox, QVBoxLayout, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, QRect, pyqtSlot
import cv2
import numpy as np
from region_selector import ROISelectableLabel
from controls import Controls

# # Configure logging
# logging.basicConfig(
#     filename='ImageMixer/Mixer.log', 
#     level=logging.DEBUG, 
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

class FourierTransformViewer(QWidget):
    fourier_image = pyqtSignal(object)
    instances = []  # Class-level list to track all instances

    def __init__(self, parent=None):
        super().__init__(parent)
        logging.debug("Initializing FourierTransformViewer instance.")
        self.width, self.height, self.radius = 250, 350, 15
        self.image = None
        self.magnitude = None
        self.phase = None
        self.real = None
        self.imaginary = None

        # original values
        self.old_magnitude = None
        self.old_phase = None
        self.old_real = None
        self.old_imaginary = None

        self.inner_components = {}
        self.outer_components = {}

        # Inital values
        self.component = self.magnitude
        self.selected = None
        self.mode = "Magnitude/Phase"

        # Fourier component display
        self.ft_image_label = ROISelectableLabel(self)
        self.ft_image_label.setAlignment(Qt.AlignCenter)
        self.ft_image_label.setStyleSheet("border-radius: 10px; border: 2px solid #11361e; background: #cdd1cf;")
        self.ft_image_label.setFixedSize(self.width, self.height)

        # Connect the ROI selection signal to the slot
        self.ft_image_label.regionSelected.connect(self.get_region_data)
        self.ft_image_label.roiChanged.connect(self.propagate_roi)

        FourierTransformViewer.instances.append(self)

        # Create controls
        self.add_slider()
        self.comp_combo()

    def propagate_roi(self, rect: QRect):
        # logging .info("Propagating ROI: %s", rect)
        if self.component is None:
            # logging .warning("No component selected. Skipping ROI propagation.")
            return
        for instance in FourierTransformViewer.instances:
            if instance is not self:
                instance.update_roi(rect)
                instance.get_region_data(rect)

    def update_roi(self, rect: QRect):
        # logging .info("Updating ROI: %s", rect)
        if self.component is None:
            # logging .warning("No component selected. Skipping ROI update.")
            return
        self.ft_image_label.rect = rect
        self.ft_image_label.update()

    def setData(self, original):
        # logging .debug("Setting data for Fourier Transform.")
        self.image = original
        self.compute_fft(self.image)

    def compute_fft(self, image):
        # logging .debug("Computing Fourier Transform.")
        f_transform = np.fft.fft2(image)
        f_shift = np.fft.fftshift(f_transform)
        self.magnitude = np.log1p(np.abs(f_shift))
        self.phase = np.angle(f_shift)
        self.real = np.real(f_shift)
        self.imaginary = np.imag(f_shift)

        # original values => won't change
        self.old_magnitude = np.log1p(np.abs(f_shift))
        self.old_phase = np.angle(f_shift)
        self.old_real = np.real(f_shift)
        self.old_imaginary = np.imag(f_shift)

    def update_ft_view(self):
        # logging .debug("Updating Fourier Transform view.")
        self.selected = self.component_combo.currentText()
        # logging .info("Selected component: %s", self.selected)
        if self.selected == "Magnitude":
            self.component = self.magnitude
        elif self.selected == "Phase":
            self.component = self.phase
        elif self.selected == "Real":
            self.component = self.real
        elif self.selected == "Imaginary":
            self.component = self.imaginary
        else:
            # logging .warning("Invalid selection in combo box.")
            return

        self.display_component(self.component)

    def get_component(self):
        return self.selected

    def display_component(self, component):
        # logging .debug("Displaying selected Fourier component.")
        normalized_component = cv2.normalize(component, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        height, width = normalized_component.shape
        qimage_component = QImage(normalized_component.data, width, height, width, QImage.Format_Grayscale8)
        pixmap_component = QPixmap.fromImage(qimage_component)

        rounded_pixmap = QPixmap(self.width, self.height)
        rounded_pixmap.fill(Qt.transparent)
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.black)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width, self.height, self.radius, self.radius)
        painter.end()

        pixmap_component = pixmap_component.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pixmap_component.setMask(rounded_pixmap.mask())

        self.ft_image_label.setPixmap(pixmap_component)
        self.ft_image_label.setPixmap(pixmap_component.scaled(self.width, self.height, Qt.KeepAspectRatio))

    def get_region_data(self, rect):
        # logging .debug("Extracting region data for ROI: %s", rect)
        if self.image is not None and not rect.isNull() and self.component is not None:
            x1 = int(rect.left() * self.component.shape[1] / self.ft_image_label.width())
            x2 = int(rect.right() * self.component.shape[1] / self.ft_image_label.width())
            y1 = int(rect.top() * self.component.shape[0] / self.ft_image_label.height())
            y2 = int(rect.bottom() * self.component.shape[0] / self.ft_image_label.height())

            inner_magnitude = np.zeros_like(self.magnitude)
            inner_phase = np.zeros_like(self.phase)
            inner_real = np.zeros_like(self.real)
            inner_imaginary = np.zeros_like(self.imaginary)

            inner_magnitude[y1:y2, x1:x2] = self.magnitude[y1:y2, x1:x2]
            inner_phase[y1:y2, x1:x2] = self.phase[y1:y2, x1:x2]
            inner_real[y1:y2, x1:x2] = self.real[y1:y2, x1:x2]
            inner_imaginary[y1:y2, x1:x2] = self.imaginary[y1:y2, x1:x2]

            self.inner_components = {
                "magnitude": inner_magnitude,
                "phase": inner_phase,
                "real": inner_real,
                "imaginary": inner_imaginary
            }

            # logging .info("Inner components extracted.")

            outer_magnitude = np.copy(self.magnitude)
            outer_magnitude[y1:y2, x1:x2] = 0

            outer_phase = np.copy(self.phase)
            outer_phase[y1:y2, x1:x2] = 0

            outer_real = np.copy(self.real)
            outer_real[y1:y2, x1:x2] = 0

            outer_imaginary = np.copy(self.imaginary)
            outer_imaginary[y1:y2, x1:x2] = 0

            self.outer_components = {
                "magnitude": outer_magnitude,
                "phase": outer_phase,
                "real": outer_real,
                "imaginary": outer_imaginary
            }

            # logging .info("Outer components extracted.")

    def get_roi(self):
        return self.inner_components, self.outer_components

    def add_slider(self):
        # logging .debug("Adding slider for intensity adjustment.")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(100)
        self.slider.setTickInterval(10)
        self.slider.setStyleSheet("""
            QSlider::handle:horizontal {
                background-color: #3c7551;
                width: 20px;
                height: 20px;
                border-radius: 10px;
                margin-top: -8px;
                margin-bottom: -8px;
            }
            QSlider::groove:horizontal {
                height: 5px;
                background: white;
            }
            QSlider::sub-page:horizontal {
                background: #11361e;
            }
        """)

        self.slider.valueChanged.connect(self.update_slider_value)

    def update_slider_value(self):
        # logging .debug("Updating slider value.")
        self.magnitude = self.old_magnitude * self.slider.value()/100
        self.phase = self.old_phase * self.slider.value()/100
        self.real = self.old_real * self.slider.value()/100
        self.imaginary = self.old_imaginary * self.slider.value()/100

    def comp_combo(self):
        # logging .debug("Initializing ComboBox for Fourier components.")
        # ComboBox for selecting Fourier components
        self.component_combo = QComboBox(self)
        self.component_combo.addItem("Choose Component")
        # logging .debug("Added default ComboBox item: 'Choose Component'.")

        # self.update_fourier_options()
        if self.mode == "Magnitude/Phase":
            # logging .debug("Magnitude/Phase mode.")
            self.component_combo.addItem("Magnitude")
            self.component_combo.addItem("Phase")
        else: 
            # logging .debug("Real/Imaginary mode.")
            self.component_combo.addItem("Real")
            self.component_combo.addItem("Imaginary")

        self.component_combo.setStyleSheet("""
            QComboBox {
                background-color: #11361e;
                color: #ffffff;
                border: 1px solid #888888;
                border-radius: 5px;
                padding: 5px;
                font-size: 18px;
            }
            QComboBox QAbstractItemView {
                background-color: #cdd1cf;
                border: 1px solid #888888;
                selection-background-color: #3c7551; /* Background color for selected item */
                selection-color: #ffffff; /* Text color for selected item */
            }
        """)
        # logging .debug("Set ComboBox stylesheet.")

        self.component_combo.currentIndexChanged.connect(self.update_ft_view)
        # logging .debug("Connected ComboBox currentIndexChanged signal to update_ft_view method.")

    def update_fourier_options(self, mode):
        self.mode = mode
        if self.mode == "Real/Imaginary":
            self.component_combo.clear()
            self.component_combo.addItems(["Choose Component", "Real", "Imaginary"])
        elif self.mode == "Magnitude/Phase":
            self.component_combo.clear()
            self.component_combo.addItems(["Choose Component", "Magnitude", "Phase"])