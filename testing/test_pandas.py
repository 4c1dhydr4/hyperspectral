import pandas as pd

roi = pd.read_csv('test.roi.txt',sep='\t')
print(roi['band_0'])