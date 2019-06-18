from PyQt5 import QtWidgets
from controllers.variables import (TRUE_COLOR,)

def enable_disabled_controls(self):
	if self.enable:
		self.combo_mode.setEnabled(True)
		self.slider_red_band.setEnabled(True)
		self.slider_green_band.setEnabled(True)
		self.slider_blue_band.setEnabled(True)
		self.button_3d_hypercube.setEnabled(True)
		self.button_pixel_analityc.setEnabled(True)
		self.lasso_button.setEnabled(True)
		self.rectangle_button.setEnabled(True)
	else:
		self.combo_mode.setEnabled(False)
		self.slider_red_band.setEnabled(False)
		self.slider_green_band.setEnabled(False)
		self.slider_blue_band.setEnabled(False)
		self.button_3d_hypercube.setEnabled(False)
		self.button_pixel_analityc.setEnabled(False)
		self.lasso_button.setEnabled(False)
		self.rectangle_button.setEnabled(False)

def combo_mode_def_items(self):
	self.combo_mode.addItem("Bandas")
	self.combo_mode.addItem("Wavelength")

def sliders_def(self):
	if self.combo_bands_flag:
		self.slider_red_band.setRange(0,150)
		self.slider_green_band.setRange(0,150)
		self.slider_blue_band.setRange(0,150)
	else:
		self.slider_red_band.setRange(0,1192)
		self.slider_green_band.setRange(0,1192)
		self.slider_blue_band.setRange(0,1192)
	self.red_band.setText(str(0))
	self.green_band.setText(str(0))
	self.blue_band.setText(str(0))

def show_sample_info(self, metadata_info):
	self.text_browser_info.clear()
	self.text_browser_info.append(metadata_info)

def set_wavelenth_sliders(self):
	if self.sample_image:
		nbands = self.sample_image.nbands
		wavelengths = self.sample_image.metadata['wavelength']
		self.slider_red_band.setRange(0,float(wavelengths[nbands-1]))
		self.slider_green_band.setRange(0,float(wavelengths[nbands-1]))
		self.slider_blue_band.setRange(0,float(wavelengths[nbands-1]))
		self.slider_red_band.setSingleStep(8)
		self.slider_green_band.setSingleStep(8)
		self.slider_blue_band.setSingleStep(8)

def set_bands_sliders(self, bands=False):
	nbands = int(self.sample_image.nbands)
	if not bands:
		bands = get_sliders_values(self)
	self.slider_red_band.setTickPosition(QtWidgets.QSlider.TicksBelow)
	self.slider_green_band.setTickPosition(QtWidgets.QSlider.TicksBelow)
	self.slider_blue_band.setTickPosition(QtWidgets.QSlider.TicksBelow)
	self.slider_red_band.setRange(0,nbands-1)
	self.slider_green_band.setRange(0,nbands-1)
	self.slider_blue_band.setRange(0,nbands-1)
	self.slider_red_band.setValue(bands[0])
	self.slider_green_band.setValue(bands[1])
	self.slider_blue_band.setValue(bands[2])
	interval = 1
	if not self.combo_bands_flag:
		interval = 8
	self.slider_red_band.setTickInterval(interval)
	self.slider_green_band.setTickInterval(interval)
	self.slider_blue_band.setTickInterval(interval)


def get_sliders_values(self):
	r = self.slider_red_band.value()
	g = self.slider_green_band.value()
	b = self.slider_blue_band.value()
	if not self.combo_bands_flag:
		r = int(round(r/8,0))
		g = int(round(g/8,0))
		b = int(round(b/8,0))
	return (r, g, b)


def set_2d_canvas(self):
	self.graph_2d_view.clear_axes()
	self.graph_2d_view.show_sample(self.sample_image, get_sliders_values(self))

def set_up_initial_values(self):
	self.combo_bands_flag = True
	self.sample_image = False
	self.enable = False
	enable_disabled_controls(self)
	sliders_def(self)
	combo_mode_def_items(self)
