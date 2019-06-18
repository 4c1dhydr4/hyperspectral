from PyQt5 import QtWidgets

def sliders_def(self, rgb=(0,0,0)):
	# Definición de Sliders y Text Box Values
	if self.combo_bands_flag:
		self.slider_red_band.setRange(0,150)
		self.slider_green_band.setRange(0,150)
		self.slider_blue_band.setRange(0,150)
	else:
		self.slider_red_band.setRange(0,1192)
		self.slider_green_band.setRange(0,1192)
		self.slider_blue_band.setRange(0,1192)
	self.red_text_box.setText(str(rgb[0]))
	self.green_text_box.setText(str(rgb[1]))
	self.blue_text_box.setText(str(rgb[2]))

def get_sliders_values(self):
	# Obtener los valores de los sliders
	r = self.slider_red_band.value()
	g = self.slider_green_band.value()
	b = self.slider_blue_band.value()
	return (r, g, b)


def set_sliders_range(self, Y):
	self.slider_red_band.setRange(0,Y)
	self.slider_green_band.setRange(0,Y)
	self.slider_blue_band.setRange(0,Y)

def set_trick_position_sliders(self):
	self.slider_red_band.setTickPosition(QtWidgets.QSlider.TicksBelow)
	self.slider_green_band.setTickPosition(QtWidgets.QSlider.TicksBelow)
	self.slider_blue_band.setTickPosition(QtWidgets.QSlider.TicksBelow)

def set_values_sliders(self, values):
	self.slider_red_band.setValue(values[0])
	self.slider_green_band.setValue(values[1])
	self.slider_blue_band.setValue(values[2])

def set_trick_interval(self, interval):
	self.slider_red_band.setTickInterval(interval)
	self.slider_green_band.setTickInterval(interval)
	self.slider_blue_band.setTickInterval(interval)

def set_single_step_sliders(self, value):
	self.slider_red_band.setSingleStep(value)
	self.slider_green_band.setSingleStep(value)
	self.slider_blue_band.setSingleStep(value)

def set_rgb_text_values(self, values):
	self.red_text_box.setText(str(values[0]))
	self.green_text_box.setText(str(values[1]))
	self.blue_text_box.setText(str(values[2]))



def set_sliders(self, values=False):
	# Setear sliders para el modo Bands
	if self.sample_image:
		nbands = int(self.sample_image.nbands)
	else:
		nbands = 1
	
	if self.combo_bands_flag:
		self.mode_title.setText('Número de Bandas:')
		interval = 4
		set_sliders_range(self, nbands-1)
		set_single_step_sliders(self, 8)
		mode_text = str(nbands)
	else:
		self.mode_title.setText('Longitud de Onda:')
		interval = 64
		if self.sample_image:
			set_sliders_range(self, float(self.sample_image.metadata['wavelength'][nbands-1]))
			meta = self.sample_image.metadata['wavelength']
			mode_text = str(meta[0] + '-' + meta[-1] + ' (nm)')
		set_single_step_sliders(self, 32)

	if values:
		set_rgb_text_values(self, values)

	self.nbands.setText(mode_text)
	set_trick_interval(self, interval)
	set_trick_position_sliders(self)