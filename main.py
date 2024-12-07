import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFrame, QSpacerItem, QVBoxLayout
from imageLoader import ImageUploader

class Mixer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mixer")
        self.setGeometry(50, 50, 1800, 900) 

        self.mainLayout = QMainWindow()
        # self.setStyleSheet()

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QVBoxLayout(self.centralWidget)

        self.initialize()

    def initialize(self):
        image_uploader1 = ImageUploader(self.centralWidget)
        image_uploader1.setFixedSize(540, 400)
        image_uploader1.move(20, 20)
        
        image_uploader2 = ImageUploader(self.centralWidget)
        image_uploader2.setFixedSize(540, 400)
        image_uploader2.move(570, 20)

        self.vLine()

        image_uploader3 = ImageUploader(self.centralWidget)
        image_uploader3.setFixedSize(540, 400)
        image_uploader3.move(20, 400)

        image_uploader4 = ImageUploader(self.centralWidget)
        image_uploader4.setFixedSize(540, 400)
        image_uploader4.move(570, 400)

    def vLine(self):
        horizontal_line = QFrame(self.centralWidget)
        horizontal_line.setStyleSheet("QFrame { background-color: #73917b; width: 2px; border: none; }")
        horizontal_line.setGeometry(1400, 20, 2, 900)
        horizontal_line.show()
        
    def createUI(self):
        # self.createUIElements()
        # self.setUI()
        # self.connectUI()
        # self.makeLayout()
        # self.stylingUI()
        # centralWidget = QWidget()
        # centralWidget.setLayout(self.mainLayout)
        # self.setCentralWidget(centralWidget)
        # self.centerWindow()
        pass

    def createUIElements(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mixer()
    window.show()
    sys.exit(app.exec_())
