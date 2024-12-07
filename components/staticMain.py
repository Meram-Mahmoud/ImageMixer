import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFrame, QSpacerItem, QVBoxLayout, QHBoxLayout
from line import Line
from input import Input

class Mixer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mixer")
        self.setGeometry(50, 50, 1800, 900) 
        
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QHBoxLayout(self.centralWidget)

        self.initialize()

    def initialize(self):
        leftLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()

        # Row of inputs
        inputRow1 = QHBoxLayout()
        input1 = Input(parent=self)
        input2 = Input(parent=self)
        ft1 = Input(parent=self)
        ft2 = Input(parent=self)
        inputRow1.addWidget(input1)
        inputRow1.addWidget(ft1)
        inputRow1.addWidget(input2)
        inputRow1.addWidget(ft2)

        # Add inputs and horizontal line to left layout
        leftLayout.addLayout(inputRow1)
        hLine = Line(horizontal=True, parent=self)
        leftLayout.addWidget(hLine)

        inputRow2 = QHBoxLayout()
        input3 = Input(parent=self)
        input4 = Input(parent=self)
        ft3 = Input(parent=self)
        ft4 = Input(parent=self)
        inputRow2.addWidget(input3)
        inputRow2.addWidget(ft3)
        inputRow2.addWidget(input4)
        inputRow2.addWidget(ft4)

        leftLayout.addLayout(inputRow2)

        port1 = Input(parent=self)
        port2 = Input(parent=self)
        rightLayout.addWidget(port1)
        rightLayout.addWidget(port2)

        # Vertical line next to the inputs
        vLine = Line(horizontal=False, parent=self)

        # Add the left layout and vertical line to the main layout
        self.mainLayout.addLayout(leftLayout)
        self.mainLayout.addWidget(vLine)
        self.mainLayout.addLayout(rightLayout)

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
