from math import sqrt, pow
import torch
import numpy as np
import cv2
import os
import time
from PIL import ImageGrab
import pandas as pd
from data import tracker
# Init tracker objects
tracker = tracker.EuclideanDistTracker()
model = torch.hub.load('ultralytics/yolov5', 'custom', path='data/last.pt', force_reload=True)
force_reload=True).eval()
model.conf = 0.5  # NMS confidence threshold
model.iou = 0.5  # NMS IoU threshold
model.agnostic = False  # NMS class-agnostic
model.multi_label = False  # NMS multiple labels per box
# (optional list) filter by class, i.e. = [0, 15, 16] for COCO persons, cats and dogs
model.classes = None
model.max_det = 1000  # maximum number of detections per image
model.amp = False  # Automatic Mixed Precision (AMP) inference

cap = cv2.VideoCapture("rtsp://iho:1q2w3e4r%40iho@10.88.240.172/axis-media/media.amp?videocodec=h264&resolution=640x480")
# Variables
COLOR_RED = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (255, 0, 0)
COLOR_YELLOW = (0, 255, 255)
line_pos = [(56, 298), (583, 600)]
x_shape = 640 # width of source
y_shape = 480 # height of source
ct = 0 #counter
# processing time
startTime = 0
endTime = 1
lastDistance = 0
def findCenterPoint(x1, y1, x2, y2): # return distance in meters
    center_x, center_y = int((x1 + x2) / 2), int((y1 + y2) / 2)
    return center_x, center_y

def calcEuclidean(center_x, center_y):
    output = sqrt(abs(pow(center_x, 2) + pow(center_y, 2)))
    return output
def findCurrentDistance(x1, y1, x2, y2):
    center_x, center_y = findCenterPoint(x1, y1, x2, y2)
    currentDistance = calcEuclidean(center_x, center_y)
    return currentDistance#  *0.0002645833 pixels to meters
while True:
    ct += 1
    rect = cap.grab()
    if ct % 5 == 0:
        ret, frame = cap.read()
        source_fps = cap.get(cv2.CAP_PROP_FPS)
        frame = [frame]
        result = model(frame)
        render_frame = np.squeeze(result.render())
        # detection box
        labels, cord = result.xyxyn[0][:, -1], result.xyxyn[0][:, :-1]
        boxes = []  # Empty list for each box
        n = len(labels) # print labels -> 4. car // 15. motorcycle
        for i in range(n):
            startTime = time.perf_counter  # timer in seconds
            row = cord[i]
            if row[4] >= 0.5: #Confidence level
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                center_x, center_y = findCenterPoint(x1, y1, x2, y2)
                cv2.circle(render_frame, (center_x, center_y), 5, COLOR_GREEN, -1)
                # Put all coordinates into boxes variable
                boxes.append([x1, y1, x2, y2]) # current box
                boxes_tracker = tracker.update(boxes) # automatic print to console output
                old_boxes = boxes.copy() # last box
                for box_tracker in boxes_tracker:
                    x1, y1, x2, y2, id = box_tracker # get coordinates each car
                    cv2.putText(render_frame, "id: " + str(id), (x1, y2 + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_YELLOW, 1, cv2.LINE_AA)
                    distance = findCurrentDistance(x1, y1, x2, y2) # in meters
                    #diffTime = round(endTime - startTime, 3)  # in seconds
                    #fps = 1/diffTime
                    fps = source_fps # ref from infertence time about 250 ms
                    speed = ((distance - lastDistance)/fps)*3.6 # *3.6 for m to km/h
                    endTime = time.time()
                    cv2.putText(
                        render_frame,
                        "speed: " + str(speed) + " km/h",
                        (x1, y2 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        COLOR_GREEN, 1, cv2.LINE_AA)
                    lastDistance = distance
        # reset counter
        if ct >= 1000:
            ct = 0
        cv2.imshow("Frame", render_frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
