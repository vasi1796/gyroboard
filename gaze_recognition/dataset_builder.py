import gzip
import pickle
from os import listdir
from os.path import isfile, join

import cv2
import numpy as np


def dump_dataset(name, dataset):
    f = gzip.open(name, 'wb')
    pickle.dump(dataset, f, protocol=2)
    f.close()


X_train = []
Y_train = []
X_test = []
Y_test = []
train = 1

folder_left = './left'
folder_right = './right'
folder_center = './center'
only_left_files = [f for f in listdir(folder_left) if isfile(join(folder_left, f))]
only_right_files = [f for f in listdir(folder_right) if isfile(join(folder_right, f))]
only_center_files = [f for f in listdir(folder_center) if isfile(join(folder_center, f))]

for n in range(0, len(only_left_files)):
    mat = cv2.imread(join(folder_left, only_left_files[n]), 0)
    if n == 1200:
        train = 0
    if mat is not None:
        if train:
            X_train.append(mat)
            Y_train.append(0)
        else:
            X_test.append(mat)
            Y_test.append(0)

train = 1
for n in range(0, len(only_right_files)):
    mat = cv2.imread(join(folder_right, only_right_files[n]), 0)
    if n == 1000:
        train = 0
    if mat is not None:
        if train:
            X_train.append(mat)
            Y_train.append(1)
        else:
            X_test.append(mat)
            Y_test.append(1)

train = 1
for n in range(0, len(only_center_files)):
    mat = cv2.imread(join(folder_center, only_center_files[n]), 0)
    if n == 900:
        train = 0
    if mat is not None:
        if train:
            X_train.append(mat)
            Y_train.append(2)
        else:
            X_test.append(mat)
            Y_test.append(2)

X_train = np.asarray(X_train)
Y_train = np.asarray(Y_train)
X_test = np.asarray(X_test)
Y_test = np.asarray(Y_test)
x_train_shape=X_train.shape
x_test_shape=X_test.shape
X_train.resize((x_train_shape[0], x_train_shape[1], x_train_shape[2], 1))
X_test.resize((x_test_shape[0], x_test_shape[1], x_test_shape[2], 1))
Y_train.resize((x_train_shape[0], 1))
Y_test.resize((x_test_shape[0], 1))

dataset = [X_train, Y_train, X_test, Y_test]
dump_dataset('eyes_dataset.pkl.gz', dataset)
print("dataset created")
