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
from controllers.ui_controls import (show_sample_info, set_bands_sliders,
	get_sliders_values, set_up_initial_values, set_2d_canvas,
	set_wavelenth_sliders,enable_disabled_controls,)
from controllers.variables import (TRUE_COLOR,)

settings.WX_GL_DEPTH_SIZE = 16


def load_sample(self):
	self.sample_image = open_image(self.sample_path)
	set_bands_sliders(self, TRUE_COLOR)
	metadata_info = get_info(self.sample_image)
	show_sample_info(self, metadata_info)
	set_2d_canvas(self)
	self.enable = True
	enable_disabled_controls(self)

def render_sample(self):
	self.sample_path, _ = QtWidgets.QFileDialog.getOpenFileName(
		None, "Seleccione la Muestra", 
		"","HSI Data (*.hdr)"
	)
	if self.sample_path:
		threading.Thread(target=load_sample(self)).start()

def spectral_imshow():
	import os
	command = 'python threading/pixel.py ' + SAMPLE_PATH
	os.system(command)

def pixel_analytic(self):
	threading.Thread(target=spectral_imshow).start()

def render_hypercube(self):
	view_cube(self.sample_image)

def slider_rgb(self):
	self.rgb_bands = get_sliders_values(self)
	self.rgb_wavelength = get_sliders_values(self)
	set_2d_canvas(self)

def change_rgb_values(self):
	rgb = get_bands_sliders(self)
	if not self.combo_bands_flag:
		rgb = tuple(map(band_wavelength_convert, rgb))
	self.red_band.setText(str(rgb[0]))
	self.green_band.setText(str(rgb[1]))
	self.blue_band.setText(str(rgb[2]))

def lasso_selector_actived(self):
	self.graph_2d_view.select_lasso_area()

def combo_mode_activaded(self, text):
	self.combo_bands_flag = False

	if text == 'Bandas':
		self.combo_bands_flag = True

	if self.combo_bands_flag:
		self.mode_title.setText('Número de Bandas:')
		if self.sample_image:
			self.nbands.setText(str(self.sample_image.nbands))
		set_bands_sliders(self)
	else:
		self.mode_title.setText('Longitud de Onda:')
		if self.sample_image:
			wave_range = str(self.sample_image.metadata['wavelength'][0] + '-' + self.sample_image.metadata['wavelength'][-1] + ' (nm)')
			self.nbands.setText(wave_range)
		set_wavelenth_sliders(self)

def setupUi_definitions(self):
	self.button_open_sample.clicked.connect(self._render_sample)
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

def main_ui(Ui_MainWindow):
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