from temp_sensor import TemperatureSensor
from qr_cam_detector import QRCamDetector
from smbus2 import SMBus
from os import system
import cv2 as cv

# Declaration of variables
cam = cv.VideoCapture(0) # Set camera object
detector = cv.QRCodeDetector() # QR detector
qr = QRCamDetector(cam,detector) # QRCamDetector object
bus = SMBus(1) # Bus object
temp_sensor = TemperatureSensor(bus) # Temp sensor object

try:
    while True:
        data, bbox = qr.qr_data_box()
        if data and bbox is not None:
            print("data is =", data)
            # system(f"espeak -ves+f8-k5-s150 '{data}'")
            body_temp = temp_sensor.body_temperature()
            print("Body Temperature :", body_temp)
except KeyboardInterrupt:
    print("End of use")
    pass

# Free the bus object
bus.close() 
# Free the camera object and exit
cam.release()
