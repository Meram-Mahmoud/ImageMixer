from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

class Input(QWidget):
    def __init__(self,x=0, y=0, width=250, height=350, color="#01240e", parent=None):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.color = color
        self.x = x
        self.y = y
        self.setFixedSize(self.width, self.height)  # Set the size of the rectangle

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = painter.pen()
        pen.setColor(QColor(self.color))  # Border color (e.g., red)
        pen.setWidth(3)  # Border thickness
        painter.setPen(pen)

        painter.drawRect(self.x, self.y, self.width, self.height)  # Draw the rectangle
    