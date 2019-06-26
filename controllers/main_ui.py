"""
	Definición de Funciones:
	Ante cambios en la interfaz gráfica:
	*from functions_definition import definitions, select_image
	*Colocar la función definitions al final de la función setupUi de la clase Ui_MainWindow
	*importar funcionalidad en la interfaz
	Autor: Luis Quiroz Burga
"""

import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from spectral import (settings, open_image, view_cube, imshow)
from controllers.tools import (get_info,band_wavelength_convert)
from controllers.ui_controls import (show_sample_info,
	set_up_initial_values, set_2d_canvas, enable_disabled_controls,)
from controllers.variables import (TRUE_COLOR,)
from controllers.sliders import (set_sliders,  get_sliders_values, set_rgb_text_values)
from controllers.bands import (get_bands,)
from controllers.roi import load_roi_data, plot_spectra, plane_to_matrix_inds

settings.WX_GL_DEPTH_SIZE = 16

SAMPLE_PATH = ''

def load_sample(self):
	# Cargar datos del Hipercubo
	self.sample_image = open_image(self.sample_path)
	metadata_info = get_info(self.sample_image)
	show_sample_info(self, metadata_info)
	set_sliders(self, TRUE_COLOR)
	self.rgb_bands = TRUE_COLOR
	set_2d_canvas(self)
	self.enable = True
	enable_disabled_controls(self)

def render_sample(self, test=False):
	# Obtención del PATH de la muestra
	if not test:
		self.sample_path, _ = QtWidgets.QFileDialog.getOpenFileName(
			None, "Seleccione la Muestra", 
			"","HSI Data (*.hdr)"
		)
	if self.sample_path:
		global SAMPLE_PATH
		SAMPLE_PATH = self.sample_path
		threading.Thread(target=load_sample(self)).start()

def spectral_imshow():
	# Apertura de análisis individual de pixeles
	import os
	command = 'python threading/pixel.py ' + SAMPLE_PATH
	os.system(command)

def pixel_analytic(self):
	# Apertura de análisis individual de pixeles abriendo un thread 
	threading.Thread(target=spectral_imshow).start()

def render_hypercube(self):
	# Apertura de la visualización en 3D del hipercubo
	view_cube(self.sample_image)

def slider_rgb(self):
	# Graficar hipercubo en 2D
	get_bands(self)
	set_sliders(self)
	set_2d_canvas(self)

def change_rgb_values(self):
	# Setear texbox con los valores de los sliders
	set_rgb_text_values(self, get_sliders_values(self))

def lasso_selector_actived(self):
	# Uso del Lasso selector de Matplotlib para seleccionar pixeles
	self.graph_2d_view.shape = self.sample_image.shape
	self.graph_2d_view.select_lasso_area()
	self.export_roi_button.setEnabled(True)
	self.graph_profile_button.setEnabled(True)

def roi_save(self):
	# Callback para guardar la información en txt de los pixeles seleccionados
	load_roi_data(
		image=self.sample_image,
		plane_list=self.graph_2d_view.lasso_plane_list, 
		shape=self.graph_2d_view.shape,
		canvas=self.graph_plot_view.canvas,
	)

def graph_spectra(self):
	pixel_list = plane_to_matrix_inds(
		self.graph_2d_view.lasso_plane_list, 
		self.graph_2d_view.shape,
	)
	plot_spectra(
		self.sample_image, 
		pixel_list,
		self.graph_plot_view.canvas
	)

def combo_mode_activaded(self, text):
	# Activar el modo Bands/Wavelength
	self.combo_bands_flag = False
	if text == 'Bandas':
		self.combo_bands_flag = True
	set_sliders(self)

def load_test(self):
	# Cargar ´hipercubo de prueba
	self.sample_path = 'D:\\Hypercubes\\HARC000.bil.hdr'
	render_sample(self, test=True)

def setupUi_definitions(self):
	# Setear funciones a controles de interfaz 
	self.button_open_sample.clicked.connect(self._render_sample)
	self.button_fast_test.clicked.connect(self._load_test)
	self.button_pixel_analityc.clicked.connect(self._pixel_analytic)
	self.button_3d_hypercube.clicked.connect(self._render_hypercube)
	self.slider_red_band.sliderReleased.connect(self._slider_rgb)
	self.slider_green_band.sliderReleased.connect(self._slider_rgb)
	self.slider_blue_band.sliderReleased.connect(self._slider_rgb)
	self.slider_red_band.sliderPressed.connect(self._slider_rgb)
	self.slider_green_band.sliderPressed.connect(self._slider_rgb)
	self.slider_blue_band.sliderPressed.connect(self._slider_rgb)
	self.slider_red_band.valueChanged.connect(self._change_rgb_values)
	self.slider_green_band.valueChanged.connect(self._change_rgb_values)
	self.slider_blue_band.valueChanged.connect(self._change_rgb_values)
	self.lasso_button.clicked.connect(self._lasso_selector_actived)
	self.combo_mode.activated[str].connect(self._combo_mode_activaded)     
	self.export_roi_button.clicked.connect(self._roi_save)
	self.graph_profile_button.clicked.connect(self._graph_spectra)

def main_ui(Ui_MainWindow):
	# Definición principal del software
	import sys
	import wx
	app = wx.App(False)
	gui_app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow
	ui.setupUi(MainWindow)
	set_up_initial_values(ui)
	print("Hyperspectral UPN is Running")
	MainWindow.show()
	sys.exit(gui_app.exec_())