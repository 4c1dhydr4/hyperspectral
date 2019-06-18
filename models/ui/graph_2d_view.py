from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import LassoSelector, Cursor
from matplotlib.path import Path
from matplotlib import patches as patches
from spectral import *
import random

class graph_2d_view(QWidget):
	
	def __init__(self, parent = None):

		QWidget.__init__(self, parent)
		self.figure_2d = Figure()
		self.canvas = FigureCanvas(self.figure_2d)
		vertical_layout = QVBoxLayout()
		vertical_layout.addWidget(self.canvas)
		self.canvas.axes = self.figure_2d.add_subplot(111)
		self.toolbar = NavigationToolbar(self.canvas, self)
		self.setLayout(vertical_layout)
		self.canvas.axes.clear()
		self.canvas.draw()
		self.layout().addWidget(self.toolbar)

	def onselect(self, verts):
		path = Path(verts)
		self.patch = patches.PathPatch(path, facecolor='red', lw=1)
		self.patch.set_alpha(0.5)
		self.canvas.axes.add_patch(self.patch)
		# plt.show()
		# self.contains_points = path.contains_points(self.rgb)
		# self.show_sample(self.rgb, (0,0,0))
		self.figure_2d.canvas.draw_idle()

	def select_lasso_area(self):
		self.lasso = LassoSelector(self.canvas.axes, self.onselect)
		self.cursor = Cursor(self.canvas.axes, 
			useblit=False, color='red', linewidth=0.5)
		# plt.show()

	def clear_axes(self):
		self.canvas.axes.clear()
		self.canvas.draw()

	def show_light_sample(self, data, **kwargs):
		self.canvas.axes.clear()
		self.canvas.axes.imshow(data, **kwargs)
		self.canvas.draw()
		self.canvas.show()

	def show_sample(self, data, bands, **kwargs):

		show_xaxis = True
		show_yaxis = True
		if 'show_xaxis' in kwargs:
			show_xaxis = kwargs.pop('show_xaxis')
		if 'show_yaxis' in kwargs:
			show_yaxis = kwargs.pop('show_yaxis')
		
		rgb_kwargs = {}
		for k in ['stretch', 'stretch_all', 'bounds']:
			if k in kwargs:
				rgb_kwargs[k] = kwargs.pop(k)

		imshow_kwargs = {'cmap': 'gray'}
		imshow_kwargs.update(kwargs)

		self.rgb = get_rgb(data, bands, **rgb_kwargs)

		if len(data.shape) == 2:
			self.rgb = self.rgb[:, :, 0]

		if show_xaxis == False:
			self.canvas.gca().xaxis.set_visible(False)
		if show_yaxis == False:
			self.canvas.gca().yaxis.set_visible(False)
		
		# ax = plt.imshow(self.rgb, **imshow_kwargs)
		self.canvas.axes.clear()
		self.canvas.axes.imshow(self.rgb, **imshow_kwargs)
		self.canvas.draw()
		self.canvas.show()