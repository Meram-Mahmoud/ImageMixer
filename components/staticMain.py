from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

class Square(QWidget):
    def __init__(self, size=100, color="#73917b", parent=None):
        super().__init__(parent)
        self.size = size
        self.color = color
        self.setFixedSize(self.size, self.size)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(self.color))
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, self.size, self.size)

class Line(QFrame):
    def __init__(self, horizontal=True, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #000;")
        if horizontal:
            self.setFixedHeight(2)
        else:
            self.setFixedWidth(2)

class Mixer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mixer")
        self.setGeometry(50, 50, 800, 600)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QHBoxLayout(self.centralWidget)  # Main horizontal layout
        self.createLeftColumn()
        self.addVerticalLine()  # Add the vertical line
        self.createRightColumn()

    def createLeftColumn(self):
        leftColumn = QVBoxLayout()

        # Create the top row
        topRow = self.createRow()
        leftColumn.addLayout(topRow)

        # Add a horizontal line
        hLine = Line(horizontal=True, parent=self)
        leftColumn.addWidget(hLine)

        # Create the bottom row
        bottomRow = self.createRow()
        leftColumn.addLayout(bottomRow)

        # Add the left column to the main layout
        self.mainLayout.addLayout(leftColumn, 3)  # Weight = 2 (for unequal columns)

    def addVerticalLine(self):
        vLine = Line(horizontal=False, parent=self)  # Create a vertical line
        self.mainLayout.addWidget(vLine)

    def createRightColumn(self):
        rightColumn = QVBoxLayout()

        # Add two squares to the right column
        rightColumn.addWidget(Square(parent=self))
        rightColumn.addWidget(Square(parent=self))

        # Add the right column to the main layout
        self.mainLayout.addLayout(rightColumn, 1)  # Weight = 1 (for unequal columns)

    def createRow(self):
        rowLayout = QHBoxLayout()
        for _ in range(4):  # Add 4 squares in a row
            rowLayout.addWidget(Square(parent=self))
        return rowLayout

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Mixer()
    window.show()
    sys.exit(app.exec_())
