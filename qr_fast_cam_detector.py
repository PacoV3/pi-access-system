import numpy as np
import pyzbar.pyzbar as pyzbar

class QRFastCamDetector:
	def __init__(self, cam):
		self.cam = cam
	
	# QR Detection
	def get_data(self):
		txt = None
		_, img = self.cam.read()
		decoded_objects = pyzbar.decode(img)
		if len(decoded_objects) >= 1:
			txt = tuple(decoded_objects[0].data.decode('UTF-8').split(','))
		return txt
