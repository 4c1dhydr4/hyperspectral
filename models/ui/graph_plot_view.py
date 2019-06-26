from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from spectral import *
import random

class graph_plot_view(QWidget):
	def __init__(self, parent = None):

		QWidget.__init__(self, parent)
		self.figure_2d = Figure()
		self.canvas = FigureCanvas(self.figure_2d)
		vertical_layout = QVBoxLayout()
		vertical_layout.addWidget(self.canvas)
		self.canvas.axes = self.figure_2d.add_subplot(111)
		self.setLayout(vertical_layout)
		self.canvas.axes.clear()
		self.canvas.axes.grid(True)
		self.canvas.draw()