import random

def get_waves(list_waves):
	new_list = []
	for item in list_waves:
		new_list.append(float(item))
	return new_list

def get_info(SAMPLE_IMAGE):
	info = ''
	m = SAMPLE_IMAGE.metadata
	if 'label' in m:
		info = info + 'Muesta: ' +  m['label'] + '\n'
	if 'interleave' in m:
		info = info + 'Interleave: ' +  m['interleave'] + '\n'
	if 'lines' in m:
		info = info + 'Lines: ' +  m['lines'] + '\n'
	if 'samples' in m:
		info = info + 'Samples: ' +  m['samples'] + '\n'
	if 'bands' in m:
		info = info + 'Bands: ' +  m['bands'] + '\n'
	info = info + 'Data Size: ' + str(int(m['lines'])*int(m['samples'])*int(m['bands'])) + '\n'
	if 'bit' in m:
		info = info + 'Bit Depth: ' +  m['bit depth'] + '\n'
	if 'shutter' in m:
		info = info + 'Shutter: ' +  m['shutter'] + '\n'
	if 'gain' in m:
		info = info + 'Gain: ' +  m['gain'] + '\n'
	if 'framerate' in m:
		info = info + 'Framerate: ' +  m['framerate'] + '\n'
	if 'reflectance scale factor'in m:
		info = info + 'Factor de Escala de Reflectancia: ' +  m['reflectance scale factor'] + '\n'
	if 'byte order'in m:
		info = info + 'Byte Order: ' +  m['byte order'] + '\n'
	if 'header offset'in m:
		info = info + 'Header Offset: ' +  m['header offset'] + '\n'
	if 'wavelength'in m:
		info = info + 'Wavelength: ' +  str(m['wavelength']) + '\n'
	return info, int(m['reflectance scale factor']), get_waves(m['wavelength'])

def band_wavelength_convert(band):
	return band*8

def wavelength_band_convert(band):
	return int(round(band/8,0))

def get_rand_color():
	return "#{:06x}".format(random.randint(0, 0xFFFFFF))

from PyQt5.QtWidgets import QMessageBox
def show_message(icon=QMessageBox.Warning, title="Mensaje", text="Texto", info="Extra Info"):
	msg = QMessageBox()
	msg.setIcon(icon)
	msg.setWindowTitle(title)
	msg.setText(text)
	msg.setInformativeText(info)
	msg.setStandardButtons(QMessageBox.Ok)
	ok = msg.exec_()

def get_central_point(points):
	x = [p[0] for p in points]
	y = [p[1] for p in points]
	return ((sum(x) / len(points))-2, (sum(y) / len(points))+1)

def to_int(list):
	int_list = []
	for item in list:
		int_list.append(int(item))
	return int_list