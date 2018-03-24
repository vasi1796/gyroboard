from keras.models import model_from_json
import cv2
import numpy as np


class GazeNN(object):
    def __init__(self, json_model_file, h5_model_file):
        self.frame = None
        json_file = open(json_model_file, 'r')
        self.loaded_model_json = json_file.read()
        json_file.close()
        self.loaded_model = model_from_json(self.loaded_model_json)
        self.loaded_model.load_weights(h5_model_file)
