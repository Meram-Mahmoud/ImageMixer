from PyQt5.QtWidgets import QLabel, QWidget, QComboBox, QVBoxLayout, QRubberBand
from PyQt5.QtGui import QPixmap, QImage, QMouseEvent,QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRect , pyqtSignal
import cv2
import numpy as np


class ROISelectableLabel(QLabel):
    # Signal to send the selected ROI
    regionSelected = pyqtSignal(QRect)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_point = None
        self.end_point = None
        self.rect = QRect()
        self.drawing = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.drawing = True
            self.rect = QRect()

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.end_point = event.pos()
            self.rect = QRect(self.start_point, self.end_point).normalized()
            self.update()  # Trigger a repaint to show the rectangle

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.drawing = False
            self.end_point = event.pos()
            self.rect = QRect(self.start_point, self.end_point).normalized()
            self.update()
            self.regionSelected.emit(self.rect)  # Emit the region for external use

    def paintEvent(self, event):
        """Draw the ROI rectangle."""
        super().paintEvent(event)
        if not self.rect.isNull():
            painter = QPainter(self)
            painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.SolidLine))
            painter.setBrush(QColor(255, 0, 0, 50))  # Semi-transparent red
            painter.drawRect(self.rect)


class FourierTransformViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.width, self.height, self.radius = 250, 350, 15
        self.image = None
        self.magnitude = None
        self.phase = None
        self.real = None
        self.imaginary = None

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
            component = self.magnitude
        elif selected == "Phase":
            component = self.phase
        elif selected == "Real":
            component = self.real
        elif selected == "Imaginary":
            component = self.imaginary
        else:
            return

        self.display_component(component)

    def display_component(self, component):
        """Displays the selected Fourier component."""
        normalized_component = cv2.normalize(component, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        height, width = normalized_component.shape
        qimage_component = QImage(normalized_component.data, width, height, width, QImage.Format_Grayscale8)
        pixmap_component = QPixmap.fromImage(qimage_component)
        self.ft_image_label.setPixmap(pixmap_component.scaled(self.width, self.height, Qt.KeepAspectRatio))

    def get_region_data(self, rect):
        print("benkhosh fe get_region_data")
        """Extracts and saves data within the selected ROI."""
        if self.image is not None and not rect.isNull():
            # Map QRect to image coordinates
            x1 = int(rect.left() * self.image.shape[1] / self.ft_image_label.width())
            x2 = int(rect.right() * self.image.shape[1] / self.ft_image_label.width())
            y1 = int(rect.top() * self.image.shape[0] / self.ft_image_label.height())
            y2 = int(rect.bottom() * self.image.shape[0] / self.ft_image_label.height())

            # Crop the region
            region = self.image[y1:y2, x1:x2]
            print("Region Data:")
            print(region)
            # Save or process `region` as needed
