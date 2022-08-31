#This project uses MobileNetSSD to detect cars
import numpy as np
import imutils
import cv2

use_gpu = False # Using AMD it will fallback to CPU automatically.
confidence_level = 0.4

CATEGORIES = { 0: 'background', 1: 'aeroplane', 2: 'bicycle', 3: 'bird', 
               4: 'boat', 5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 
               9: 'chair', 10: 'cow', 11: 'diningtable', 12: 'dog', 
              13: 'horse', 14: 'motorbike', 15: 'person', 
              16: 'pottedplant', 17: 'sheep', 18: 'sofa', 
              19: 'train', 20: 'tvmonitor'}
 
CLASSES =  ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", 
            "bus", "car", "cat", "chair", "cow", 
           "diningtable",  "dog", "horse", "motorbike", "person", 
           "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
# Random number from 0-255 with size of 'CLASSES', 3 -> [B, G, R]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# Using Deep Neural Network from MobileNet SSD
net = cv2.dnn.readNetFromCaffe('ssd_files/MobileNetSSD_deploy.prototxt', 'ssd_files/MobileNetSSD_deploy.caffemodel')

# IF NVIDIA CUDA is present
if use_gpu:
    print("[INFO] Using CUDA.")
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    
# Start streaming  
print(f'[INFO] OpenCV {cv2.__version__}')
print("[INFO] Reading Streaming video")

vs = cv2.VideoCapture('vid/highway.mp4')

while True:
    rect, frame = vs.read()
    if rect == True:
        frame = imutils.resize(frame, height=300)
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), (127.5, 127.5, 127.5))
        # Predict
        net.setInput(blob)
        detections = net.forward()
        
        # start line     
       # cv2.line(frame, (167,175), (291,175), (0,0,255), 2)
        # end line
       # cv2.line(frame, (126, 233), (326, 233), (0, 0, 255), 2)
        
        # Time for prob.
        for i in np.arange(0, detections.shape[2]):
            # confidence of prediction
            confidence = detections[0, 0, i, 2]
            
            if confidence > confidence_level: # If confidence > threshold
                # class label
                idx = int(detections[0, 0, i, 1])
                
                # Draw box and label
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int16")
                # label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100) # make it to readable %
                label = CLASSES[idx]
                print(label)
                
                if label == "car" or label == "bus":
                    label = "car"
                elif label == "motorbike" or label == "person" or label == "bicycle":
                    label = "motorcycle"
                    
                cv2.rectangle(frame, (startX, startY),(endX, endY), (0, 255, 255), 2)  # thickness
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
        cv2.imshow('Live detection',frame)
        
    if cv2.waitKey(22) == 27: # or (cv2.waitKey(22) & 0xFF == ord('q')):  # press ESC
        break
            
vs.release()
cv2.destroyAllWindows()
