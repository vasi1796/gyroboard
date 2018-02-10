import cv2

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    'C:/Users/vasy1/Anaconda2/envs/tensorflow/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(
    'C:/Users/vasy1/Anaconda2/envs/tensorflow/Lib/site-packages/cv2/data/haarcascade_eye.xml')
index = "748"

if __name__ == "__main__":
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi_gray = gray[int(y + 30):int(y + h / 1.9), x + 25:x + w - 25]
            roi_gray = cv2.resize(roi_gray, (140, 50))
            no = int(index) + 1
            index = str(no)
            cv2.imshow("roi_eyes", roi_gray)
            if img is not None:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(5, 5))
                cl1 = clahe.apply(roi_gray)
                cv2.imshow("cl", cl1)
                cv2.imwrite("center/img" + index + ".jpg", cl1)

            """
            roi_color = img[int(y + 20):y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 2, 3)
            for (ex, ey, ew, eh) in eyes:
                found_eye = roi_gray[ey:ey + eh, ex:ex + ew]
                cv2.equalizeHist(found_eye, found_eye)
                cv2.imshow("normalized eye",found_eye)
                #cv2.imwrite("left/img" + index + ".jpg", found_eye)
                #cv2.imwrite("right/img" + index + ".jpg", found_eye)
                #cv2.imwrite("center/img" + index + ".jpg", found_eye)
                no=int(index)+1
                index=str(no)
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)"""
        cv2.imshow("face", img)
        cv2.waitKey(1)

cap.release()
