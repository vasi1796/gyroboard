from keras.models import Sequential  # basic class for specifying and training a neural network
from keras.layers import Convolution2D, MaxPooling2D, Dense, Dropout, Flatten, Activation, BatchNormalization
from keras.utils import np_utils  # utilities for one-hot encoding of ground truth values
from keras.callbacks import TensorBoard, EarlyStopping
from keras.regularizers import l2  # L2-regularisation
import time

import numpy as np
import gzip
import pickle


def load_data(dataset):
    with gzip.open(dataset, 'rb') as f:
        try:
            X_train, y_train, X_test, y_test = pickle.load(f, encoding='latin1')
        except:
            X_train, y_train, X_test, y_test = pickle.load(f)
        return X_train, y_train, X_test, y_test


timestr = time.strftime("%Y%m%d_%H%M")
batch_size = 32  # in each iteration, we consider 32 training examples at once
num_epochs = 50  # we iterate 200 times over the entire training set
kernel_size = 3  # we will use 3x3 kernels throughout
pool_size = 2  # we will use 2x2 pooling throughout
conv_depth_1 = 32  # we will initially have 32 kernels per conv. layer...
conv_depth_2 = 64  # ...switching to 64 after the first pooling layer
drop_prob_1 = 0.25
drop_prob_2 = 0.5  # dropout in the FC layer with probability 0.5
hidden_size = 512  # the FC layer will have 512 neurons
l2_lambda = 0.0001

X_train, y_train, X_test, y_test = load_data('./data/eyes_dataset.pkl.gz')

num_train, height, width, depth = X_train.shape  # there are 50000 training examples in CIFAR-10
num_test = X_test.shape[0]  # there are 10000 test examples in CIFAR-10
num_classes = np.unique(y_train).shape[0]  # there are 10 image classes

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= np.max(X_train)  # Normalise data to [0, 1] range
X_test /= np.max(X_test)  # Normalise data to [0, 1] range

Y_train = np_utils.to_categorical(y_train, num_classes)  # One-hot encode the labels
Y_test = np_utils.to_categorical(y_test, num_classes)  # One-hot encode the labels

model = Sequential()
model.add(Convolution2D(conv_depth_1, (kernel_size, kernel_size), padding='same',input_shape=(height, width, depth),
                        kernel_initializer='he_uniform', kernel_regularizer=l2(l2_lambda)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(pool_size, pool_size)))
model.add(Convolution2D(conv_depth_1, (kernel_size, kernel_size)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(pool_size, pool_size)))
model.add(Dropout(drop_prob_1))
model.add(Convolution2D(conv_depth_2, (kernel_size, kernel_size)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(pool_size, pool_size)))
model.add(Flatten())
model.add(Dense(hidden_size))
model.add(Activation('relu'))
model.add(Dropout(drop_prob_2))
model.add(Dense(num_classes, kernel_initializer='glorot_uniform',
                kernel_regularizer=l2(l2_lambda)))
model.add(Activation('softmax'))

tbCallback = TensorBoard(log_dir='./Graph', histogram_freq=10, write_graph=True, write_images=True)

model.compile(loss='categorical_crossentropy',  # using the cross-entropy loss function
              optimizer='adam',  # using the Adam optimiser
              metrics=['accuracy'])  # reporting the accuracy

model.fit(X_train, Y_train,  # Train the model using the training set...
          batch_size=batch_size, epochs=num_epochs,
          verbose=1, validation_split=0.2, callbacks=[tbCallback, EarlyStopping(monitor='val_loss',
                                                                                patience=5)])  # ...holding out 10% of the data for validation
score = model.evaluate(X_test, Y_test, verbose=1)  # Evaluate the trained model on the test set!

print('Test score is: ', score[0])
print('Accuracy is: ', score[1])

model_json = model.to_json()
with open("./models/model_" + timestr + ".json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("./models/model_" + timestr + ".h5")
print("Saved model to disk")
