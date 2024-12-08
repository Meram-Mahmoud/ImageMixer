from PyQt5.QtWidgets import QFrame

class Line(QFrame):
    def __init__(self, horizontal=True, parent=None):
        super().__init__(parent)
        self.horizontal = horizontal
        self.setStyleSheet("QFrame { background-color: #01240e; }")
        self.update_style()

    def update_style(self):
        # Set the frame's shape based on its orientation
        if self.horizontal:
            self.setFrameShape(QFrame.HLine)
            # self.setFrameShadow(QFrame.Sunken)
        else:
            self.setFrameShape(QFrame.VLine)
            # self.setFrameShadow(QFrame.Sunken)
