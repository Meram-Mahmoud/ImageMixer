from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout

class Mix(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.btn()

    def btn(self):
        self.button = QPushButton("Mix")
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #01240e;  
                color: white; 
                font-size: 18px; 
                border-radius: 8px; 
                padding: 10px; 
                width: 150px;
            }
            QPushButton:pressed {
                background-color: #cdd1cf; 
                border: 2px solid #01240e;
                color: #01240e;
            }
        """)
        self.button.setFixedWidth(300)
        layout = QVBoxLayout(self)
        layout.addWidget(self.button)
        
    @property
    def clicked(self):
        return self.button.clicked
