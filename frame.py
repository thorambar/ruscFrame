# Simple definition of a frame, basicly a matrix, maybe overkill, but hey
# Thorambar Dae Rusc 2017

import numpy as np

class Frame:
	
	def __init__(self, dim):
		self._matrix = np.zeros( (dim, dim, 3), dtype=np.uint8 )
		self._dim = dim

	def init(self):
		self._matrix = np.zeros( (self._dim, self._dim, 3), dtype=np.uint8 )

	def deinit(self):
		# Empty, maybe need to free space after destruction idk.
		return 
		
	def __enter__(self):
		self.init()
		return self

	def __exit__(self, exception_type, exception_value, traceback):
		self.deinit()

	def set_pixel(self, x, y, color):
		self._matrix[x][y] = color

	def set_pixel_list(self, list):
		# May be the better alternative to get_matrix but also a bit cumbersome 
		for elem in list:
			x, y, color = elem
			self._matrix[x][y] = color

	def get_matrix_(self):
		# Basically should not be used, maybe gets removed, but also maybe faster, TODO test it
		return sellf._matrix

	def get_pixel(self, x, y):
		return self._matrix[x][y]
