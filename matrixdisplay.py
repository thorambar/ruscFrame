# A driver that makes it easy to use WS2812 LEDs as an display (only for square displays).
# The LEDs have to be wired in serial, so that like a strip.
# Based on the neoPixel library from Adafruit
# Thorambar Dae Rusc 2017

from neopixel import *

class MatrixDispaly:

	def __init__(self, dim, ledpin=18, ledfreq=800000, leddma=5, ledbrightness=5, invert=False, ledchannel=0, ledstriptype=ws.WS2811_STRIP_GRB):
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
		self._led_strip = Adafruit_NeoPixel(_led_count, _led_pin, _led_freq_hz, _led_dma, _led_brightness, _led_invert, _led_channel, _led_strip_type)

	
	def deinit(self):
		clear_screen()

	
	def __enter__(self):
		self.init()
		return self

	
	def __exit__(self, exception_type, exception_value, traceback):
		self.deinit()

	
	def draw_frame(self, matrix):
		# Will only need a matrix of RGB values and draws it
		for i in range(0, dim):
			for j in range(0, dim):
				r, g, b = matrix[i][j]
				strip.setPixelColor(cords_to_pixnum(i, j, res), Color(r, g, b))
		strip.show()

	
	def set_brigtnes(self, brightness):
		self._led_brightness = brightness
		self._led_strip.setBrightness(_led_brightness)

	
	def get_brightnes(self):
		return self._led_brightness

	
	def get_dim(self):
		return self._led_dim

	
	def get_led:count(self):
		return self._led_count

	
	def clear_screen():
		# Clear screen 
		for i in range(self._led_strip.numPixels()):
			strip.setPixelColor(i, Color(0, 0, 0))
			strip.show()