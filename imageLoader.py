import sys
from PyQt5.QtWidgets import QApplication, QLabel, QFileDialog, QHBoxLayout, QWidget, QComboBox
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPainterPath
from PyQt5.QtCore import Qt, QEvent
import cv2
import numpy as np

class ImageUploader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create the layout for the window
        layout = QHBoxLayout(self)
        self.width, self.height, self.radius = 250, 350, 15
        # Create the original image display QLabel
        self.original_image_label = QLabel(self)
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_image_label.setStyleSheet("border-radius: 10px; border: 2px solid #73917b;")
        self.original_image_label.setFixedSize(self.width, self.height)  # Rectangle size
        pixmap = QPixmap("ImageMixer/icons/coloredUpload.png")
        self.original_image_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio))  # Adjust size as needed
        self.image = None

        # Create a ComboBox below the original image label
        self.component_combo = QComboBox(self)
        self.component_combo.addItem("Choose Component")
        self.component_combo.addItem("Magnitude")
        self.component_combo.addItem("Phase")
        self.component_combo.addItem("Real")
        self.component_combo.addItem("Imaginary")
        
        # Connect the ComboBox to the plot_fourier function
        self.component_combo.currentIndexChanged.connect(self.plot_fourier)
        
        # Create the FT image display QLabel
        self.ft_image_label = QLabel(self)
        self.ft_image_label.setAlignment(Qt.AlignCenter)
        self.ft_image_label.setStyleSheet("border-radius: 10px; border: 2px solid #73917b;")
        self.ft_image_label.setFixedSize(self.width, self.height)  # Same size as the original image label
        self.ftImage = None
        
        # Add labels to the layout
        layout.addWidget(self.original_image_label)
        layout.addWidget(self.component_combo)
        layout.addSpacing(20)  # 30px space between the original image and FT image
        layout.addWidget(self.ft_image_label)
        
        # Set the layout for the window
        self.setLayout(layout)

        self.magnitude = None
        self.phase = None
        self.real = None
        self.imaginary = None
    
    def mousePressEvent(self, event):
        # Handle double-click event to open file dialog
        if event.button() == Qt.LeftButton and event.type() == QEvent.MouseButtonDblClick:
            self.upload_image()
            
    def upload_image(self):
        # Open file dialog to select an image
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.bmp)")
        
        if file_path:
            # Load the image using OpenCV
            img_bgr = cv2.imread(file_path)

            # Convert the image to grayscale
            img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

            # Store the image for FFT processing
            self.image = img_gray

            # Convert the grayscale image to QImage
            height, width = img_gray.shape
            qimage = QImage(img_gray.data, width, height, width, QImage.Format_Grayscale8)

            # Convert QImage to QPixmap and set it in the QLabel
            pixmap = QPixmap.fromImage(qimage)
            pixmap = self.get_rounded_pixmap(pixmap, self.original_image_label.size(), self.radius)
            self.original_image_label.setPixmap(pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio))

            # Compute the Fourier Transform and display it
            self.fft()

    def fft(self):
        # Compute the 2D Fourier Transform for the entire image
        f_transform = np.fft.fft2(self.image)  # Complex array
        f_shift = np.fft.fftshift(f_transform)  # Shift the zero frequency component to the center

        # Extract the components
        magnitude = np.log1p(np.abs(f_shift)) # Magnitude spectrum
        phase = np.angle(f_shift)   # Phase spectrum
        real = np.real(f_shift)     # Real part
        imaginary = np.imag(f_shift)  # Imaginary part

        # Store these components as attributes for later use
        self.magnitude = magnitude
        self.phase = phase
        self.real = real
        self.imaginary = imaginary

        # # Normalize the desired component for display (e.g., phase)
        # normalized_phase = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        # # Convert the phase spectrum to a QPixmap for GUI display
        # height, width = normalized_phase.shape
        # qimage_phase = QImage(normalized_phase.data, width, height, width, QImage.Format_Grayscale8)

        # # Convert QImage to QPixmap
        # pixmap_phase = QPixmap.fromImage(qimage_phase)

        # # Apply rounded corners to the phase pixmap
        # rounded_pixmap_phase = self.get_rounded_pixmap(pixmap_phase, self.ft_image_label.size(), self.radius)

        # # Display the rounded phase pixmap in the QLabel
        # self.ft_image_label.setPixmap(rounded_pixmap_phase.scaled(self.width, self.height, Qt.KeepAspectRatio))

    def plot_fourier(self):
        # Get the selected component from the combobox
        selected_component = self.component_combo.currentText()
        
        # Based on the selected component, plot the corresponding FT image
        if selected_component == "Magnitude" and self.magnitude is not None:
            component_data = self.magnitude
        elif selected_component == "Phase" and self.phase is not None:
            component_data = self.phase
        elif selected_component == "Real" and self.real is not None:
            component_data = self.real
        elif selected_component == "Imaginary" and self.imaginary is not None:
            component_data = self.imaginary
        else:
            return  # Do nothing if no valid component is selected

        # Normalize the component for display
        normalized_component = cv2.normalize(component_data, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        # Convert the component to QImage for display
        height, width = normalized_component.shape
        qimage_component = QImage(normalized_component.data, width, height, width, QImage.Format_Grayscale8)

        # Convert QImage to QPixmap
        pixmap_component = QPixmap.fromImage(qimage_component)

        # Apply rounded corners to the pixmap
        rounded_pixmap = self.get_rounded_pixmap(pixmap_component, self.ft_image_label.size(), self.radius)

        # Display the rounded pixmap in the QLabel
        self.ft_image_label.setPixmap(rounded_pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio))
    
    # Changing the style of the image to match the size of the rectangle
    def get_rounded_pixmap(self, pixmap, size, radius):
        # Resize the pixmap to fit the QLabel
        pixmap = pixmap.scaled(size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        # Create a transparent pixmap with the QLabel's size
        rounded_pixmap = QPixmap(size)
        rounded_pixmap.fill(Qt.transparent)

        # Create a QPainter to draw the rounded pixmap
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        # Create a rounded rectangle path
        path = QPainterPath()
        path.addRoundedRect(0, 0, size.width(), size.height(), radius, radius)

        # Set the clip path and draw the pixmap
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        return rounded_pixmap



# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ImageUploader()
#     window.setWindowTitle("Image Upload and Fourier Transform")
#     window.resize(850, 850)  # Resize window to fit both images
#     window.show()
#     sys.exit(app.exec_())
