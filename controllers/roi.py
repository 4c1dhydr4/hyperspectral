"""
	Tratado de ROIs con Pyqt5, Matplotlib y Numpy:
	Autor: Luis Quiroz Burga
"""
import math
from numpy import mean

class ROI():
	def __init__(self, mean_list, max_list, min_list, 
		plane_list, pixel_list, shape, name):
		self.mean_list = mean_list
		self.max_list = max_list
		self.min_list = min_list
		self.plane_list = plane_list
		self.pixel_list = pixel_list
		self.shape = shape
		self.name = name

	def __str__(self):
		return 'ROI: {}'.format(str(self.name))

def verts_normalization(verts):
	# Normalizo los vertices a flotantes sin decimales.
	new_verts = list()
	for vert in verts:
		new_verts.append((round(vert[0]),round(vert[1])))
		# new_verts.append((round(vert[0]),round(vert[1])))
	return new_verts

def get_points(shape):
	# Obtengo una matriz de puntos del tamaño de la imágen
	points_x = range(shape[0]) 
	points_y = range(shape[1]) 
	points = list()
	for px in points_x:
		for py in points_y:
			points.append([py,px])
	return points

def get_pixel_list(grid):
	# Obtengo la lista de pixeles (plano)
	pixel = 0
	pixel_list = list()
	for x in grid:
		if x:
			pixel_list.append(pixel)
		pixel = pixel+1
	return pixel_list

def plane_to_matrix_inds(plane_list, shape):
	pixel_list = list()
	points = get_points(shape)
	for pixel in plane_list:
		pixel_list.append(points[pixel])
	return pixel_list

def write_in_file(file, pixel):
	for data in pixel:
		file.write(str(round(data,3)) + '\t')
	file.write('\n')

def get_y1_y2_list(pixel, max_list, min_list):
	ind = 0
	for data in pixel:
		try:
			if data>=max_list[ind]:
				max_list[ind] = data
		except Exception as e:
			max_list.append(data)
		try:
			if data<=min_list[ind]:
				min_list[ind] = data
		except Exception as e:
			min_list.append(data)
		ind = ind + 1

def get_ranges_data(pixel_list, image):
	max_list, min_list = [], []
	for px in pixel_list:
		pixel = image.read_pixel(px[1], px[0])
		get_y1_y2_list(pixel, max_list, min_list)
	mean_list = []
	for dx in range(len(max_list)):
		mean_list.append(mean((min_list[dx],max_list[dx])))
	return max_list, min_list, mean_list

def plot_spectra(image, pixel_list, canvas):
	canvas.axes.clear()
	canvas.axes.grid(True)
	profiles = list()
	max_list, min_list, mean_list = get_ranges_data(pixel_list, image)
	canvas.axes.fill_between(range(len(mean_list)), max_list, min_list,
                     color='r', alpha=.5)
	canvas.axes.plot(mean_list, 'r')
	canvas.axes.set_xlabel('Bandas')
	canvas.axes.set_ylabel('Intensidad')
	canvas.show()
	canvas.draw()

def save_roi_to_list(image, name, plane_list, shape, roi_list):
	pixel_list = plane_to_matrix_inds(plane_list, shape)
	max_list, min_list, mean_list = get_ranges_data(pixel_list, image)
	roi = ROI(plane_list=plane_list, shape=shape, pixel_list=pixel_list,
		max_list=max_list, min_list=min_list, mean_list=mean_list,
		name=name)

	Aqui me quedé

	roi_list.append(roi)

def save_roi_data(image, plane_list, shape, canvas, roi_list):
	pixel_list = plane_to_matrix_inds(plane_list, shape)
	file = open('test.txt','w')
	print(shape[2])
	for ind in range(1,shape[2]+1):
		file.write(str(ind) + '\t')
	file.write('\n')
	for px in pixel_list:
		pixel = image.read_pixel(px[0],px[1])
		write_in_file(file, pixel)
	file.close()
