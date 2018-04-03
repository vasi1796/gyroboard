import numpy as np
from keras.models import model_from_json


class WordNN:
    def __init__(self, json_model_file, h5_model_file):
        json_file = open(json_model_file, 'r')
        self.loaded_model_json = json_file.read()
        json_file.close()
        self.loaded_model = model_from_json(self.loaded_model_json)
        self.loaded_model.load_weights(h5_model_file)
        # self.loaded_model.predict(np.zeros((1, 50, 140, 1)))

    def process_chars(self):
        pass
