import math

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

import statistics as st
def plot_spectra(image, pixel_list, canvas):
	canvas.axes.clear()
	canvas.axes.grid(True)
	profiles = list()
	for px in pixel_list:
		# profiles.append(image.read_pixel(px[0],px[1]))
		# canvas.axes.plot(profiles)
		canvas.axes.plot(image.read_pixel(px[0],px[1]))
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
