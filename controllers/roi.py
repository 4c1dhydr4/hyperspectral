import math
from numpy import mean

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

def get_x_y1_y2_list(pixel, max_list, min_list):
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

def plot_spectra(image, pixel_list, canvas):
	canvas.axes.clear()
	canvas.axes.grid(True)
	profiles = list()
	max_list, min_list = [], []
	for px in pixel_list:
		pixel = image.read_pixel(px[1], px[0])
		get_x_y1_y2_list(pixel, max_list, min_list)
	mean_list = []
	for dx in range(len(max_list)):
		mean_list.append(mean((min_list[dx],max_list[dx])))
	canvas.axes.fill_between(range(len(mean_list)), max_list, min_list,
                     color='r', alpha=.5)
	canvas.axes.plot(mean_list, 'r')
	canvas.axes.set_xlabel('Bandas')
	canvas.axes.set_ylabel('Intensidad')
	canvas.show()
	canvas.draw()

def load_roi_data(image, plane_list, shape, canvas):
	pixel_list = plane_to_matrix_inds(plane_list, shape)
	file = open('test.txt','w')
	for px in pixel_list:
		file.write(str(px[0])+ '\t' + str(px[1]) + '\t')
		pixel = image.read_pixel(px[0],px[1])
		write_in_file(file, pixel)
	file.close()
