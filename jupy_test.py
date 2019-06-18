import pandas as pd
import os
from matplotlib import pyplot as plt
from spectral import *

# PROJ_DIR = os.path.dirname(os.getcwd())
PROJ_DIR = os.getcwd()
SAMPLES_DIR = os.path.join(PROJ_DIR, 'samples')
SAMPLE_FILE = SAMPLES_DIR + '\\HARC000.bil.hdr'
# SAMPLE_FILE = SAMPLES_DIR + '\\M9L1.bil.hdr'

SAMPLE = open_image(SAMPLE_FILE)

