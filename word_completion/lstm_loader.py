from __future__ import print_function
from keras.utils.data_utils import get_file
import io
import numpy as np
from keras.models import load_model
import pickle
import heapq
import cv2
from threading import Thread

letter_list = ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e',
               'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e']
letter_string = ""
predictions = []


def sample(preds, top_n=3):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds)
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)

    return heapq.nlargest(top_n, range(len(preds)), preds.take)


def prepare_input(text):
    x = np.zeros((1, len(text), len(chars)))

    for t, char in enumerate(text):
        x[0, t, char_indices[char]] = 1.

    return x


def predict_completion(text):
    original_text = text
    completion = ''
    while True:
        x = prepare_input(text)
        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds, top_n=1)[0]
        next_char = indices_char[next_index]

        text = text[1:] + next_char
        completion += next_char

        if len(original_text + completion) + 2 > len(original_text) and next_char == ' ':
            return completion


def thread_pred():
    while True:
        if len(letter_string) is 40:
            predict_completions(letter_string, 3)
            print()


def predict_completions(text, n=3):
    if len(text) is 40:
        x = prepare_input(text)
        preds = model.predict(x, verbose=0)[0]
        next_indices = sample(preds, n)
        print([indices_char[idx] + predict_completion(text[1:] + indices_char[idx]) for idx in next_indices])


path = get_file('nietzsche.txt', origin='https://s3.amazonaws.com/text-datasets/nietzsche.txt')
with io.open(path, encoding='utf-8') as f:
    text = f.read().lower()
print('corpus length:', len(text))

chars = sorted(list(set(text)))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

print('unique chars: ', len(chars))

SEQUENCE_LENGTH = 40
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - SEQUENCE_LENGTH, step):
    sentences.append(text[i: i + SEQUENCE_LENGTH])
    next_chars.append(text[i + SEQUENCE_LENGTH])
print('num training examples: ', len(sentences))

X = np.zeros((len(sentences), SEQUENCE_LENGTH, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

model = load_model('keras_model.h5')
#history = pickle.load(open("history.p", "rb"))

prepare_input("This is an example of input for our LSTM".lower())

quotes = [
    "It is not a lack of love, but a lack of friendship that makes unhappy marriages.",
    "It is not a lack of love, but a lack of friendship that makes unhappy marriages.",
    "I'm not upset that you lied to me, I'm upset that from now on I can't believe you.",
    "And those who were seen dancing were thought to be insane by those who could not hear the music.",
    "It is hard enough to remember my opinions, without also remembering my reasons for them!"
]
for q in quotes:
    seq = q[:40].lower()
    print(seq)
    predict_completions(seq, 5)
    print()

# let = ''.join(letter_list)
# test=let.lower()
# print(let.lower())
# print(len(let))
# predict_completions(test,3)
# print()
words_thread = Thread(target=thread_pred, args=())
words_thread.start()
cap = cv2.VideoCapture(0)
while True:
    ret, img = cap.read()
    cv2.imshow("fr", img)
    key = cv2.waitKey(1)
    if key != -1:
        letter_list.pop(0)
        letter_list.append(chr(key))
        letter_string = ''.join(letter_list)
        letter_string = letter_string.lower()
