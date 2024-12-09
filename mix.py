from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout

class Mix(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.btn()

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
        self.button.setFixedWidth(280)
        layout = QVBoxLayout(self)
        layout.addWidget(self.button)
        
    @property
    def clicked(self):
        return self.button.clicked
