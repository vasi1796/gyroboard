import cv2
import numpy as np

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    'C:/Users/vasy1/Anaconda2/envs/tensorflow/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(
    'C:/Users/vasy1/Anaconda2/envs/tensorflow/Lib/site-packages/cv2/data/haarcascade_eye.xml')
index ="1"
if __name__ == "__main__":
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            roi_gray = gray[int(y + 20):int(y + h / 1.9), x:x + w]
            roi_color = img[int(y + 20):y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 2, 3)
            # cv2.imshow("roi_eyes",roi_gray)
            for (ex, ey, ew, eh) in eyes:
                found_eye = roi_gray[ey:ey + eh, ex:ex + ew]
                cv2.equalizeHist(found_eye, found_eye)
                # cv2.imshow("normalized eye",found_eye)
                #cv2.imwrite("left/img" + index + ".jpg", found_eye)
                #cv2.imwrite("right/img" + index + ".jpg", found_eye)
                cv2.imwrite("center/img" + index + ".jpg", found_eye)
                no=int(index)+1
                index=str(no)
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        cv2.imshow("face", img)
        cv2.waitKey(1)

cap.release()
