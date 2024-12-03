import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from imageLoader import ImageUploader
from mainstyle import mainStyle

# class Mixer():
#     def __init__(self):
#         self.view_port()

#     def view_port(self):
#         pass

# Main application outside the class
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create the main window
    window = QLabel()
    window.setWindowTitle("Image Upload Example")
    window.setGeometry(50, 50, 1800, 1000)
    
    # Add the custom image uploader
    image_uploader1 = ImageUploader(window)
    image_uploader1.move(20, 20)  # Position inside the main window
    image_uploader2 = ImageUploader(window)
    image_uploader2.move(570, 20)  # Position inside the main window
    image_uploader3 = ImageUploader(window)
    image_uploader3.move(20, 400)  # Position inside the main window
    image_uploader4 = ImageUploader(window)
    image_uploader4.move(570, 400)  # Position inside the main window

    window.setStyleSheet(mainStyle)

    window.show()
    sys.exit(app.exec_())
