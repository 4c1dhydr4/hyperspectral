from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import LassoSelector, Cursor
from matplotlib.path import Path
from matplotlib import patches as patches
from spectral import *
from controllers.roi import verts_normalization, get_points, get_pixel_list
from controllers.tools import get_rand_color, get_central_point
import random

class graph_2d_view(QWidget):
	
	def __init__(self, parent = None):

		QWidget.__init__(self, parent)
		self.figure_2d = Figure(frameon=False)
		self.canvas = FigureCanvas(self.figure_2d)
		vertical_layout = QVBoxLayout()
		vertical_layout.addWidget(self.canvas)
		self.canvas.axes = self.figure_2d.add_axes([0, 0, 1, 1])
		self.toolbar = NavigationToolbar(self.canvas, self)
		self.setLayout(vertical_layout)
		self.canvas.axes.clear()
		self.canvas.axes.set_axis_off()
		self.canvas.draw()
		self.layout().addWidget(self.toolbar)

	def onselect(self, verts):
		self.verts = verts_normalization(verts)
		path = Path(self.verts)
		self.tag_coords = get_central_point(self.verts)
		self.actual_color = get_rand_color()
		self.patch = patches.PathPatch(path, 
			facecolor=self.actual_color, lw=1,)
		self.patch.set_alpha(0.5)
		points = get_points(self.shape)
		self.grid = self.patch.contains_points(points, radius=1e-9)
		self.lasso_plane_list = get_pixel_list(self.grid)
		self.canvas.axes.add_patch(self.patch)
		self.figure_2d.canvas.draw_idle()

	def paint_roi(self, roi):
		verts = verts_normalization(roi.verts)
		path = Path(verts)
		tag_coords = get_central_point(verts)
		actual_color = roi.color
		patch = patches.PathPatch(path, 
			facecolor=actual_color, lw=1,)
		patch.set_alpha(0.5)
		points = get_points(roi.shape)
		self.canvas.axes.add_patch(patch)
		self.figure_2d.canvas.draw_idle()

	def select_lasso_area(self):
		self.lasso_plane_list = list()
		lasso_props = {'color':'red','linewidth':0.5,'alpha':1}
		self.lasso = LassoSelector(self.canvas.axes, self.onselect, lineprops=lasso_props)
		self.cursor = Cursor(self.canvas.axes, 
			useblit=False, color='red', linewidth=0.5)
		# plt.show()

	def clear_axes(self):
		self.canvas.axes.clear()
		self.canvas.draw()

	def show_light_sample(self, image, rgb_bands, **kwargs):
		rgb = image.read_band(rgb_bands)
		# Shit happens
		self.canvas.axes.clear()
		self.canvas.axes.imshow(rgb, **kwargs)
		self.canvas.axes.set_axis_off()
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

		imshow_kwargs = {
			'cmap': 'gray',
			'origin': 'upper',
			'aspect': 'equal',
		}
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
		self.canvas.axes.set_axis_off()
		self.canvas.draw()
		self.canvas.show()