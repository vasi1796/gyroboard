from keras.models import model_from_json  # basic class for specifying and training a neural network
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    'C:/Users/vasy1/Anaconda2/envs/tensorflow/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_gray = gray[int(y + 30):int(y + h / 1.9), x + 25:x + w - 25]
        roi_gray = cv2.resize(roi_gray, (140, 50))
        image = np.asarray(roi_gray)
        image.resize((1, 50, 140, 1))
        image = image.astype(np.float32)
        image /= np.max(image)  # Normalise data to [0, 1] range
        prediction = loaded_model.predict(image, batch_size=32, verbose=0)
        print(np.argmax(prediction))
