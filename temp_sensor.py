from mlx90614 import MLX90614

class TemperatureSensor:
	def __init__(self, bus):
		self.sensor = MLX90614(bus, address=0x5A)
	
	def body_temperature(self):
		return self.sensor.get_object_1()
