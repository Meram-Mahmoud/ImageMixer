import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout
from imageLoader import ImageUploader
from components.line import Line
from output import Output
from mix import Mix
from PyQt5.QtCore import Qt
from controls import Controls

class Mixer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mixer")
        self.setGeometry(50, 50, 1800, 900)

        self.centralWidget = QWidget(self)
        self.centralWidget.setStyleSheet("background-color: #11361e;")
        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QHBoxLayout(self.centralWidget)  # Main horizontal layout
        self.createLeftColumn()
        # self.addVerticalLine()  # Add the vertical line
        self.createRightColumn()
    
    def createLeftColumn(self):
        leftColumn = QVBoxLayout()

        # Create the top row
        topRow = QHBoxLayout()
        self.image_uploader1 = ImageUploader()
        self.image_uploader2 = ImageUploader()
        topRow.addWidget(self.image_uploader1)
        topRow.addWidget(self.image_uploader2)
        # leftColumn.addLayout(topRow)

        # Create a QWidget to hold the left column layout and set the border
        topRowWidget = QWidget(self)
        topRowWidget.setLayout(topRow)
        topRowWidget.setObjectName("topRowWidget")
        topRowWidget.setStyleSheet("""#topRowWidget {
                                            border: 3px solid #11361e;
                                            border-radius: 20px;
                                            background: #cdd1cf;
                                        }""")
        leftColumn.addWidget(topRowWidget)

        # # Add a horizontal line
        # hLine = Line(horizontal=True, parent=self)
        # leftColumn.addWidget(hLine)

        # Create the bottom row
        bottomRow = QHBoxLayout()
        self.image_uploader3 = ImageUploader()
        self.image_uploader4 = ImageUploader()
        bottomRow.addWidget(self.image_uploader3)
        bottomRow.addWidget(self.image_uploader4)
        # leftColumn.addLayout(bottomRow)
        
        # Create a QWidget to hold the left column layout and set the border
        bottomRowWidget = QWidget(self)
        bottomRowWidget.setLayout(bottomRow)
        bottomRowWidget.setObjectName("bottomRowWidget")
        bottomRowWidget.setStyleSheet("""#bottomRowWidget {
                                            border: 3px solid #11361e;
                                            border-radius: 20px;
                                            padding: 10px;
                                            background: #cdd1cf;
                                        }""")
        leftColumn.addWidget(bottomRowWidget)        

        # Add the left column to the main layout
        leftColumnWidget = QWidget(self)
        leftColumnWidget.setLayout(leftColumn)
        # leftColumnWidget.setStyleSheet("""border: 3px solid #01240e;
        #                                 border-radius: 20px;
        #                                 padding: 10px;
        #                                 margin: 10px;""")
        self.mainLayout.addWidget(leftColumnWidget, 3)  # Weight = 3 for the left column

    def createRightColumn(self):
        rightColumn = QVBoxLayout()

        self.controls = Controls()
        rightColumn.addWidget(self.controls, 1)
        
        # Output ports
        self.port1 = Output()
        self.port2 = Output()
        rightColumn.addWidget(self.port1, 5)
        rightColumn.addWidget(self.port2, 5)

        self.mix_button = Mix()
        rightColumn.addWidget(self.mix_button, 1)
        rightColumn.setAlignment(self.mix_button, Qt.AlignmentFlag.AlignCenter)  # Center the button
        self.mix_button.clicked.connect(self.get_ft_components)

        rightColumnWidget = QWidget()
        rightColumnWidget.setLayout(rightColumn)
        rightColumnWidget.setObjectName("RightColumnWidget")
        rightColumnWidget.setStyleSheet("""#RightColumnWidget {
                                            border: 3px solid #11361e;
                                            border-radius: 20px;
                                            padding: 10px;
                                            background: #cdd1cf;
                                        }""")
        # Add the right column to the main layout
        rightColumnWidget.setFixedHeight(960)

        self.mainLayout.addWidget(rightColumnWidget, 1)

    def get_ft_components(self):
        mode, img1, img2, img3, img4 = None, None, None, None, None
        if self.controls.get_roi() == "Inner":
            print("inner")
            if self.controls.get_mode() == "Magnitude/Phase":
                mode = "mp"
                img1 = self.image_uploader1.get_component()[0]
                img2 = self.image_uploader2.get_component()[0]
                img3 = self.image_uploader3.get_component()[0]
                img4 = self.image_uploader4.get_component()[0]
            
            else:
                mode = "ri"
                img1 = self.image_uploader1.get_component()[0]
                img2 = self.image_uploader2.get_component()[0]
                img3 = self.image_uploader3.get_component()[0]
                img4 = self.image_uploader4.get_component()[0]
        
        else:
            print("outer")
            if self.controls.get_mode() == "Magnitude/Phase":
                mode = "mp"
                img1 = self.image_uploader1.get_component()[1]
                img2 = self.image_uploader2.get_component()[1]
                img3 = self.image_uploader3.get_component()[1]
                img4 = self.image_uploader4.get_component()[1]
            
            else:
                mode = "ri"
                img1 = self.image_uploader1.get_component()[1]
                img2 = self.image_uploader2.get_component()[1]
                img3 = self.image_uploader3.get_component()[1]
                img4 = self.image_uploader4.get_component()[1]
        
        print(mode)
        self.image_uploader1.image_ft.set_mode(mode)
        port = self.controls.get_option()
        if port == "Port 1":
            self.port1.set_data([img1, img2, img3, img4], mode)
        else:   
            self.port2.set_data([img1, img2, img3, img4], mode)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mixer()
    window.show()
    sys.exit(app.exec_())
