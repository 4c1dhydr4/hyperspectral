import math

def verts_normalization(verts):
	# normalizo los vertices a flotantes sin decimales.
	# Aqui me quedé
	# Aqui me quedé
	# Aqui me quedé
	# Aqui me quedé
	# Aqui me quedé
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

def load_roi_data(plane_list, shape):
	pixel_list = plane_to_matrix_inds(plane_list, shape)
	print(pixel_list)