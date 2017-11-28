# A driver that makes it easy to use WS2812 LEDs as an display (only for square displays).
# The LEDs have to be wired in serial, so that like a strip.
# Based on the neoPixel library from Adafruit
# Thorambar Dae Rusc 2017

from neopixel import *

class MatrixDispaly:

	def __init__(self, dim, ledpin=18, ledfreq=800000, leddma=5, ledbrightness=5, invert=False, ledchannel=0, ledstrip=ws.WS2811_STRIP_GRB):
		# LED strip configuration:
		self._led_count = dim * dim
		self._led_pin = ledpin
		self._led_freq_hz = ledfreq
		self._led_dma = leddma
		self._led_brightness = ledbrightness
		self._led_invert = inverted
		self._led_channel = ledchannel
		self._led_strip = ledstrip


	def init(self):
		# TODO has to open connection to the string

	def deinit(self):
		# TODO has to close the connection to the strip 

	def __enter__(self):
		self.init()
		return self

	def __exit__(self, exception_type, exception_value, traceback):
		self.deinit()

	def draw_frame(self, matrix):
		# TODO will only need a matrix of RGB values, thand draws it

	def set_brigtnes(self, brightnes):
		# TODO

	def get_brightnes(self):
		# TODO

