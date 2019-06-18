from controllers.sliders import get_sliders_values
from controllers.tools import (wavelength_band_convert,)


def get_bands(self):
	sliders_values = get_sliders_values(self)
	if not self.combo_bands_flag:
		self.rgb_bands = tuple(map(wavelength_band_convert, sliders_values))
	else:
		self.rgb_bands = sliders_values
