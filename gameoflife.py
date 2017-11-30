# Simple game of life implementation for a square matrix

import matrixdisplay
import frame
import numpy 
import random
import time

class GameOfLife:

	def __init__(self, display, color=(250, 255, 30), T=200):
		self._display = display
		self._N = self._display.get_dim()
		self._old_grid = numpy.zeros((self._N, self._N, 1), dtype='i')
		self._new_grid = numpy.zeros((self._N, self._N, 1), dtype='i')
							#np.zeros( (dim, dim, 3), dtype=np.uint8 )
		self._color = color
		self._T = T

		# Create random initial configuration 
		for i in range(0, self._N):
			for j in range(0, self._N):
				if(random.randint(0, 100) < random.randint(15, 25)):
					self._old_grid[i][j] = 1
				else:
					self._old_grid[i][j] = 0

	def live_neigbours(self, i, j):
		s = 0 # Total number of live neighbors 
		for x in [i-1, i, i+1]:
			for y in [j-1, j, j+1]:
				if(x == i and y == j):
					continue
				if(x != self._N and y != self._N):
					s += self._old_grid[x][y]
				elif(x == self._N and y != self._N):
					s += self._old_grid[0][y]
				elif(x != self._N and y == self._N):
					s += self._old_grid[x][0]
				else:
					s += self._old_grid[0][0]
		return s

	def play(self):
		print 'now Playing'
		t = 1 # Current time level
		write_frequency = 5 # How frequently the output gets drawn 
		while(t <= self._T):
			#print self._T, '----------------------------------'
			#print self._old_grid

			for i in range(self._N):
				for j in range(self._N):
					live = self.live_neigbours(i, j)
					if(self._old_grid[i][j] == 1 and live < 2):
						self._new_grid[i][j] = 0 # Dead from starvation 
					if(self._old_grid[i][j] == 1 and (live == 2 or live == 3)):
						self._new_grid[i][j] = 1 # Continue living
					if(self._old_grid[i][j] == 1 and live > 3):
						self._new_grid[i][j] = 0 # Dead from overcrowding
					if(self._old_grid[i][j] == 0 and live == 3):
						self._new_grid[i][j] = 1 # Alive from reproduction 
			
			# Draw frame on display
			#if(t % write_frequency == 0):
			if True:
				fr = frame.Frame(self._N)
				for x in range(0, self._N):
					for y in range(0, self._N):
						if (self._old_grid[x][y] == 1):
							fr.set_pixel(x, y, self._color)
				self._display.draw_frame(fr)
				#time.sleep(0.5)

			self._old_grid = self._new_grid.copy()
			t += 1		

