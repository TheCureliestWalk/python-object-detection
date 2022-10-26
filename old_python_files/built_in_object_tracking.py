# Project
# 1. Not using any trained model, only use for detecting moving object with some big [width and height]
# 2. Save data including speed estimation, picture, cars id, timestamp
# 3. Save these data to database (influxdb, postgresql)
# optional.
# - Using Flask to display these data for easily understanding.


import numpy as np
import imutils
import cv2

#cap = cv2.VideoCapture("vid/211212_02_Jakarta_4k_018.mp4")
cap = cv2.VideoCapture("rtsp://iho:1q2w3e4r%40iho@10.88.240.172/axis-media/media.amp?videocodec=h264&resolution=640x480")

od = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50)

while True:
    ret, frame = cap.read()
    #frame = imutils.resize(frame, height=720) # video size is fixed by rtsp
    h, w, _ = frame.shape
    #print(h,w,_)
    roi = frame[320:1200, 100:1200] # frame[height, width]
    
    mask = od.apply(roi)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    for ct in contours:
        area = cv2.contourArea(ct)

        if area > 100:
            #cv2.drawContours(roi, [ct], -1, (0, 255,0), 2)
            x, y, w, h = cv2.boundingRect(ct)
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Region of Interest", roi)
    
    
    key = cv2.waitKey(30)
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()