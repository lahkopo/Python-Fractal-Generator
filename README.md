Fractal Generator 
A desktop application built with Python and PyQt6 for generating and visualizing various beautiful fractals. This tool provides a user-friendly interface to customize and explore the intricate world of fractal mathematics.

Features
Multiple Fractal Types: Generate classic fractals like Mandelbrot, Julia, and more.
Customization: Easily adjust parameters such as resolution, color schemes, maximum iterations, and fractal-specific constants.
User-Friendly GUI: A simple and intuitive interface built with PyQt6.
Real-Time Progress: A progress bar shows the status of the fractal generation, which runs on a separate thread to keep the UI responsive.
Save Your Art: Save any generated fractal as a high-quality .png image.

Fractals Available
The generator currently supports the following fractal types:
Mandelbrot Set
Julia Set
Burning Ship
Newton Fractal
Barnsley Fern
Sierpinski Triangle

Setup and Installation
Follow these steps to get the application running on your local machine.

Prerequisites
Python 3.6 or newer.

Installation Steps
Clone the repository (or simply download the app.py file into a new folder).
git clone https://your-repository-url.com/
cd fractal-generator

Create and activate a virtual environment. This keeps your project dependencies isolated.
# Create the environment
python -m venv venv

# Activate on Windows
.\venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate

Install the required libraries. All dependencies are listed in the requirements.txt file.
pip install -r requirements.txt


How to Run
With your virtual environment activated and dependencies installed, run the application with the following command:
python app.py


The application window will launch, and you can start generating your own fractals!