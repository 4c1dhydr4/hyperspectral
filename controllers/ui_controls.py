# Autor: Luis Quiroz Burga
from controllers.variables import (TRUE_COLOR,)
from controllers.sliders import (sliders_def, get_sliders_values)
from controllers.bands import get_bands

def enable_disabled_controls(self):
	# Desactivar/Activar controles de Interfaz
	if self.enable:
		self.combo_mode.setEnabled(True)
		self.slider_red_band.setEnabled(True)
		self.slider_green_band.setEnabled(True)
		self.slider_blue_band.setEnabled(True)
		self.button_3d_hypercube.setEnabled(True)
		self.button_pixel_analityc.setEnabled(True)
		self.lasso_button.setEnabled(True)
	else:
		self.combo_mode.setEnabled(False)
		self.slider_red_band.setEnabled(False)
		self.slider_green_band.setEnabled(False)
		self.slider_blue_band.setEnabled(False)
		self.button_3d_hypercube.setEnabled(False)
		self.button_pixel_analityc.setEnabled(False)
		self.lasso_button.setEnabled(False)
		self.export_roi_button.setEnabled(False)
		self.graph_profile_button.setEnabled(False)
		self.add_roi_button.setEnabled(False)

def combo_mode_def_items(self):
	# Seteo de Combo de Modo Bands/Wavelength
	self.combo_mode.addItem("Bandas")
	self.combo_mode.addItem("Wavelength")

def show_sample_info(self, metadata_info):
	# Mostrar Información de la cabecera
	self.text_browser_info.clear()
	self.text_browser_info.append(metadata_info)

def set_2d_canvas(self):
	# Setear imagen de la muestra en el Canvas Matplotlib
	self.graph_2d_view.clear_axes()
	self.graph_2d_view.show_sample(self.sample_image, self.rgb_bands)

def set_up_initial_values(self):
	# Setear valores iniciales de la interfaz
	self.combo_bands_flag = True
	self.sample_image = False
	self.enable = False
	self.rgb_bands  = (0,0,0)
	self.rgb_wavelength = (0,0,0)
	self.graph_2d_view.clear_axes()
	self.graph_plot_view.clear_axes()
	self.text_browser_info.clear()
	self.roi_list = []
	self.roi_list_number = 0
	self.rois_tree_widget.setHeaderLabels(['Nombre','ID','Color'])
	self.rois_tree_widget.setAlternatingRowColors(True)
	enable_disabled_controls(self)
	sliders_def(self)
	combo_mode_def_items(self)
