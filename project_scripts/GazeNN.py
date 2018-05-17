from keras.models import model_from_json
import cv2
import numpy as np


class GazeNN(object):
    def __init__(self, json_model_file, h5_model_file):
        json_file = open(json_model_file, 'r')
        self.loaded_model_json = json_file.read()
        json_file.close()
        self.loaded_model = model_from_json(self.loaded_model_json)
        self.loaded_model.load_weights(h5_model_file)
        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(
            'C:/Users/vasy1/AppData/Local/Continuum/anaconda3/pkgs/opencv-3.3.1-py36h20b85fd_1/Library/etc/haarcascades/haarcascade_frontalface_default.xml')
        self.loaded_model.predict(np.zeros((1, 50, 140, 1)))

    def process_image(self):
        ret, img = self.cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            # preprocess image
            roi_gray = gray[int(y + 30):int(y + h / 1.9), x + 25:x + w - 25]
            roi_gray = cv2.resize(roi_gray, (140, 50))
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(5, 5))
            cl1 = clahe.apply(roi_gray)
            cv2.imshow('face', cl1)
            key_press=cv2.waitKey(1)
            # prepare input for model
            image = np.asarray(roi_gray)
            image.resize((1, 50, 140, 1))
            image = image.astype(np.float32)
            image /= np.max(image)  # Normalise data to [0, 1] range
            prediction = self.loaded_model.predict(image, batch_size=32, verbose=0)
            return np.argmax(prediction), key_press
        return -1,-1
