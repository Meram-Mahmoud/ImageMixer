from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QWidget, QComboBox, QVBoxLayout, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, QRect
import cv2
import numpy as np
from region_selector import ROISelectableLabel
from controls import Controls

class FourierTransformViewer(QWidget):
    fourier_image = pyqtSignal(object)
    instances = []  # Class-level list to track all instances

    def __init__(self, parent=None):
        super().__init__(parent)
        self.width, self.height, self.radius = 250, 350, 15
        self.image = None
        self.magnitude = None
        self.phase = None
        self.real = None
        self.imaginary = None
        self.inner_components = {}
        self.outer_components = {}

        # Inital values
        self.component= self.magnitude
        self.selected = None
        self.mode = 'mp'
        Controls.staticMetaObject.connectSlotsByName(self)

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
        """Update all other instances with the new ROI."""
        if self.component is None:
            return  # Skip instances with no component
        for instance in FourierTransformViewer.instances:
            if instance is not self:
                instance.update_roi(rect)
                instance.get_region_data(rect)

    def update_roi(self, rect: QRect):
        """Update the ROI of the current instance."""
        if self.component is None:
            return  # Skip instances with no component
        self.ft_image_label.rect = rect
        self.ft_image_label.update()

    def setData(self, original):
        self.image=original
        # print("setting the data before fourier, IMAGE:")
        # print(self.image)
        self.compute_fft(self.image)

    def compute_fft(self, image):
        # if image.any():
            """Computes Fourier Transform of the input image."""
            f_transform = np.fft.fft2(image)
            f_shift = np.fft.fftshift(f_transform)
            self.magnitude = np.log1p(np.abs(f_shift))
            self.phase = np.angle(f_shift)
            self.real = np.real(f_shift)
            self.imaginary = np.imag(f_shift)
            # print("setting the data after fourier, MAGNITUDE:")
            # print(self.magnitude)
            # self.display_component(self.component)

            self.fourier_image.emit([self.magnitude, self.phase, self.real, self.imaginary])

    def update_ft_view(self):
        """Updates the Fourier component display based on user selection."""
        # if not self.image:
        #     return

        self.selected = self.component_combo.currentText()
        if self.selected == "Magnitude":
            self.component = self.magnitude
        elif self.selected == "Phase":
            self.component = self.phase
        elif self.selected == "Real":
            self.component = self.real
        elif self.selected == "Imaginary":
            self.component = self.imaginary
        else:
            return

        self.display_component(self.component)

    def get_component(self):
        return self.selected

    def display_component(self, component):
        """Displays the selected Fourier component with rounded corners."""
        # Normalize the component to 8-bit grayscale
        normalized_component = cv2.normalize(component, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        height, width = normalized_component.shape
        qimage_component = QImage(normalized_component.data, width, height, width, QImage.Format_Grayscale8)
        pixmap_component = QPixmap.fromImage(qimage_component)

        # Create a rounded mask
        rounded_pixmap = QPixmap(self.width, self.height)
        rounded_pixmap.fill(Qt.transparent)  # Transparent background
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.black)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width, self.height, self.radius, self.radius)
        painter.end()

        # Apply the mask to the pixmap
        pixmap_component = pixmap_component.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pixmap_component.setMask(rounded_pixmap.mask())

        # Set the rounded pixmap to the QLabel
        self.ft_image_label.setPixmap(pixmap_component)
        self.ft_image_label.setPixmap(pixmap_component.scaled(self.width, self.height, Qt.KeepAspectRatio))

    def get_region_data(self, rect):
        """Extracts and saves data within the selected ROI or outside the selected ROI."""
        if self.image is not None and not rect.isNull():
            # Map QRect to image coordinates
            x1 = int(rect.left() * self.component.shape[1] / self.ft_image_label.width())
            x2 = int(rect.right() * self.component.shape[1] / self.ft_image_label.width())
            y1 = int(rect.top() * self.component.shape[0] / self.ft_image_label.height())
            y2 = int(rect.bottom() * self.component.shape[0] / self.ft_image_label.height())

            # Create copies of the original arrays
            inner_magnitude = np.zeros_like(self.magnitude)
            inner_phase = np.zeros_like(self.phase)
            inner_real = np.zeros_like(self.real)
            inner_imaginary = np.zeros_like(self.imaginary)

            # Retain the values within the rectangle and zero out everything else
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

            #ACCESSING AND PRINTING
            # if "magnitude" in self.inner_components:
            print("Inner Magnitude:")
            print(self.inner_components["magnitude"])
            # else:
            #     print("Inner magnitude data not available.")


            # Extract the outer region (everything except inside the rectangle)
            outer_magnitude = np.copy(self.magnitude)  # Create a copy of the entire image
            # Set the area inside the rectangle to 0 (black or empty)
            outer_magnitude[y1:y2, x1:x2] = 0

            outer_phase = np.copy(self.phase)  # Create a copy of the entire image
            outer_phase[y1:y2, x1:x2] = 0

            outer_real = np.copy(self.real)  # Create a copy of the entire image
            outer_real[y1:y2, x1:x2] = 0

            outer_imaginary = np.copy(self.imaginary)  # Create a copy of the entire image
            outer_imaginary[y1:y2, x1:x2] = 0

            self.outer_components = {
            "magnitude": outer_magnitude,
            "phase": outer_phase,
            "real": outer_real,
            "imaginary": outer_imaginary
            }
            # print("Outer MAG:")
            # print(self.outer_components["magnitude"])
            # print("Outer PHASE:")
            # print(self.outer_components["phase"])
            # print("Outer REAL:")
            # print(self.outer_components["real"])
            # print("Outer IMAG:")
            # print(self.outer_components["imaginary"])
            
    def get_roi(self):
        return self.inner_components, self.outer_components

    def add_slider(self):
        self.slider = QSlider(Qt.Horizontal)  # Horizontal slider
        self.slider.setMinimum(0)  # Minimum value
        self.slider.setMaximum(100)  # Maximum value
        self.slider.setValue(100)  # Initial value
        # self.slider.setTickPosition(QSlider.TicksBelow)  # Show ticks below the slider
        self.slider.setTickInterval(10)  # Interval between ticks
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

        # self.slider.valueChanged.connect(self.update_slider_value)

    # def update_slider_value(self):
    #     # Update the value label when the slider value changes
    #     self.slider_value_label.setText(f"{self.slider.value()}")        
    
    # not used
    def set_mode(self, mode):
        self.mode = mode

    def comp_combo(self):
        # ComboBox for selecting Fourier components
        self.component_combo = QComboBox(self)
        self.component_combo.addItem("Choose Component")
        if self.mode == 'mp':
            self.component_combo.addItem("Magnitude")
            self.component_combo.addItem("Phase")
        # else: 
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
        self.component_combo.currentIndexChanged.connect(self.update_ft_view)

