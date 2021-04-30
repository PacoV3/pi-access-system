print("[INFO] Cargando paquetes...")
from temp_sensor import TemperatureSensor
# from qr_cam_detector import QRCamDetector
from qr_fast_cam_detector import QRFastCamDetector
from mask_recon import MaskRecon
from datetime import datetime
from time import time, sleep
from smbus2 import SMBus
import RPi.GPIO as gpio
from os import system
import requests
import cv2


def activate_actuator():
    gpio.setmode(gpio.BOARD)
    gpio.setup(12, gpio.OUT)

    gpio.output(12, True)
    print("On")
    sleep(10)

    gpio.output(12, False)
    print("Off")
    sleep(10)
    print("Disponible nuevamente")


def main():
    # Declarations
    bus = SMBus(1) # Bus object
    temp_sensor = TemperatureSensor(bus) # Temp sensor object
    cam = cv2.VideoCapture(0) # Set camera object
    qr = QRFastCamDetector(cam) # QRFastCamDetector object
    # detector = cv2.QRCodeDetector() # QR detector
    # qr = QRCamDetector(cam, detector) # QRCamDetector object
    mask_recon = MaskRecon(cam=cam, coords=(100, 30, 300, 270), model_location="mask_detector.model") # MaskRecon object

    # As soon as the program starts search for mask after the correct body temp
    search_for_mask = True
    temp_change = True
    body_temp = 0
    interval_time = 40 # seconds
    change_time = time()
    print("[INFO] Sistema listo!")
    while True:
        try:
            time_now = time()
            temp_sensor_val = temp_sensor.body_temperature()
            body_temp = temp_sensor_val if body_temp < temp_sensor_val else body_temp
            if 33 < body_temp < 37.5:
                if temp_change:
                    print(f"Temperatura: {body_temp:.2f}")
                    change_time = time()
                    temp_change = False
                if search_for_mask:
                    mask_probability = mask_recon.get_mask_p(wait_time=0.5)
                    if mask_probability > 0.9:
                        change_time = time()
                        print('Mascarilla encontrada')
                        search_for_mask = False
                else:
                    data = qr.get_data()
                    if data:
                        qr_type, user_id = data
                        if qr_type == 'Entry':
                            # url = 'https://controlacces.herokuapp.com/registro_entradas'
                            now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                            request = {'id_user': user_id, 'time_in': now}
                            print(f"Request: {request}")
                            # x = requests.post(url, json = myobj)
                            # TEXT SPEACH
                            # system(f"espeak -ves+f8-k5-s150 'todo correcto'")
                            activate_actuator()
                            change_time = time()
                            body_temp = 0
                            search_for_mask = True
                            temp_change = True
            if time_now - change_time > interval_time:
                change_time = time()
                body_temp = 0
                search_for_mask = True
                temp_change = True
                print(f"{interval_time} seconds")
        except KeyboardInterrupt:
            print("End of app")
            bus.close() # Free the bus object
            cam.release() # Free the camera object and exit
            gpio.cleanup()
            break

if __name__ == '__main__':
    main()
