from math import sqrt, pow
from turtle import distance
import torch
import numpy as np
import cv2
import os
import time
from PIL import ImageGrab
import pandas as pd
from data import tracker

# Change distance according to real path.
# -------------------------------------------
realDistance = 20 # in meters
# -------------------------------------------

# Init tracker objects
tracker = tracker.EuclideanDistTracker()
#eDist = dist.InitDistanceCalculation()

model = torch.hub.load('ultralytics/yolov5', 'custom', path='data/last.pt', force_reload=True)
#model_name = 'last.pt'
#model = torch.hub.load(os.getcwd(), 'data', source='local', path=model_name, force_reload=True).eval()
model.conf = 0.5  # NMS confidence threshold
model.iou = 0.5  # NMS IoU threshold
model.agnostic = False  # NMS class-agnostic
model.multi_label = False  # NMS multiple labels per box
# (optional list) filter by class, i.e. = [0, 15, 16] for COCO persons, cats and dogs
model.classes = None
model.max_det = 1000  # maximum number of detections per image
model.amp = False  # Automatic Mixed Precision (AMP) inference

cap = cv2.VideoCapture("rtsp://iho:1q2w3e4r%40iho@10.88.240.172/axis-media/media.amp?videocodec=h264&resolution=640x480")
#cap.set(cv2.CAP_PROP_FPS, 5.0)
#cap = cv2.VideoCapture("vid/Volkswagen - 7272.mp4")
# Variables
COLOR_RED = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (255, 0, 0)
COLOR_YELLOW = (0, 255, 255)
line_pos = [(56, 298), (583, 600)]
# Detection Area poly lines
detection_area = np.array([[(47,265), (559,264), (636,407), (22,391)]], dtype=np.int32)

x_shape = 640 # width of source
y_shape = 480 # height of source
ct = 0 #counter
last_x, last_y = 0, 0
# processing time
startTime = 0
endTime = 1

lastDistance = 0

def findCenterPoint(x1, y1, x2, y2): # return distance in meters
    center_x, center_y = int((x1 + x2) / 2), int((y1 + y2) / 2)
    return center_x, center_y

def calcEuclidean(current_x, current_y, last_x, last_y):
    output = sqrt(abs(pow(current_x-last_x, 2) + pow(current_y-last_y, 2)))
    return output



while True:
    ct += 1 # using counter for seek to last frame of RTSP
    rect = cap.grab()
    if ct % 5 == 0:
        ret, frame = cap.read()
        source_fps = cap.get(cv2.CAP_PROP_FPS)
        frame = [frame]
        result = model(frame)

        render_frame = np.squeeze(result.render())
        render_frame = cv2.resize(render_frame, [640, 480], interpolation = cv2.INTER_AREA)
        # detection box
        labels, cord = result.xyxyn[0][:, -1], result.xyxyn[0][:, :-1]
        boxes = []  # Empty list for each box
        n = len(labels) # print labels -> 4. car // 15. motorcycle
        for i in range(n):
            startTime = time.perf_counter  # timer in seconds
            row = cord[i]
            if row[4] >= 0.5: #Confidence level
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                # find center points
                center_x, center_y = findCenterPoint(x1, y1, x2, y2)
                # keep as current position
                current_x, current_y = center_x, center_y
                print(current_x, current_y)
                cv2.circle(render_frame, (center_x, center_y), 5, COLOR_GREEN, -1)
                # Put all coordinates into boxes variable
                boxes.append([x1, y1, x2, y2]) # current box
                boxes_tracker = tracker.update(boxes) # automatic print to console output
                for box_tracker in boxes_tracker:
                    x1, y1, x2, y2, id = box_tracker # get coordinates each car
                    cv2.putText(render_frame, "id: " + str(id), (x1, y2 + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_YELLOW, 1, cv2.LINE_AA)

                    # get Euclidean Distance
                    euclideanDist = calcEuclidean(current_x, current_y, last_x, last_y)
                    #print(euclideanDist)
                    fps = source_fps # ref from inference time about 250 ms
                    speed = round(
                        ((euclideanDist*realDistance) / (fps)) * 3.6, 2) # m/s -> km/h
                    endTime = time.time()
                    cv2.putText(
                        render_frame,
                        "speed: " + str(speed) + " km/h",
                        (x1, y2 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        COLOR_GREEN, 1, cv2.LINE_AA)
                    # change these position to last position
                    last_x, last_y = current_x, current_y
        # reset counter
        if ct >= 1000:
            ct = 0
        cv2.imshow("Frame", render_frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
