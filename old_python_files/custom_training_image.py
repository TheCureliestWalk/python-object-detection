import torch
import numpy as np
import cv2

model = torch.hub.load('ultralytics/yolov5', 'custom', path='data/last.pt', force_reload=True)

cap = cv2.imread('img/real_sit.jpg')


while cap.isOpened():
    ret, frame = cap.read()
    result = model(frame)
    cv2.imshow("Frame", np.squeeze(result.render()))
    key = cv2.waitKey(30)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
