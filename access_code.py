print("[INFO] loading packages...")
from temp_sensor import TemperatureSensor
from qr_cam_detector import QRCamDetector
from mask_recon import MaskRecon
from smbus2 import SMBus
from os import system
import cv2

# Declarations
bus = SMBus(1) # Bus object
temp_sensor = TemperatureSensor(bus) # Temp sensor object
cam = cv2.VideoCapture(0) # Set camera object
detector = cv2.QRCodeDetector() # QR detector
qr = QRCamDetector(cam, detector) # QRCamDetector object
mask_recon = MaskRecon(cam=cam, coords=(100, 30, 300, 270), model_location="mask_detector.model") # MaskRecon object

# As soon as the program starts search for mask after the correct body temp
search_for_mask = True
temp_change = True
while True:
    try:
        # time_now = time()
        temp_sensor_val = temp_sensor.body_temperature()
        body_temp = temp_sensor_val if body_temp < temp_sensor_val else body_temp
        if 30 < body_temp < 37.5:
            # if temp_change:
                # time_for_change = time()
                # temp_change = False
            if search_for_mask:
                mask_probability = mask_recon.get_mask_p(wait_time=0.5)
                if mask_probability > 0.8:
                    search_for_mask = False
            else:
                data = qr.qr_data_box()
                if data:
                    print("data is =", data)
                    # TEXT SPEACH
                    system(f"espeak -ves+f8-k5-s150 'todo correcto'")
                    # Restart all variables
                    body_temp = 0
                    search_for_mask = True
                    temp_change = True
        # if time_now - time_for_change > 10000:
            # reset_variables()
    except KeyboardInterrupt:
        print("End of app")
        bus.close() # Free the bus object
        cam.release() # Free the camera object and exit
        break
