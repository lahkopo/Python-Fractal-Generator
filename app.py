import sys
import numpy as np
import time
import matplotlib

matplotlib.use("QtAgg")

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import threading
import queue
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFileDialog,
    QPushButton,
    QComboBox,
    QMessageBox,
    QLineEdit,
    QLabel,
    QProgressBar,
)
from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets


# GUI
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fractal Generator")
        self.resize(640, 800)

        # Variable
        self.fractal_type = "Mandelbrot"
        self.resolution = "500x500"
        self.color_scheme = "inferno"
        self.max_iter = 100
        self.power = 2.0
        self.c_real = -0.42
        self.c_imag = 0.6
        self.fractal_types = [
            "Mandelbrot",
            "Julia",
            "Burning Ship",
            "Newton",
            "Barnsley Fern",
            "Sierpinski Triangle",
        ]
        self.resolutions = [
            "500x500",
            "800x800",
            "1024x1024",
            "1920x1080",
            "2560x1440",
            "3840x2160",
        ]
        self.color_schemes = [
            "inferno",
            "plasma",
            "viridis",
            "magma",
            "twilight",
            "coolwarm",
            "hot",
            "jet",
            "rainbow",
            "terrain",
            "ocean",
            "nipy_spectral",
        ]
        self.progress_value = 0

        #layout za raspored widgeta
        layout = QGridLayout()

        # Odabir fraktala
        self.fractal_menu_label = QLabel("Select Fractal Type:")
        self.fractal_menu = QComboBox()
        self.fractal_menu.setEditable(False)
        self.fractal_menu.addItems(self.fractal_types)
        self.fractal_menu.currentTextChanged.connect(self.combo_frac_type_changed)
        layout.addWidget(self.fractal_menu_label, 0, 0)
        layout.addWidget(self.fractal_menu, 0, 1)

        # Odabir rezolucije
        self.color_menu_label = QLabel("Select Resolution:")
        self.color_menu = QComboBox()
        self.color_menu.setEditable(False)
        self.color_menu.addItems(self.resolutions)
        self.color_menu.currentTextChanged.connect(self.combo_resolution_changed)
        layout.addWidget(self.color_menu_label, 1, 0)
        layout.addWidget(self.color_menu, 1, 1)

        # Odabir boje
        self.color_menu_label = QLabel("Select Color Scheme:")
        self.color_menu = QComboBox()
        self.color_menu.setEditable(False)
        self.color_menu.addItems(self.color_schemes)
        self.color_menu.currentTextChanged.connect(self.combo_color_scheme_changed)
        layout.addWidget(self.color_menu_label, 2, 0)
        layout.addWidget(self.color_menu, 2, 1)

        # Max iterations
        self.max_iter_label = QLabel("Max Iterations:")
        self.max_iter_entry = QLineEdit()
        self.max_iter_entry.setText(str(self.max_iter))
        self.max_iter_entry.editingFinished.connect(self.edit_max_iter_changed)
        layout.addWidget(self.max_iter_label, 3, 0)
        layout.addWidget(self.max_iter_entry, 3, 1)

        # Power (for Mandelbrot and Burning Ship)
        self.power_label = QLabel("Power:")
        self.power_entry = QLineEdit()
        self.power_entry.setText(str(self.power))
        self.power_entry.editingFinished.connect(self.edit_power_changed)
        layout.addWidget(self.power_label, 4, 0)
        layout.addWidget(self.power_entry, 4, 1)

        # Julia set constant
        self.c_real_label = QLabel("Constant (c) - Real Part:")
        self.c_real_entry = QLineEdit()
        self.c_real_entry.setText(str(self.c_real))
        self.c_real_entry.editingFinished.connect(self.edit_c_real_changed)
        self.c_imag_label = QLabel("Constant (c) - Imaginary Part:")
        self.c_imag_entry = QLineEdit()
        self.c_imag_entry.setText(str(self.c_imag))
        self.c_imag_entry.editingFinished.connect(self.edit_c_imag_changed)
        layout.addWidget(self.c_real_label, 6, 0)
        layout.addWidget(self.c_real_entry, 6, 1)
        layout.addWidget(self.c_imag_label, 7, 0)
        layout.addWidget(self.c_imag_entry, 7, 1)
        self.c_real_label.setVisible(False)
        self.c_real_entry.setVisible(False)
        self.c_imag_label.setVisible(False)
        self.c_imag_entry.setVisible(False)

        # Generate dugme
        self.generate_button = QPushButton("Generate Fractal")
        self.generate_button.clicked.connect(self.generate_fractal_threaded)
        self.generate_button.setStyleSheet("QPushButton{padding: 6px;}")
        layout.addWidget(self.generate_button, 8, 0, 1, 2)

        # Progress bar
        self.progress = QProgressBar()
        layout.addWidget(self.progress, 9, 0, 1, 2)

        # Canvas
        self.figure, self.ax = plt.subplots(figsize=(8, 8))
        self.canvas = FigureCanvasQTAgg(self.figure)
        # self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        # self.canvas.get_tk_widget().pack()
        layout.addWidget(self.canvas, 10, 0, 1, 2)

        # Save dugme
        self.save_button = QPushButton("Save Fractal")
        self.save_button.clicked.connect(self.save_fractal)
        self.save_button.setStyleSheet("QPushButton{padding: 6px; font-weight: bold;}")
        layout.addWidget(self.save_button, 11, 0, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def combo_frac_type_changed(self, s):
        self.fractal_type = s
        fractal_type = self.fractal_type

        if fractal_type == "Mandelbrot" or fractal_type == "Burning Ship":
            self.power_label.setVisible(True)
            self.power_entry.setVisible(True)
            self.c_real_label.setVisible(False)
            self.c_real_entry.setVisible(False)
            self.c_imag_label.setVisible(False)
            self.c_imag_entry.setVisible(False)

        elif fractal_type == "Julia":
            self.power_label.setVisible(False)
            self.power_entry.setVisible(False)
            self.c_real_label.setVisible(True)
            self.c_real_entry.setVisible(True)
            self.c_imag_label.setVisible(True)
            self.c_imag_entry.setVisible(True)

        else:
            self.power_label.setVisible(False)
            self.power_entry.setVisible(False)
            self.c_real_label.setVisible(False)
            self.c_real_entry.setVisible(False)
            self.c_imag_label.setVisible(False)
            self.c_imag_entry.setVisible(False)

    def combo_resolution_changed(self, s):
        self.resolution = s

    def combo_color_scheme_changed(self, s):
        self.color_scheme = s

    def edit_max_iter_changed(self):
        try:
            self.max_iter = int(self.max_iter_entry.text())
        except:
            QMessageBox.warning(self, "Max Iterations Warning!", "The entered value must be a integer number.")

    def edit_power_changed(self):
        try:
            power = self.power_entry.text().replace(",",".")
            self.power = float(power)
        except:
            QMessageBox.warning(self, "Power Warning!", "The entered value must be a decimal number.")

    def edit_c_real_changed(self):
        try:
            c_real = self.c_real_entry.text().replace(",",".")
            self.c_real = float(c_real)
        except:
            QMessageBox.warning(self, "Constant (c) Real Part Warning!", "The entered value must be a decimal number.")


    def edit_c_imag_changed(self):
        try:
            c_imag = self.c_imag_entry.text().replace(",",".")
            self.c_imag = float(c_imag)
        except:
            QMessageBox.warning(self, "Constant (c) Imaginary Part Warning!", "The entered value must be a decimal number.")

    def generate_fractal_threaded(self):
        self.queue = queue.Queue()
        threading.Thread(target=self.generate_fractal, args=(self.queue,)).start()
        time.sleep(0.1)
        self.check_queue()
            
    def check_queue(self):
        try:
            fractal, fractal_type, color_scheme = self.queue.get_nowait()
            self.progress.setValue(100)
            self.display_fractal(fractal, fractal_type, color_scheme)
        except queue.Empty:
            self.progress.setValue(self.progress_value)
            time.sleep(0.1)
            self.check_queue()

    def generate_fractal(self, q):
        self.generate_button.setEnabled(False)
        self.progress_value = 0
        self.progress.setValue(self.progress_value)
        fractal_type = self.fractal_type
        width, height = self.get_resolution()
        max_iter = self.max_iter
        color_scheme = self.color_scheme

        if fractal_type == "Mandelbrot":
            power = self.power
            fractal = self.mandelbrot(width, height, -2, 1, -1.5, 1.5, max_iter, power)
        elif fractal_type == "Julia":
            c = complex(self.c_real, self.c_imag)
            fractal = self.julia(width, height, -2, 2, -2, 2, max_iter, c)
        elif fractal_type == "Burning Ship":
            power = self.power
            fractal = self.burning_ship(width, height, -2, 2, -2, 2, max_iter, power)
        elif fractal_type == "Newton":
            fractal = self.newton_fractal(width, height, -2, 2, -2, 2, max_iter)
        elif fractal_type == "Barnsley Fern":
            fractal = self.barnsley_fern(width, height, max_iter)
        elif fractal_type == "Sierpinski Triangle":
            fractal = self.sierpinski_triangle(width, height, max_iter)

        q.put((fractal, fractal_type, color_scheme))
        self.fractal = fractal
        self.color_scheme_final = color_scheme
        # self.display_fractal(fractal, fractal_type, color_scheme)

    def display_fractal(self, fractal, fractal_type, color_scheme):
        self.ax.clear()
        norm = mcolors.Normalize(vmin=fractal.min(), vmax=fractal.max())
        cmap = plt.get_cmap(color_scheme)

        width, height = self.get_resolution()

        if width == height:
            extent = (0, 1, 0, 1)
        else:
            aspect_ratio = width / height
            if aspect_ratio > 1:
                extent = (0, 16, 0, 9)
            else:
                extent = (0, 9, 0, 16)

        self.ax.imshow(fractal, cmap=cmap, norm=norm, extent=extent)
        self.ax.set_title(f"{fractal_type} - {color_scheme}")
        self.canvas.draw()
        self.generate_button.setEnabled(True)

    def save_fractal(self):
        if hasattr(self, "fractal"):
            filename = QFileDialog.getSaveFileName(
                self,
                caption="Save fracal in .png image",
                directory="fractal.png",
                filter="(*.png)",
            )
            if filename:
                cmap = plt.get_cmap(self.color_scheme_final)
                plt.imsave(
                    filename[0],
                    self.fractal,
                    cmap=cmap,
                    origin="lower",
                    dpi=100,
                )
                QMessageBox.information(
                    self, "Success!", "Fractal image saved successfully."
                )
        else:
            QMessageBox.warning(self, "Warning!", "No fractal data available to save.")

    def get_resolution(self):
        res_text = self.resolution
        width, height = map(int, res_text.split("x"))
        return width, height

    # Fractal Funkcije
    #####################################################################################
    def mandelbrot(self, width, height, x_min, x_max, y_min, y_max, max_iter, power):
        aspect_ratio = width / height
        x_range = x_max - x_min
        y_range = y_max - y_min

        if aspect_ratio > 1:
            y_center = (y_min + y_max) / 2
            y_range_adjusted = x_range / aspect_ratio
            y_min = y_center - y_range_adjusted / 2
            y_max = y_center + y_range_adjusted / 2
        else:
            x_center = (x_min + x_max) / 2
            x_range_adjusted = y_range * aspect_ratio
            x_min = x_center - x_range_adjusted / 2
            x_max = x_center + x_range_adjusted / 2

        x_vals = np.linspace(x_min, x_max, width)
        y_vals = np.linspace(y_min, y_max, height)
        y_len = len(y_vals) #za računanje progresa
        fractal = np.zeros((height, width))

        for i, y in enumerate(y_vals):
            for j, x in enumerate(x_vals):
                c = complex(x, y)
                z = 0
                for n in range(max_iter):
                    if abs(z) > 2:
                        fractal[i, j] = n
                        break
                    z = z**power + c

            self.progress_value = round((i / y_len) * 100)

        return fractal

    def julia(self, width, height, x_min, x_max, y_min, y_max, max_iter, c):
        aspect_ratio = width / height
        x_range = x_max - x_min
        y_range = y_max - y_min

        if aspect_ratio > 1:
            y_center = (y_min + y_max) / 2
            y_range_adjusted = x_range / aspect_ratio
            y_min = y_center - y_range_adjusted / 2
            y_max = y_center + y_range_adjusted / 2
        else:
            x_center = (x_min + x_max) / 2
            x_range_adjusted = y_range * aspect_ratio
            x_min = x_center - x_range_adjusted / 2
            x_max = x_center + x_range_adjusted / 2

        x_vals = np.linspace(x_min, x_max, width)
        y_vals = np.linspace(y_min, y_max, height)
        y_len = len(y_vals) #za računanje progresa
        fractal = np.zeros((height, width))

        for i, y in enumerate(y_vals):
            for j, x in enumerate(x_vals):
                z = complex(x, y)
                for n in range(max_iter):
                    if abs(z) > 2:
                        fractal[i, j] = n
                        break
                    z = z**2 + c

            self.progress_value = round((i / y_len) * 100)

        return fractal
    

    def burning_ship(self, width, height, x_min, x_max, y_min, y_max, max_iter, power):
        aspect_ratio = width / height
        x_range = x_max - x_min
        y_range = y_max - y_min

        if aspect_ratio > 1:
            y_center = (y_min + y_max) / 2
            y_range_adjusted = x_range / aspect_ratio
            y_min = y_center - y_range_adjusted / 2
            y_max = y_center + y_range_adjusted / 2
        else:
            x_center = (x_min + x_max) / 2
            x_range_adjusted = y_range * aspect_ratio
            x_min = x_center - x_range_adjusted / 2
            x_max = x_center + x_range_adjusted / 2

        x_vals = np.linspace(x_min, x_max, width)
        y_vals = np.linspace(y_min, y_max, height)
        y_len = len(y_vals) #za računanje progresa
        fractal = np.zeros((height, width))

        for i, y in enumerate(y_vals):
            for j, x in enumerate(x_vals):
                c = complex(x, y)
                z = 0
                for n in range(max_iter):
                    if abs(z) > 2:
                        fractal[i, j] = n
                        break
                    z = complex(abs(z.real), abs(z.imag)) ** power + c

            self.progress_value = round((i / y_len) * 100)

        return fractal

    def newton_fractal(self, width, height, x_min, x_max, y_min, y_max, max_iter, n=3):
        aspect_ratio = width / height
        x_range = x_max - x_min
        y_range = y_max - y_min

        if aspect_ratio > 1:
            y_center = (y_min + y_max) / 2
            y_range_adjusted = x_range / aspect_ratio
            y_min = y_center - y_range_adjusted / 2
            y_max = y_center + y_range_adjusted / 2
        else:
            x_center = (x_min + x_max) / 2
            x_range_adjusted = y_range * aspect_ratio
            x_min = x_center - x_range_adjusted / 2
            x_max = x_center + x_range_adjusted / 2

        x_vals = np.linspace(x_min, x_max, width)
        y_vals = np.linspace(y_min, y_max, height)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = X + 1j * Y
        roots = np.exp(2j * np.pi * np.arange(n) / n)
        fractal = np.zeros(Z.shape, dtype=int)

        for i in range(max_iter):
            Z -= (Z**n - 1) / (n * Z ** (n - 1))
            distances = np.abs(Z[..., np.newaxis] - roots)
            closest_root = np.argmin(distances, axis=-1)
            fractal = closest_root

            self.progress_value = round((i / max_iter) * 100)

        return fractal

    def barnsley_fern(self, width, height, max_iter):
        aspect_ratio = width / height
        x_min, x_max = -2.5, 2.5
        y_min, y_max = 0, 10

        if aspect_ratio > 1:
            y_center = (y_min + y_max) / 2
            y_range_adjusted = (x_max - x_min) / aspect_ratio
            y_min = y_center - y_range_adjusted / 2
            y_max = y_center + y_range_adjusted / 2
        else:
            x_center = (x_min + x_max) / 2
            x_range_adjusted = (y_max - y_min) * aspect_ratio
            x_min = x_center - x_range_adjusted / 2
            x_max = x_center + x_range_adjusted / 2

        fractal = np.zeros((height, width))
        x, y = 0, 0

        for a in range(max_iter):
            r = np.random.rand()
            if r < 0.01:
                x, y = 0, 0.16 * y
            elif r < 0.86:
                x, y = 0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6
            elif r < 0.93:
                x, y = 0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6
            else:
                x, y = -0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44

            i = int((x - x_min) * width / (x_max - x_min))
            j = int((y - y_min) * height / (y_max - y_min))
            if 0 <= i < width and 0 <= j < height:
                fractal[j, i] += 1

            self.progress_value = round((a / max_iter) * 100)

        return fractal

    def sierpinski_triangle(self, width, height, max_iter):
        aspect_ratio = width / height
        x_min, x_max = 0, 1
        y_min, y_max = 0, 1

        if aspect_ratio > 1:
            y_center = (y_min + y_max) / 2
            y_range_adjusted = (x_max - x_min) / aspect_ratio
            y_min = y_center - y_range_adjusted / 2
            y_max = y_center + y_range_adjusted / 2
        else:
            x_center = (x_min + x_max) / 2
            x_range_adjusted = (y_max - y_min) * aspect_ratio
            x_min = x_center - x_range_adjusted / 2
            x_max = x_center + x_range_adjusted / 2

        fractal = np.zeros((height, width))
        x, y = 0, 0

        for a in range(max_iter):
            r = np.random.rand()
            if r < 0.5:
                x, y = 0.5 * x, 0.5 * y
            elif r < 0.75:
                x, y = 0.5 * x + 0.25, 0.5 * y + 0.5
            else:
                x, y = 0.5 * x + 0.5, 0.5 * y

            i = int((x - x_min) * width / (x_max - x_min))
            j = int((y - y_min) * height / (y_max - y_min))
            if 0 <= i < width and 0 <= j < height:
                fractal[j, i] += 1

            self.progress_value = round((a / max_iter) * 100)

        return fractal

    #####################################################################################


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
