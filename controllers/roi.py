"""
	Tratado de ROIs con Pyqt5, Matplotlib y Numpy:
	Autor: Luis Quiroz Burga
"""
import math
from numpy import mean
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QTreeWidgetItem
from controllers.tools import show_message, confirm_message, to_int
from controllers.ui_controls import reset_canvas

class ROI():
	def __init__(self, mean_list, max_list, min_list, 
		plane_list, pixel_list, shape, name, id, color, verts,
		tag_coords):
		self.mean_list = mean_list
		self.max_list = max_list
		self.min_list = min_list
		self.plane_list = plane_list
		self.pixel_list = pixel_list
		self.shape = shape
		self.name = name
		self.id = id
		self.color = color
		self.verts = verts
		self.tag_coords = tag_coords

	def __str__(self):
		return 'ROI: {}'.format(str(self.name))

def verify_roi_name(name, roi_list):
	# Verifica si el nombre del ROI existe en la lista
	for roi in roi_list:
		if name == roi.name:
			show_message(icon=QMessageBox.Warning, title="Error en nueva ROI", 
				text="Existe una ROI con el nombre {}".format(name), 
				info="Por favor vuelva a guardar la ROI con un nombre diferente")
			return False
	return True

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
	# Puntos planos a matriz de coordenadas seleccionadas
	pixel_list = list()
	points = get_points(shape)
	for pixel in plane_list:
		pixel_list.append(points[pixel])
	return pixel_list

def write_in_file(file, pixel):
	# Escribe en el archivo
	for data in pixel:
		if data == pixel[-1]:
			file.write(str(round(data,3)))
		else:
			file.write(str(round(data,3)) + '\t')
	file.write('\n')

def get_y1_y2_list(pixel, max_list, min_list):
	# Obtener la lista de máximos y mínimos para gráfica
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

def get_ranges_data(pixel_list, image, scale_factor):
	# Obtengo los rangos de la gráfica: máximos, mínimos y medios
	max_list, min_list = [], []
	for px in pixel_list:
		pixel = image.read_pixel(px[1], px[0])*scale_factor
		get_y1_y2_list(pixel, max_list, min_list)
	mean_list = []
	for dx in range(len(max_list)):
		mean_list.append(mean((min_list[dx],max_list[dx])))
	return max_list, min_list, mean_list

def plot_spectra(image, roi, canvas, waves):
	# Plotea los datos en el Canvas
	canvas.axes.grid(True)
	canvas.axes.fill_between(waves, roi.max_list, roi.min_list,
                     color=roi.color, alpha=.3)
	canvas.axes.plot(waves, roi.mean_list, color=roi.color, label=roi.name, lw=2)
	canvas.axes.set_xlabel('Wavelength (nm)')
	# canvas.axes.set_ylabel('Intensidad')
	canvas.axes.legend()
	canvas.show()
	canvas.draw()

def refresh_roi_to_tree(roi_list, RT):
	RT.clear()
	for roi in roi_list:
		R = QTreeWidgetItem(RT,[roi.name,None, str(roi.id)])
		R.setCheckState(0, QtCore.Qt.Checked)
		R.setBackground(1,QtGui.QBrush(QtGui.QColor(roi.color)))
		r = QTreeWidgetItem(R,['Bandas', str(roi.shape[2])])
		r = QTreeWidgetItem(R,['Rango', str(roi.shape[2])])
		r = QTreeWidgetItem(R,['Píxeles', str(len(roi.pixel_list))])

def save_roi_to_list(image, name, plane_list, 
		shape, roi_list, roi_tree, id, 
		color, scale_factor, verts, tag_coords):
	pixel_list = plane_to_matrix_inds(plane_list, shape)
	max_list, min_list, mean_list = get_ranges_data(pixel_list, image, scale_factor)
	roi = ROI(plane_list=plane_list, shape=shape, pixel_list=pixel_list,
		max_list=max_list, min_list=min_list, mean_list=mean_list,
		name=name, id=id, color=color, verts=verts, tag_coords=tag_coords)
	roi_list.append(roi)
	refresh_roi_to_tree(roi_list, roi_tree)

def save_roi_file(path, roi, image, scale_factor):
	file = open(path + '/' + roi.name + '.roi.txt','w')
	for ind in range(1, roi.shape[2]+1):
		if ind == range(1, roi.shape[2]+1)[-1]:
			file.write('B' + str(ind))
		else:
			file.write('B' + str(ind) + '\t')
	file.write('\n')
	for px in roi.pixel_list:
		pixel = image.read_pixel(px[1],px[0])*scale_factor
		pixel = to_int(pixel)
		write_in_file(file, pixel)
	file.close()

def save_roi_data(image, roi_list, scale_factor):
	path = QFileDialog.getExistingDirectory(None, "Seleccione el folder destino", "")
	if path:
		for roi in roi_list:
			confirm = confirm_message(title="Guardando Información", 
						text="Guardar ROI \"{}\"".format(roi.name), 
						info="Por favor espere")
			if confirm:
				save_roi_file(path, roi, image, scale_factor)
		show_message(icon=QMessageBox.Information, title="Guardado con éxito", 
			text="Las regiones de interés fueron guardadas con éxito", info=""
		)
	
def get_roi_by_item_list(roi_list, text):
	for roi in roi_list:
		if roi.name == text:
			return roi

def ploting_rois(rois_tree, roi_list, image, canvas, waves):
	reset_canvas(canvas)
	if rois_tree.topLevelItemCount() == 0:
		show_message(icon=QMessageBox.Warning, title="Regiones de Interés Vacías", 
					text="Guarde y seleccione las Regiones de Interés que desee graficar.", info="")
	for index in range(rois_tree.topLevelItemCount()):
		top_item = rois_tree.topLevelItem(index)
		if top_item.checkState(0) == 2:
			roi = get_roi_by_item_list(roi_list, top_item.text(0))
			plot_spectra(image, roi, canvas, waves)

def tag_roi(graph_2d_view, text, tag_coords=False):
	if not tag_coords:
		tag_coords = graph_2d_view.tag_coords
	graph_2d_view.canvas.axes.annotate(text,
	    xy=(tag_coords[0], tag_coords[1]),
	    color='w',fontsize=9)
	graph_2d_view.canvas.draw_idle()

def save_and_graph_roi_mean(self, text):
	if verify_roi_name(text, self.roi_list):
		self.roi_list_number = self.roi_list_number + 1
		tag_roi(self.graph_2d_view, text)
		save_roi_to_list(
			image=self.sample_image,
			name=text,
			plane_list=self.graph_2d_view.lasso_plane_list, 
			shape=self.graph_2d_view.shape,
			roi_list=self.roi_list,
			roi_tree=self.rois_tree_widget,
			id=self.roi_list_number,
			color=self.graph_2d_view.actual_color,
			scale_factor=self.scale_factor,
			verts=self.graph_2d_view.verts,
			tag_coords=self.graph_2d_view.tag_coords
		)
		ploting_rois(
			self.rois_tree_widget, self.roi_list,
			self.sample_image,self.graph_plot_view.canvas,
			self.waves
		)

def paint_rois(graph_2d_view, roi_list):
	for roi in roi_list:
		graph_2d_view.paint_roi(roi)
		tag_roi(graph_2d_view, roi.name, roi.tag_coords)
