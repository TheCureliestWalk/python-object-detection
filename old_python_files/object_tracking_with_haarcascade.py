# Project
# 1. Not using any trained model, only use for detecting moving object with some big [width and height]
# 2. Save data including speed estimation, picture, cars id, timestamp
# 3. Save these data to database (influxdb, postgresql)
# optional.
# - Using Flask to display these data for easily understanding.


import numpy as np
import imutils
import cv2
import os
cap = cv2.VideoCapture("img/motorbike_th.webp")
car_haarcascade = cv2.CascadeClassifier('haarcascade/haarcascade_car.xml')
motorcycle_haarcasacde = cv2.CascadeClassifier('haarcascade/two_wheeler.xml')

while True:
    ret, frame = cap.read()
    frame = imutils.resize(frame, height=240)
    h, w, _ = frame.shape
    # print(h,w,_)
    # roi = frame[320:1200, 100:1200] # frame[height, width]
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cars = motorcycle_haarcasacde.detectMultiScale(gray, 1.4, 1)
    i = 0
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        i = i + 1
        print("Car Detected: ", cars)
        
    cv2.imshow('Cars', frame)
            
    key = cv2.waitKey(30)
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()