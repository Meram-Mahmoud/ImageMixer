from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QMouseEvent, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRect, pyqtSignal, QPoint

class ROISelectableLabel(QLabel):
    # Signal to send the selected ROI
    regionSelected = pyqtSignal(QRect)
    roiChanged = pyqtSignal(QRect)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_point = None
        self.end_point = None
        self.rect = QRect()
        self.drawing = False
        self.resizing = False
        self.selected_handle = None
        self.handle_size = 10  # Size of the resizing handles
        self.moving = False  # Flag for moving the rectangle
        self.offset = QPoint()  # Offset for dragging

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()

            # Check if the user clicked on a resizing handle
            for handle, rect in self.get_handles().items():
                if rect.contains(event.pos()):
                    self.selected_handle = handle
                    self.resizing = True
                    return

            # Check if the user clicked inside the rectangle
            if self.rect.contains(event.pos()):
                self.moving = True
                # Calculate offset between mouse position and rectangle's top-left corner
                self.offset = event.pos() - self.rect.topLeft()
                return

            # Otherwise, start drawing a new rectangle
            self.drawing = True
            self.rect = QRect(self.start_point, self.start_point)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.resizing and self.selected_handle:
            self.resize_rect(event.pos())
            self.roiChanged.emit(self.rect) 
        elif self.moving:
            # Calculate new top-left position considering the offset
            new_top_left = event.pos() - self.offset
            self.move_rect(new_top_left)
            self.roiChanged.emit(self.rect) 
        elif self.drawing:
            self.end_point = event.pos()
            self.rect = QRect(self.start_point, self.end_point).normalized()
        self.update()  # Trigger a repaint to show updates

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            if self.drawing:
                self.drawing = False
                self.end_point = event.pos()
                self.rect = QRect(self.start_point, self.end_point).normalized()
                self.regionSelected.emit(self.rect)  # Emit the selected region
            elif self.resizing:
                self.resizing = False
                self.selected_handle = None
            elif self.moving:
                self.moving = False

            self.roiChanged.emit(self.rect)
            self.update()

    def paintEvent(self, event):
        """Draw the ROI rectangle and resizing handles."""
        super().paintEvent(event)
        if not self.rect.isNull():
            painter = QPainter(self)

            # Draw the rectangle
            painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.SolidLine))
            painter.setBrush(QColor(255, 0, 0, 50))  # Semi-transparent red
            painter.drawRect(self.rect)

            # Draw resizing handles
            for rect in self.get_handles().values():
                painter.setBrush(QColor(255, 0, 0))  # Red handles
                painter.setPen(Qt.NoPen)
                painter.drawRect(rect)

    def get_handles(self):
        """Calculate the positions of the resizing handles."""
        x1, y1, x2, y2 = self.rect.left(), self.rect.top(), self.rect.right(), self.rect.bottom()
        size = self.handle_size

        # Handles: corners and midpoints of edges
        handles = {
            'top-left': QRect(x1 - size // 2, y1 - size // 2, size, size),
            'top-right': QRect(x2 - size // 2, y1 - size // 2, size, size),
            'bottom-left': QRect(x1 - size // 2, y2 - size // 2, size, size),
            'bottom-right': QRect(x2 - size // 2, y2 - size // 2, size, size),
            'top': QRect((x1 + x2) // 2 - size // 2, y1 - size // 2, size, size),
            'bottom': QRect((x1 + x2) // 2 - size // 2, y2 - size // 2, size, size),
            'left': QRect(x1 - size // 2, (y1 + y2) // 2 - size // 2, size, size),
            'right': QRect(x2 - size // 2, (y1 + y2) // 2 - size // 2, size, size),
        }
        return handles

    def resize_rect(self, pos: QPoint):
        """Resize the rectangle based on the dragged handle."""
        if self.selected_handle == 'top-left':
            self.rect.setTopLeft(pos)
        elif self.selected_handle == 'top-right':
            self.rect.setTopRight(pos)
        elif self.selected_handle == 'bottom-left':
            self.rect.setBottomLeft(pos)
        elif self.selected_handle == 'bottom-right':
            self.rect.setBottomRight(pos)
        elif self.selected_handle == 'top':
            self.rect.setTop(pos.y())
        elif self.selected_handle == 'bottom':
            self.rect.setBottom(pos.y())
        elif self.selected_handle == 'left':
            self.rect.setLeft(pos.x())
        elif self.selected_handle == 'right':
            self.rect.setRight(pos.x())

        # Ensure the rectangle stays normalized
        self.rect = self.rect.normalized()
        self.regionSelected.emit(self.rect)

    def move_rect(self, new_top_left):
        """Move the rectangle to the new top-left position."""
        rect_size = self.rect.size()  # Get the size of the rectangle
        self.rect.setTopLeft(new_top_left)  # Set the top-left corner
        self.rect.setSize(rect_size)  # Adjust the size
        self.update()  # Trigger a repaint to reflect changes visually
        self.regionSelected.emit(self.rect)  # Emit the updated region
