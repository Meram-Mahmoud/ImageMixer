import sys
from PyQt5.QtWidgets import QApplication, QLabel
from imageLoader import ImageUploader

# Main application outside the class
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create the main window
    window = QLabel()
    window.setWindowTitle("Image Upload Example")
    window.setGeometry(50, 50, 1900, 1000)
    
    # Add the custom image uploader
    image_uploader1 = ImageUploader(window)
    image_uploader1.move(50, 30)  # Position inside the main window
    image_uploader2 = ImageUploader(window)
    image_uploader2.move(770, 30)  # Position inside the main window
    image_uploader3 = ImageUploader(window)
    image_uploader3.move(50, 450)  # Position inside the main window
    image_uploader4 = ImageUploader(window)
    image_uploader4.move(770, 450)  # Position inside the main window

    window.show()
    sys.exit(app.exec_())
