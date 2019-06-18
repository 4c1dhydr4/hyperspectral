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
	return info

def band_wavelength_convert(band):
	return band*8

def band_wavelength_convert(band):
	return round(band/8,0)