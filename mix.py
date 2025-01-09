from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QProgressBar, QHBoxLayout
from PyQt5.QtCore import pyqtSignal
import logging
import time

# Configure logging
logging.basicConfig(
    filename='ImageMixer/Mixer.log', 
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Mix(QWidget):
    flag = pyqtSignal(object)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.btn()
        self.progress()

    def btn(self):
        self.button = QPushButton("Mix")
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #11361e;  
                color: white; 
                font-size: 20px; 
                border-radius: 8px; 
                padding: 10px; 
                font-weight: bold;                                  
            }
            QPushButton:pressed {
                background-color: #cdd1cf; 
                border: 2px solid #11361e;
                color: #11361e;
            }
        """)
        self.button.setFixedWidth(100)

    def progress(self):
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(45)
        self.progress_bar.setFixedWidth(150)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #11361e;
                border-radius: 10px;
                text-align: center;
                color: #11361e;
                font-weight: bold;
                background-color: #cdd1cf;
            }
            QProgressBar::chunk {
                background-color: #5a996f;
            }
        """)
        self.progress_bar.setValue(0)

        layout = QHBoxLayout(self)
        layout.addWidget(self.button, 1)
        layout.addSpacing(20)
        layout.addWidget(self.progress_bar, 2)

    def update_progress(self):
        # print("in progress bar")
        for i in range(101):
            # if stop_flag.is_set():
            #     break
            self.progress_bar.setValue(i*20)
            time.sleep(0.35)
            logging.debug(f"Progress updated to: {i*20}%")
        self.progress_bar.setValue(0)
        
    @property
    def clicked(self):
        return self.button.clicked
