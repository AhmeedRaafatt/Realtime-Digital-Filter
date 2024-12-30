import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
    QLabel, QSlider, QFileDialog, QCheckBox, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.patches import Circle
from scipy.signal import freqz, zpk2tf, butter, cheby1, cheby2, ellip, bessel

class FilterDesignApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-Time Digital Filter Design")
        self.setGeometry(100, 100, 1200, 800)

        # Main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # Initialize data and UI components
        self.zeros = []
        self.poles = []
        self.history = []  # Undo/Redo history
        self.redo_stack = []
        self.unit_circle_radius = 1
        self.sample_rate = 1000
        self.selected_point = None
        self.selected_type = None
        self.initialize_ui()

    def create_plot_canvas(self):
        fig, ax = plt.subplots()
        fig.tight_layout()
        canvas = FigureCanvas(fig)

        # Connect mouse events for dragging
        canvas.mpl_connect('button_press_event', self.on_click)
        canvas.mpl_connect('button_release_event', self.on_release)
        canvas.mpl_connect('motion_notify_event', self.on_motion)

        return canvas, ax

    def initialize_ui(self):
        # Layouts for different sections
        self.graph_layout = QHBoxLayout()
        self.controls_layout = QVBoxLayout()
        self.main_layout.addLayout(self.graph_layout)
        self.main_layout.addLayout(self.controls_layout)

        # Z-Plane Plot
        self.z_plane_canvas, self.z_plane_ax = self.create_plot_canvas()
        self.graph_layout.addWidget(self.z_plane_canvas)

        # Frequency Response Plot
        self.freq_response_canvas, self.freq_response_ax = self.create_plot_canvas()
        self.graph_layout.addWidget(self.freq_response_canvas)

        # Controls Section
        self.add_buttons()
        self.add_sliders()
        self.add_checkboxes_and_comboboxes()
        self.plot_z_plane()
        self.plot_frequency_response()


    def add_buttons(self):
        # Add buttons for filter operations
        self.add_zero_button = QPushButton("Add Zero")
        self.add_pole_button = QPushButton("Add Pole")
        self.clear_zeros_button = QPushButton("Clear Zeros")
        self.clear_poles_button = QPushButton("Clear Poles")
        self.clear_all_button = QPushButton("Clear All")
        self.swap_zeros_poles_button = QPushButton("Swap Zeros/Poles")
        self.undo_button = QPushButton("Undo")
        self.redo_button = QPushButton("Redo")
        self.save_filter_button = QPushButton("Save Filter")
        self.load_filter_button = QPushButton("Load Filter")
        self.generate_c_code_button = QPushButton("Generate C Code")

        self.controls_layout.addWidget(self.add_zero_button)
        self.controls_layout.addWidget(self.add_pole_button)
        self.controls_layout.addWidget(self.clear_zeros_button)
        self.controls_layout.addWidget(self.clear_poles_button)
        self.controls_layout.addWidget(self.clear_all_button)
        self.controls_layout.addWidget(self.swap_zeros_poles_button)
        self.controls_layout.addWidget(self.undo_button)
        self.controls_layout.addWidget(self.redo_button)
        self.controls_layout.addWidget(self.save_filter_button)
        self.controls_layout.addWidget(self.load_filter_button)
        self.controls_layout.addWidget(self.generate_c_code_button)

        # Connect buttons to actions
        self.add_zero_button.clicked.connect(lambda: self.add_element("zero"))
        self.add_pole_button.clicked.connect(lambda: self.add_element("pole"))
        self.clear_zeros_button.clicked.connect(self.clear_zeros)
        self.clear_poles_button.clicked.connect(self.clear_poles)
        self.clear_all_button.clicked.connect(self.clear_all)
        self.swap_zeros_poles_button.clicked.connect(self.swap_zeros_poles)
        self.undo_button.clicked.connect(self.undo)
        self.redo_button.clicked.connect(self.redo)
        self.save_filter_button.clicked.connect(self.save_filter)
        self.load_filter_button.clicked.connect(self.load_filter)
        self.generate_c_code_button.clicked.connect(self.generate_c_code)

    def add_sliders(self):
        self.speed_slider_label = QLabel("Processing Speed")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(50)

        self.controls_layout.addWidget(self.speed_slider_label)
        self.controls_layout.addWidget(self.speed_slider)

    def add_checkboxes_and_comboboxes(self):
        self.add_conjugates_checkbox = QCheckBox("Add Conjugates")
        self.controls_layout.addWidget(self.add_conjugates_checkbox)

        self.filter_library_combobox = QComboBox()
        self.filter_library_combobox.addItems([
            "Butterworth LPF", "Butterworth HPF", "Chebyshev LPF", "Chebyshev HPF",
            "Elliptic LPF", "Elliptic HPF", "Bessel LPF", "Bessel HPF"
        ])
        self.filter_library_combobox.currentIndexChanged.connect(self.load_predefined_filter)

        self.controls_layout.addWidget(QLabel("Filter Library"))
        self.controls_layout.addWidget(self.filter_library_combobox)

    def add_element(self, element_type):
        new_element = 0.5 + 0j if element_type == "zero" else 0.7 + 0j
        if element_type == "zero":
            self.zeros.append(new_element)
        elif element_type == "pole":
            self.poles.append(new_element)
        if self.add_conjugates_checkbox.isChecked() and new_element.imag != 0:
            conjugate = new_element.conjugate()
            if element_type == "zero":
                self.zeros.append(conjugate)
            elif element_type == "pole":
                self.poles.append(conjugate)
        self.save_to_history()
        self.plot_z_plane()
        self.plot_frequency_response()

    def on_click(self, event):
        if event.inaxes != self.z_plane_ax:
            return
        for idx, z in enumerate(self.zeros):
            if abs(z.real - event.xdata) < 0.05 and abs(z.imag - event.ydata) < 0.05:
                self.selected_point = idx
                self.selected_type = "zero"
                return
        for idx, p in enumerate(self.poles):
            if abs(p.real - event.xdata) < 0.05 and abs(p.imag - event.ydata) < 0.05:
                self.selected_point = idx
                self.selected_type = "pole"
                return

    def on_motion(self, event):
        if event.inaxes != self.z_plane_ax or self.selected_point is None:
            return
        new_position = complex(event.xdata, event.ydata)
        if abs(new_position) > 1.5:  # Boundary check
            return
        if self.selected_type == "zero":
            self.zeros[self.selected_point] = new_position
        elif self.selected_type == "pole":
            self.poles[self.selected_point] = new_position
        self.plot_z_plane()
        self.plot_frequency_response()

    def on_release(self, event):
        if self.selected_point is not None:
            self.save_to_history()
        self.selected_point = None
        self.selected_type = None

    def clear_zeros(self):
        self.zeros.clear()
        self.save_to_history()
        self.plot_z_plane()
        self.plot_frequency_response()

    def clear_poles(self):
        self.poles.clear()
        self.save_to_history()
        self.plot_z_plane()
        self.plot_frequency_response()

    def clear_all(self):
        self.zeros.clear()
        self.poles.clear()
        self.save_to_history()
        self.plot_z_plane()
        self.plot_frequency_response()

    def swap_zeros_poles(self):
        self.zeros, self.poles = self.poles, self.zeros
        self.save_to_history()
        self.plot_z_plane()
        self.plot_frequency_response()

    def undo(self):
        if self.history:
            self.redo_stack.append((self.zeros.copy(), self.poles.copy()))
            self.zeros, self.poles = self.history.pop()
            self.plot_z_plane()
            self.plot_frequency_response()

    def redo(self):
        if self.redo_stack:
            self.history.append((self.zeros.copy(), self.poles.copy()))
            self.zeros, self.poles = self.redo_stack.pop()
            self.plot_z_plane()
            self.plot_frequency_response()

    def save_to_history(self):
        self.history.append((self.zeros.copy(), self.poles.copy()))
        if len(self.history) > 50:  # Limit history size
            self.history.pop(0)

    def save_filter(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Filter", "", "CSV Files (*.csv)")
        if file_name:
            with open(file_name, "w") as file:
                file.write("zeros,poles\n")
                file.write("{}\n".format(",".join(map(str, self.zeros))))
                file.write("{}\n".format(",".join(map(str, self.poles))))

    def load_filter(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Filter", "", "CSV Files (*.csv)")
        if file_name:
            with open(file_name, "r") as file:
                lines = file.readlines()
                self.zeros = [complex(z) for z in lines[1].strip().split(",")]
                self.poles = [complex(p) for p in lines[2].strip().split(",")]
            self.plot_z_plane()
            self.plot_frequency_response()

    def generate_c_code(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Generate C Code", "", "C Files (*.c)")
        if file_name:
            with open(file_name, "w") as file:
                file.write("// C Code for Digital Filter\n")
                file.write("// Zeros: {}\n".format(self.zeros))
                file.write("// Poles: {}\n".format(self.poles))

    def plot_z_plane(self):
        self.z_plane_ax.clear()
        self.z_plane_ax.add_artist(Circle((0, 0), self.unit_circle_radius, color="black", fill=False))
        self.z_plane_ax.scatter([z.real for z in self.zeros], [z.imag for z in self.zeros], color="blue", label="Zeros")
        self.z_plane_ax.scatter([p.real for p in self.poles], [p.imag for p in self.poles], color="red", label="Poles")
        self.z_plane_ax.set_xlim([-1.5, 1.5])
        self.z_plane_ax.set_ylim([-1.5, 1.5])
        self.z_plane_ax.axhline(0, color='gray', linestyle='--', linewidth=0.5)
        self.z_plane_ax.axvline(0, color='gray', linestyle='--', linewidth=0.5)
        self.z_plane_ax.set_aspect('equal', adjustable='box')
        self.z_plane_ax.legend()
        self.z_plane_canvas.draw()

    def plot_frequency_response(self):
        self.freq_response_ax.clear()
        if self.zeros or self.poles:
            b, a = zpk2tf(self.zeros, self.poles, 1)
            w, h = freqz(b, a, worN=8000)
            self.freq_response_ax.plot(w / np.pi, 20 * np.log10(abs(h)), color="blue", label="Magnitude Response")
            self.freq_response_ax.set_title("Frequency Response")
            self.freq_response_ax.set_xlabel("Normalized Frequency (xπ rad/sample)")
            self.freq_response_ax.set_ylabel("Magnitude (dB)")
            self.freq_response_ax.grid(True)
        self.freq_response_canvas.draw()

    def load_predefined_filter(self, index):
        predefined_filters = {
            0: butter(4, 0.2, btype='low', output='zpk'),
            1: butter(4, 0.2, btype='high', output='zpk'),
            2: cheby1(4, 1, 0.2, btype='low', output='zpk'),
            3: cheby1(4, 1, 0.2, btype='high', output='zpk'),
            4: ellip(4, 1, 40, 0.2, btype='low', output='zpk'),
            5: ellip(4, 1, 40, 0.2, btype='high', output='zpk'),
            6: bessel(4, 0.2, btype='low', output='zpk'),
            7: bessel(4, 0.2, btype='high', output='zpk')
        }
        if index in predefined_filters:
            z, p, _ = predefined_filters[index]
            self.zeros = list(z)
            self.poles = list(p)
            self.plot_z_plane()
            self.plot_frequency_response()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FilterDesignApp()
    window.show()
    sys.exit(app.exec_())
