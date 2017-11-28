# Basic bitmap renderer for fonts based on the work of tdicola from adafruit
# It only needs to get the string, x, y, and a function to draw pixels
# Thorambar Dae Rusc 2017

import struct

class BitmapFont:

	def __init__(self, width, height, pixel, font_name='font/font5x8.bin'):
		# format:
		# - 1 unsigned byte: font character width in pixels
		# - 1 unsigned byte: font character height in pixels
		# - x bytes: font data, in ASCII order covering all 255 characters.
		# Each character should have a byte for each pixel column of
		# data (i.e. a 5x8 font has 5 bytes per character).
		self._width = width			# Height and width of the drawing area  
		self._height = height
		self._pixel = pixel			# Function to be called to draw, should at least take (x, y Pixels)
		self._font_name = font_name
		self._font = None

	def init(self):
		# Open font file and grab the chars width an height (only up to 8px tall)
		self._font = open(self._font_name, 'rb')
		self._font_width, self._font_height = struct.unpack('BB', self._font.read(2))

	def deinit(self):
		self._font.close

	def __enter__(self):
		self.init()
		return self

	def __exit__(self, exception_type, exception_value, traceback):
		self.deinit()

	def draw_char(self, ch, x, y, *args, **kwargs):
		# Don't draw chars that are not on screen
		if( x < -self._font_width or x >= self._width or y < -self._font_height or y >= self._height ):
			return
		# Go through the columns of chars
		for char_x in range(self._font_width):
			self._font.seek(2 + (ord(ch) * self._font_width) + char_x)
			line = struct.unpack('B', self._font.read(1))[0]
			# Go through each row in the column byte
			for char_y in range(self._font_height):
				# Draw a pixel for each pixel that is set
				if(  (line >> char_y) & 0x1 ):
					self._pixel(x + char_x, y + char_y, *args, **kwargs)

	def text(self, text, x, y, *args, **kwargs):
	# Draw text at location with the char function
		for i in range(len(text)):
			self.draw_char(text[i], x + (i * (self._font_width + 1)), y, *args, **kwargs) 

	def width(self, text):
		# Return needed with for text 
		return len(text) * (self._font_width + 1)
