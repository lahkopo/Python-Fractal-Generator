<div align="center">

# 🎨 Fractal Generator 🌀

**A desktop application for generating and exploring beautiful fractal art using Python and PyQt6.**

</div>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.6%2B-blue?style=for-the-badge&logo=python" alt="Python 3.6+">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge" alt="PRs Welcome">
</p>

<div align="center">



</div>

## ✨ About The Project

This tool provides a user-friendly graphical interface to generate, customize, and visualize a variety of classic fractals. It leverages Matplotlib for rendering and runs the computationally intensive generation process on a separate thread to ensure the UI remains smooth and responsive.

---

## 🌟 Features

-   **Multiple Fractal Types**: Generate the Mandelbrot Set, Julia Set, Burning Ship, and more.
-   **Deep Customization**: Adjust resolution, color schemes, iteration depth, and other fractal-specific parameters.
-   **Responsive UI**: A progress bar provides real-time feedback without freezing the application.
-   **Save Your Art**: Export any generated fractal as a high-quality `.png` image to share or save.

---

## 🌀 Fractals Available

The generator currently supports the following fractal types:

-   Mandelbrot Set
-   Julia Set
-   Burning Ship
-   Newton Fractal
-   Barnsley Fern
-   Sierpinski Triangle

---

## 🛠️ Getting Started

Follow these simple steps to get the application running on your local machine.

### Prerequisites

You'll need **Python 3.6** or newer installed on your system.

### Installation

1.  **Clone the repository** to your local machine:
    ```sh
    git clone https://github.com/lahkopo/Python-Fractal-Generator
    ```

2.  **Create and activate a virtual environment**:
    ```sh
    # Create the environment
    python -m venv venv

    # Activate on Windows
    .\venv\Scripts\activate

    # Activate on macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the required dependencies** from the `requirements.txt` file:
    ```sh
    pip install -r requirements.txt
    ```

---

## ▶️ How to Run

With your virtual environment activated, launch the application with a single command:

```sh
python app.py
