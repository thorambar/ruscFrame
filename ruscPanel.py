# The main class of the ruscPanel LED matrix display software
# Thorambar Dae Rusc 2017

import time
from random import randint

import frame
import matrixdisplay
import bitmapfont
import gameoflife
import random

from neopixel import *
import PIL as pil
from PIL import ImageFont, ImageDraw
import numpy as np

# ++++ Global vars +++++++++++++
DDIM = 16

def to_pix(image):
	img = image.resize((DDIM, DDIM)).convert('RGB') # AA maybe bad
	pixels = frame.Frame(DDIM) # 8 bit for 0-255 values of RGB
	for i in range(0, DDIM):
		for j in range(0, DDIM):
			#pixels[j][i] = img.getpixel((i, j)) # for some reason correctly rotated
			pixels.set_pixel( j, i, img.getpixel((i, j)) )
	return pixels

def draw_line( frame, sp=(0,0), ep=(0,0), color=(255, 255, 0) ):
	# Bresenham-Line Algorithm
	x1, y1 = sp
	x2, y2 = ep
	dx = x2 - x1
	dy = y2 - y1
	is_steep = abs(dy) > abs(dx) 	# Determine how steep the line is
	if is_steep:					# if line to steep
		x1, y1 = y1, x1
		x2, y2 = y2, x2
	swapped = False					# Swap start and end points if necessary and store swap state
	if x1 > x2:
		x1, x2 = x2, x1
		y1, y2 = y2, y1
		swapped = True
	dx = x2 - x1					# Recalculate differentials
	dy = y2 - y1
	error = int(dx / 2.0)			# Calculate error
	ystep = 1 if y1 < y2 else -1
	y = y1
	points = []						# Iterate over bounding box generating points between start and end
	for x in range(x1, x2 + 1):
		coord = (y, x) if is_steep else (x, y)
		points.append(coord)
		error -= abs(dy)
		if error < 0:
			y += ystep
			error += dx
	if swapped:						# Reverse the list if the coordinates were swapped
		points.reverse()
	for obj in points:
		x, y = obj
		frame.set_pixel(x, y, color)




def main():
	# create a connection to the display with size 8 
	with matrixdisplay.MatrixDispaly(DDIM) as display:
		im = pil.Image.open('img/mario.jpg')
		display.draw_frame(to_pix(im))
		time.sleep(5)

		while True:
			game = gameoflife.GameOfLife(display, (179, 240, 0), 100)
			display.clear_screen()
			game.play()




		fr = frame.Frame(DDIM)
		while True:
			for i in range(0,16):
				draw_line(fr, (i,0), (15-i,15), (250, 0, 10 ))
				draw_line(fr, (0,i), (15,15-i), (0, 0, 255 ))
				display.draw_frame(fr)
				#time.sleep(0.1)
			fr = frame.Frame(DDIM)
			#time.sleep(0.1)


		t = 0.09
		while True:
			display.fill_screen((0, 255, 0))
			time.sleep(t)
			display.fill_screen((0, 255, 255))
			time.sleep(t)
			display.fill_screen((255, 255, 0))
			time.sleep(t)
			display.fill_screen((255, 255, 255))
			time.sleep(t)

	

if __name__ == "__main__": main()