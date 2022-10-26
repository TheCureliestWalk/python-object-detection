import cv2
import time
import numpy as np
import imutils

# Create our body classifier
car_classifier = cv2.CascadeClassifier('haarcascade/cars.xml')

# Initiate video capture for video file
cap = cv2.VideoCapture('vid/highway.mp4')


# Loop once video is successfully loaded
while cap.isOpened():
    
    # Read first frame
    ret, frame = cap.read()
    frame = imutils.resize(frame, height=240)
    (h, w) = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   
    # Pass frame to our car classifier
    cars = car_classifier.detectMultiScale(gray, 1.3, 2)
    
    # Extract bounding boxes for any bodies identified
    for (x,y,w,h) in cars:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        cv2.imshow('Cars', frame)

    if cv2.waitKey(1) == ord('q'): 
        break

cap.release()
cv2.destroyAllWindows()