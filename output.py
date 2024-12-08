import sys
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

        self.port()

    def port(self):
        # Main horizontal layout
        layout = QHBoxLayout(self)

        # Original Image Section
        self.original_image_label = QLabel(self)
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_image_label.setStyleSheet("border-radius: 10px; border: 2px solid #01240e;")
        self.original_image_label.setFixedSize(self.width, self.height)

        layout.addWidget(self.original_image_label)

    def add_image_components(self, component):
        if self.output_image is None:
            self.output_image = component
        else: 
            self.output_image += component
    
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
    
