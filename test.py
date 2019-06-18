import pdb

import os
import numpy as np
from matplotlib.widgets import LassoSelector
from matplotlib.path import Path


from spectral import open_image, imshow, get_rgb
import matplotlib.pyplot as plt
import matplotlib.image as img
import matplotlib.cm as cm
from spectral import *



PROJ_DIR = os.getcwd()
SAMPLES_DIR = os.path.join(PROJ_DIR, 'samples')
sample = SAMPLES_DIR + '\\HARC000.bil.hdr'

image = open_image(sample) #.load()
bands = (70,70,30)
fig, ax = plt.subplots()
rgb = get_rgb(image, bands)
im = ax.imshow(rgb)
plt.draw()
plt.show()
pdb.set_trace()
print(image)
x = input()






# im = imshow(s.load(), bands)









# data = s.read_bands(bands)
# im = imshow(s.load(), bands)


# plt.show()

# plt.imshow(s.read_band(0))

# settings.WX_GL_DEPTH_SIZE = 16
# sample = SAMPLES_FOLDER + 'HARC000.bil.hdr'
# sample = 'HARC000.bil.hdr'
# view = imshow(img, (80, 69, 57))
# view_cube(img)
# x = input()


# print(img)
# print(view)

# save_rgb('rgb.jpg', img, [80, 69, 57])
