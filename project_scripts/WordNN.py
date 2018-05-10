from __future__ import print_function
from keras.utils.data_utils import get_file
import io
import numpy as np
from keras.models import load_model
import heapq
letter_list = ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e',
               'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e']
letter_string = ""
predictions = []


class WordNN:
    def __init__(self, h5_model_file):
        path = get_file('nietzsche.txt', origin='https://s3.amazonaws.com/text-datasets/nietzsche.txt')
        with io.open(path, encoding='utf-8') as f:
            self.text = f.read().lower()

        self.chars = sorted(list(set(self.text)))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))

        self.model = load_model(h5_model_file)

        init_quote = "It is not a lack of love, but a lack of friendship that makes unhappy marriages."
        seq = init_quote[:40].lower()
        self.predict_completions(seq, 5)

    def sample(self, preds, top_n=3):
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds)
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)

        return heapq.nlargest(top_n, range(len(preds)), preds.take)

    def prepare_input(self, text):
        x = np.zeros((1, len(text), len(self.chars)))

        for t, char in enumerate(text):
            x[0, t, self.char_indices[char]] = 1.

        return x

    def predict_completion(self, text):
        original_text = text
        completion = ''
        while True:
            x = self.prepare_input(text)
            preds = self.model.predict(x, verbose=0)[0]
            next_index = self.sample(preds, top_n=1)[0]
            next_char = self.indices_char[next_index]

            text = text[1:] + next_char
            completion += next_char

            if len(original_text + completion) + 2 > len(original_text) and next_char == ' ':
                return completion

    def predict_completions(self, text, n=3):
        if len(text) is 40:
            x = self.prepare_input(text)
            preds = self.model.predict(x, verbose=0)[0]
            next_indices = self.sample(preds, n)
            return [self.indices_char[idx] + self.predict_completion(text[1:] + self.indices_char[idx]) for idx in next_indices]

