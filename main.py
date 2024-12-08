import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFrame, QSpacerItem, QVBoxLayout, QHBoxLayout
from imageLoader import ImageUploader
from components.line import Line
from components.input import Input
from output import Output

class Mixer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mixer")
        self.setGeometry(50, 50, 1800, 900) 

        self.centralWidget = QWidget(self)
        self.centralWidget.setStyleSheet("background-color: #cdd1cf;")
        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QHBoxLayout(self.centralWidget)  # Main horizontal layout
        self.createLeftColumn()
        self.addVerticalLine()  # Add the vertical line
        self.createRightColumn()
    
    def createLeftColumn(self):
        leftColumn = QVBoxLayout()

        # Create the top row
        topRow = QHBoxLayout()
        image_uploader1 = ImageUploader()
        image_uploader2 = ImageUploader()
        topRow.addWidget(image_uploader1)
        topRow.addWidget(image_uploader2)
        leftColumn.addLayout(topRow)

        # Add a horizontal line
        hLine = Line(horizontal=True, parent=self)
        leftColumn.addWidget(hLine)

        # Create the bottom row
        bottomRow = QHBoxLayout()
        image_uploader3 = ImageUploader()
        image_uploader4 = ImageUploader()
        bottomRow.addWidget(image_uploader3)
        bottomRow.addWidget(image_uploader4)
        leftColumn.addLayout(bottomRow)

        # Add the left column to the main layout
        self.mainLayout.addLayout(leftColumn, 2)  # Weight = 2 (for unequal columns)
    
    def addVerticalLine(self):
        vLine = Line(horizontal=False, parent=self)  # Create a vertical line
        self.mainLayout.addWidget(vLine)

    def createRightColumn(self):
        rightColumn = QVBoxLayout()

        # Output ports
        port1 = Output()
        port2 = Output()
        rightColumn.addWidget(port1)
        rightColumn.addWidget(port2)

        # Add the right column to the main layout
        self.mainLayout.addLayout(rightColumn, 1)  # Weight = 1 (for unequal columns)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mixer()
    window.show()
    sys.exit(app.exec_())
