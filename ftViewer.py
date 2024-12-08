from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QWidget, QComboBox, QVBoxLayout
from PyQt5.QtCore import Qt
import cv2
import numpy as np
from region_selector import ROISelectableLabel


class FourierTransformViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.width, self.height, self.radius = 250, 350, 15
        self.image = None
        self.magnitude = None
        self.phase = None
        self.real = None
        self.imaginary = None
        self.component=None

        # ComboBox for selecting Fourier components
        self.component_combo = QComboBox(self)
        self.component_combo.addItem("Choose Component")
        self.component_combo.addItem("Magnitude")
        self.component_combo.addItem("Phase")
        self.component_combo.addItem("Real")
        self.component_combo.addItem("Imaginary")
        self.component_combo.setStyleSheet("""
            QComboBox {
                background-color: #01240e;
                color: #ffffff;
                border: 1px solid #888888;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        # Fourier component display
        self.ft_image_label = ROISelectableLabel(self)
        self.ft_image_label.setAlignment(Qt.AlignCenter)
        self.ft_image_label.setStyleSheet("border-radius: 10px; border: 2px solid #01240e;")
        self.ft_image_label.setFixedSize(self.width, self.height)

        # Connect the ROI selection signal to the slot
        self.ft_image_label.regionSelected.connect(self.get_region_data)

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.component_combo)
        layout.addWidget(self.ft_image_label)

        # Connections
        self.component_combo.currentIndexChanged.connect(self.update_ft_view)

    def setData(self, original):
        self.image=original
        print("setting the data before fourier, IMAGE:")
        print(self.image)
        self.compute_fft(self.image)

    def compute_fft(self, image):
        """Computes Fourier Transform of the input image."""
        f_transform = np.fft.fft2(image)
        f_shift = np.fft.fftshift(f_transform)
        self.magnitude = np.log1p(np.abs(f_shift))
        self.phase = np.angle(f_shift)
        self.real = np.real(f_shift)
        self.imaginary = np.imag(f_shift)
        print("setting the data after fourier, MAGNITUDE:")
        print(self.magnitude)

    def update_ft_view(self):
        """Updates the Fourier component display based on user selection."""
        # if not self.image:
        #     return

        selected = self.component_combo.currentText()
        if selected == "Magnitude":
            self.component = self.magnitude
        elif selected == "Phase":
            self.component = self.phase
        elif selected == "Real":
            self.component = self.real
        elif selected == "Imaginary":
            self.component = self.imaginary
        else:
            return

        self.display_component(self.component)

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

    def get_region_data(self, rect, region_type='inner'):
        """Extracts and saves data within the selected ROI or outside the selected ROI."""
        if self.image is not None and not rect.isNull():
            # Map QRect to image coordinates
            x1 = int(rect.left() * self.component.shape[1] / self.ft_image_label.width())
            x2 = int(rect.right() * self.component.shape[1] / self.ft_image_label.width())
            y1 = int(rect.top() * self.component.shape[0] / self.ft_image_label.height())
            y2 = int(rect.bottom() * self.component.shape[0] / self.ft_image_label.height())

            # Extract data based on region_type
            if region_type == 'inner':
                # Crop the region inside the rectangle (inner region)
                region = self.component[y1:y2, x1:x2]
                print("Inner Region Data:")
                print(region)
            elif region_type == 'outer':
                # Extract the outer region (everything except inside the rectangle)
                outer_region = np.copy(self.component)  # Create a copy of the entire image

                # Set the area inside the rectangle to 0 (black or empty)
                outer_region[y1:y2, x1:x2] = 0

                print("Outer Region Data:")
                print(outer_region)
                region = outer_region  # Return the outer region data

            # Save or process the region as needed
            return region

