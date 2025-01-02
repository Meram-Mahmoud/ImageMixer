# Image Mixer Application
(Image
The Image Mixer project is a graphical application designed for mixing and processing images using Fourier Transform (FT) components. It provides a user-friendly interface to load images, perform Fourier Transform operations, and create composite images by combining selected FT components.
## Features
### 1. Graphical User Interface (GUI)
The application offers a user-friendly GUI with the following components:

### 1. Image Viewports: Display loaded images for processing.
-[Fourier Transform (FT) Viewports:] (#Show FT components of the loaded images.)
-[Output Viewports:] (#Display the final mixed and processed images.)
### 2. Image Loading and Processing
Load Images: Users can upload images in formats like PNG, JPG, JPEG, and JFIF using the "Browse" option in each Image Viewport.
Image Processing: Loaded images are transformed into Fourier Transform components, which are visualized in the FT Viewports. These components form the basis for mixing operations.
### 3. Image Mixing
Mixing Options: Users can mix pairs of FT components (Magnitude, Phase, Real, Imaginary) selected from combo boxes. The application ensures valid selections before proceeding.
Adjustable Parameters: Sliders allow users to control the weights of the selected FT components, enabling fine-tuning of the final mixed image.
### 4. Interactive User Interactions
Component Selection: Users can select and manipulate specific regions of images or FT components to enhance control over the mixing process.
Brightness and Contrast Adjustment: Adjust brightness and contrast of images interactively via mouse movements, ensuring clear visualization of regions during the mixing process.
### 5. Error Handling
Informative Feedback: The application provides error messages to guide users when invalid inputs or operations occur, such as improper FT component selections.
### 6. Logging
  Activity Logs: Events and errors are logged into a file named Mixer.log. This log aids in debugging and provides a record of the application's activities.
How to Use
Run the Application:

Execute the script to launch the GUI.
Load Images:

Double-click on any Image Viewport and use the "Browse" option to upload images.
Adjust Visualization:

Use right-click and drag (horizontal/vertical) on the mouse to modify brightness and contrast.
Select Mixing Options:

Choose FT components and adjust the mixing parameters using the sliders.
Mix Images:

Click the "Mix" button to generate the mixed image.
View Output:

The mixed image will appear in the Output Viewport.
Dependencies
This project relies on the following Python libraries:

PyQt6: For GUI development.
NumPy: For numerical computations.
Pillow (PIL): For image processing.
SciPy: For performing Fast Fourier Transform (FFT) operations.
Install the dependencies using:

bash
Copy code
pip install -r requirements.txt
Logging
All events and errors are recorded in our_log.log. Check this file for detailed logs of application activities, which can assist in debugging and analysis.

Demo
Check out the demo video for a walkthrough of the application: Demo.mp4

How to Run
Install the dependencies:
bash
Copy code
pip install -r requirements.txt
Launch the application:
bash
Copy code
python main.py
Contributors
We welcome contributions! Feel free to explore, experiment, and enhance the Image Mixer application.
