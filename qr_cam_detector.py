class QRCamDetector:
	def __init__(self, cam, detector):
		self.cam = cam
		self.detector = detector
	
	# QR Detection
	def get_data(self):
		# Get image
		_, img = self.cam.read()
		# Get bounding box and data
		data, _, _ = self.detector.detectAndDecode(img)
		return data
