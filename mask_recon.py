from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import imutils
import time
import cv2

class MaskRecon:
    def __init__(self, cam, coords, model_location):
        print("[INFO] Loading face mask detector model...")
        self.mask_net = load_model(model_location)
        self.coords = coords
        self.cam = cam
        time.sleep(1)

    def detect_and_predict_mask(self, frame):
        faces = []
        preds = []
        startX, startY, endX, endY = self.coords
        # ordering, resize it to 224x224, and preprocess it
        face_box = frame[startY:endY, startX:endX]
        face_box = cv2.cvtColor(face_box, cv2.COLOR_BGR2RGB)
        face_box = cv2.resize(face_box, (224, 224))
        face_box = img_to_array(face_box)
        face_box = preprocess_input(face_box)
        faces.append(face_box)

        faces = np.array(faces, dtype="float32")
        preds = self.mask_net.predict(faces, batch_size=1)
        #             Mask       No mask
        # preds = [[0.00580262 0.99419737]]
        return preds

    def get_mask_p(self, wait_time):
        time.sleep(wait_time)
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        _, frame = self.cam.read()
        frame = imutils.resize(frame, width=400)
        #             Mask       No mask
        # preds = [[0.00580262 0.99419737]]
        preds = self.detect_and_predict_mask(frame)
        if preds.any():
            mask, withoutMask = preds[0]
            return mask
        return -1

def main():
    cam = cv2.VideoCapture(0)
    mask_recon = MaskRecon(cam, coords=(100, 30, 300, 270), model_location="mask_detector.model")
    while True:
        preds = mask_recon.get_mask_p(wait_time=0.5)
        print(preds)


if __name__ == "__main__":
    main()
    cam.release()
