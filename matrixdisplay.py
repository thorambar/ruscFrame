# A driver that makes it easy to use WS2812 LEDs as an display (only for square displays).
# The LEDs have to be wired in serial, so that like a strip.
# Based on the neoPixel library from Adafruit
# Thorambar Dae Rusc 2017

from neopixel import *
import frame

import argparse
import signal
import sys


class MatrixDispaly:

	def __init__(self, dim, ledpin=18, ledfreq=800000, leddma=5, ledbrightness=1, inverted=False, ledchannel=0, ledstriptype=ws.WS2811_STRIP_GRB):
		# LED strip configuration:
		self._led_dim = dim
		self._led_count = dim * dim
		self._led_pin = ledpin
		self._led_freq_hz = ledfreq
		self._led_dma = leddma
		self._led_brightness = ledbrightness
		self._led_invert = inverted
		self._led_channel = ledchannel
		self._led_strip_type = ledstriptype
		self._led_strip = None

	def init(self):
		self._led_strip = Adafruit_NeoPixel(self._led_count, self._led_pin, self._led_freq_hz, self._led_dma, \
			self._led_invert, self._led_brightness, self._led_channel, self._led_strip_type)
		self._led_strip.begin()


	def deinit(self):
		self.clear_screen

	def __enter__(self):
		self.init()
		return self

	def __exit__(self, exception_type, exception_value, traceback):
		self.deinit()

	def draw_frame(self, frame):
		#print id(self)
		# Will only need a frame of RGB values and draws it
		for i in range(0, self._led_dim):
			for j in range(0, self._led_dim):
				r, g, b = frame.get_pixel(i, j)
				self._led_strip.setPixelColor( self.cords_to_pixnum(i, j, self._led_dim), Color(r, g, b) )
		self._led_strip.show()	

	def set_brigtnes(self, brightness):
		self._led_brightness = brightness
		self._led_strip.setBrightness(_led_brightness)

	def get_brightnes(self):
		return self._led_brightness

	def get_dim(self):
		return self._led_dim

	def get_ledcount(self):
		return self._led_count

	def clear_screen(self):
		# Clear screen 
		for i in range(self._led_strip.numPixels()):
			self._led_strip.setPixelColor(i, Color(0, 0, 0))
		self._led_strip.show()

	def fill_screen(self, color):
		# Clear screen 
		r, g, b = color
		c = Color(r, g, b)
		for i in range(self._led_strip.numPixels()):
			self._led_strip.setPixelColor(i, c)
		self._led_strip.show()

	def cords_to_pixnum(self, x, y, res):
		return x + y * res