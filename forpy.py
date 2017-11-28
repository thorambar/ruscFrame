# My own little wrapper class for for the WS2812(b) aka NeoPixel LEDs in a nxm 
# matrix configuration. Everything should return A nxmx(rgb) matrix to be drawn.
# Thorambar dae Rusc 2017

import numpy as np
import sys
import PIL as pil
from PIL import ImageFont, ImageDraw
import bitmapfont



import time

from neopixel import *

import argparse
import signal
import sys

def signal_handler(signal, frame):
        colorWipe(strip, Color(0,0,0))
        sys.exit(0)

def opt_parse():
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', action='store_true', help='clear the display on exit')
        args = parser.parse_args()
        if args.c:
                signal.signal(signal.SIGINT, signal_handler)

# LED strip configuration:
LED_COUNT      = 64      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 40     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour order


# ==== Image to pixel conversion ==========================================
def to_pix(image, res):
	img = image.resize((res, res)).convert('RGB') # AA maybe bad
	pixels = np.zeros( (res,res,3), dtype=np.uint8 ) # 8 bit for 0-255 values of RGB
	for i in range(0, res):
		for j in range(0, res):
			pixels[j][i] = img.getpixel((i, j)) # for some reason correctly rotated
	return pixels

# ==== Draw methods for different shapes ==================================
def new_canvas( res ):
	return np.zeros( (res,res,3), dtype=np.uint8 )

def draw_line( image, sp=(0,0), ep=(0,0), color=(255, 255, 255) ):
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
		image[obj[0]][obj[1]] = color
	return image

def draw_circle( image, cp=(0, 0), radius=0, color=(255, 255, 255) ):
	# Bresenham-Circle ALgorithm 
	x0, y0 = cp
	f = 1 - radius
	ddf_x = 1
	ddf_y = -2 * radius
	x = 0
	y = radius
	image[x0][y0 + radius] = color
	image[x0][y0 - radius] = color
	image[x0 + radius][y0] = color
	image[x0 - radius][y0] = color
	
	while( x < y ):
		if( f >= 0 ):
			y -= 1
			ddf_y += 2
			f += ddf_y
		x += 1
		ddf_x += 2
		f += ddf_x
		image[x0 + x][y0 + y] = color
		image[x0 - x][y0 + y] = color
		image[x0 + x][y0 - y] = color
		image[x0 - x][y0 - y] = color
		image[x0 + y][y0 + x] = color
		image[x0 - y][y0 + x] = color
		image[x0 + y][y0 - x] = color
		image[x0 - y][y0 - x] = color

	return image

def draw_text(image, str):
	font = ImageFont.load_default()
	img = pil.Image.new('RGB', (16, 16))
	img = ImageDraw.Draw(img)
	img.text((10, 10), str, font=font)
	return toPix(img, resolutuion)

def cords_to_pixnum(x, y, res):
	return x + y * res

def pix_to_cords(num, res):
	return ( (num % res), floor(num / res) )

def draw_in_Matrix( x, y, matrix, color=(255, 0, 0) ):
	matrix[y][x] = color
	return matrix


	
# ++++ Debug stuff and test display +++++++++++++++++++++++++++++++++++++++




def matrix_to_strip(matrix, strip, res):
	for i in range(0, res):
		for j in range(0, res):
			color = matrix[i][j]
			a, b, c = color
			strip.setPixelColor(cords_to_pixnum(i, j, res), Color(a, b, c))
	strip.show()



# ==== Main code ==========================================================
resolutuion = 8

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# Intialize the library (must be called once before other functions).
strip.begin()



im = pil.Image.open('img/mario.jpg')
nim = to_pix(im, resolutuion)
matrix_to_strip(nim, strip, resolutuion)
#displayImage(nim)


#matrix = new_canvas(resolutuion)
#with bitmapfont.BitmapFont(resolutuion, resolutuion, draw_in_Matrix) as bf:
	#bf.text('hallo Welt', 2, 0, matrix, (94, 94, 2))






#drawLine(matrix, (8,8), (8, 13), (255, 50, 87) )
#drawCircle(matrix, (8,8), 6, (32, 64, 128))
#display_image(matrix)



# =============
exit(0)