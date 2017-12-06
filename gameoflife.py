# Simple game of life implementation for a square matrix

import matrixdisplay
from neopixel import *
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
		self._color = color
		self._T = T
		self._strip = self._display.get_strip()

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

	def px_to_string(self, x, y):
		return (x % 8 + y % 8 *8) + x/8 * 64 + y/8 *128

	def play(self):
		r, g, b = self._color
		print 'now Playing'
		t = 1 # Current time level
		write_frequency = 5 # How frequently the output gets drawn 
		while(t <= self._T):
			stillAllive = 0
			for i in range(self._N):
				for j in range(self._N):
					live = self.live_neigbours(i, j)
					if(self._old_grid[i][j] == 1 and live < 2):
						self._new_grid[i][j] = 0 # Dead from starvation 
						self._strip.setPixelColor( self.px_to_string(i, j), Color(0, 0, 255) )
						stillAllive += 1
					if(self._old_grid[i][j] == 1 and (live == 2 or live == 3)):
						self._new_grid[i][j] = 1 # Continue living
						self._strip.setPixelColor( self.px_to_string(i, j), Color(r, g, b) )
						#stillAllive += 1
					if(self._old_grid[i][j] == 1 and live > 3):
						self._new_grid[i][j] = 0 # Dead from overcrowding
						self._strip.setPixelColor( self.px_to_string(i, j), Color(0, 0, 255) )
						stillAllive += 1
					if(self._old_grid[i][j] == 0 and live == 3):
						self._new_grid[i][j] = 1 # Alive from reproduction 
						self._strip.setPixelColor( self.px_to_string(i, j), Color(r, g, b) )
						stillAllive += 1		
			#time.sleep(0.2)			

			if(stillAllive == 0):
				return # Return when it has died out changing 
			self._display._write_out_buffer()
			self._old_grid = self._new_grid.copy()
			t += 1		

