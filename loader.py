from PyQt5.QtWidgets import QLabel, QFileDialog, QWidget
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPainterPath
from PyQt5.QtCore import Qt
import cv2
import numpy as np

class ImageLoader(QWidget):
    def __init__(self, viewport, parent=None):
        super().__init__(parent)

        self.width, self.height, self.radius = 250, 350, 15
        self.image = None
        self.brightness = 0
        self.contrast = 1
        self.is_dragging = False   #not used
        self.viewport=viewport

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.bmp)")
        if file_path:
            img_bgr = cv2.imread(file_path)
            img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            self.image = img_gray

            # Convert to QPixmap for display
            height, width = img_gray.shape
            qimage = QImage(img_gray.data, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qimage)
            pixmap = self.get_rounded_pixmap(pixmap, self.viewport.size(), self.radius)
            self.viewport.setPixmap(pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio))
            return img_gray

    def update_image(self):
        if self.image is not None:
            adjusted_image = cv2.convertScaleAbs(self.image, alpha=self.contrast, beta=self.brightness)
            height, width = adjusted_image.shape
            qimage = QImage(adjusted_image.data, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qimage)
            pixmap = self.get_rounded_pixmap(pixmap, self.viewport.size(), self.radius)
            self.viewport.setPixmap(pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio))

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
