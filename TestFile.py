import cv2
import numpy as np

cap = cv2.VideoCapture(0)


def findFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/Images/haarcascades/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)
    myFaceList = []
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        print(cx)
        print(cy)
        area = w * h
        cv2.circle(img, (int(cx), int(cy)), 5, (0, 255, 0), cv2.FILLED)
        myFaceList.append([cx, cy])
        myFaceListArea.append(area)
        if len(myFaceListArea) != 0:
            i = myFaceListArea.index(max(myFaceListArea))
            return img, [myFaceList[i]], myFaceListArea[i]
        else:
            return img, [[0, 0], 0]




while True:
    _, img = cap.read()
    findFace(img)
    cv2.imshow("Output", img)
    cv2.waitKey(1)