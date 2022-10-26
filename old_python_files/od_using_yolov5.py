import os
import cv2
import numpy as np
import imutils
import time
from PIL import Image
# Include custom data
from data import classes as classes
from data import tracker


# Constants.
INPUT_WIDTH = 640
INPUT_HEIGHT = 640
SCORE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.45
CONFIDENCE_THRESHOLD = 0.45

# Text parameters.
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
THICKNESS = 1

# Colors in B G R
BLACK = (0, 0, 0)
BLUE = (255, 178, 50)
YELLOW = (0, 255, 255)
RED = (0, 0, 255)
GREEN = (0, 255, 0)

classes = list(classes.classes_dict.values())
tracker = tracker.EuclideanDistTracker()

detection_save_dir = "saved_pic"
image_dir = os.path.join('data', 'images')
print(image_dir)
def draw_label(input_image, label, left, top):
    """Draw text onto image at location."""

    # Get text size.
    text_size = cv2.getTextSize(label, FONT_FACE, FONT_SCALE, THICKNESS)
    dim, baseline = text_size[0], text_size[1]
    # Use text size to create a BLACK rectangle.
    cv2.rectangle(input_image, (left, top),
                  (left + dim[0], top + dim[1] + baseline), BLACK, cv2.FILLED)
    # Display text inside the rectangle and convert to %
    cv2.putText(input_image, label, (left, top +
                dim[1]), FONT_FACE, FONT_SCALE, YELLOW, THICKNESS, cv2.LINE_AA)


def pre_process(input_image, net):
    # Create a 4D blob from a frame.
    blob = cv2.dnn.blobFromImage(
        input_image, 1/255, (INPUT_WIDTH, INPUT_HEIGHT), [0, 0, 0], 1, crop=False)

    # Sets the input to the network.
    net.setInput(blob)

    # Runs the forward pass to get output of the output layers.
    output_layers = net.getUnconnectedOutLayersNames()
    outputs = net.forward(output_layers)
    # print(outputs[0].shape)

    return outputs


def post_process(input_image, outputs):
    # Lists to hold respective values while unwrapping.
    class_ids = []
    confidences = []
    boxes = []

    # Rows.
    rows = outputs[0].shape[1]

    image_height, image_width = input_image.shape[:2]

    # Resizing factor.
    x_factor = image_width / INPUT_WIDTH
    y_factor = image_height / INPUT_HEIGHT

    # Iterate through 25200 detections.
    for r in range(rows):
        row = outputs[0][0][r]
        confidence = row[4]

        # Discard bad detections and continue.
        if confidence >= CONFIDENCE_THRESHOLD:
            classes_scores = row[5:]

            # Get the index of max class score.
            class_id = np.argmax(classes_scores)

            #  Continue if the class score is above threshold.
            if (classes_scores[class_id] > SCORE_THRESHOLD):
                confidences.append(confidence)
                class_ids.append(class_id)

                cx, cy, w, h = row[0], row[1], row[2], row[3]

                left = int((cx - w/2) * x_factor)
                top = int((cy - h/2) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)

                box = np.array([left, top, width, height])
                boxes.append(box)
                
                

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv2.dnn.NMSBoxes(
        boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    for i in indices:
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        cv2.rectangle(input_image, (left, top), (left + width, top + height), GREEN, 2*THICKNESS)
        label = "{}:{:.2f}".format(classes[class_ids[i]], confidences[i])
        draw_label(input_image, label, left, top)
        
        # Object tracking
        boxes_id = tracker.update(boxes)
        for box_id in boxes_id:
            left, top, width, height, id = box_id
            #cv2.putText(input_image, str(id), (left, top-15), FONT_FACE , FONT_SCALE, YELLOW, THICKNESS)
            draw_label(input_image, str(id), left-15, top)
            
    return input_image

def savePic(img):
    # Get current time for file name
    currentTime = time.strftime("D-%d-%m-%Y-T-%HH-%MM-%SS")
    # Save pic
    getImg = Image.fromarray(img)
    getImg.save(detection_save_dir + "/" + currentTime + ".jpg")

if __name__ == '__main__':

    #cap = cv2.VideoCapture("vid/211212_02_Jakarta_4k_018.mp4")
    #cap = cv2.VideoCapture("rtsp://prawee:1q2w3e4r@10.88.97.100:554/cam/realmonitor?channel=6&subtype=0")
    cap = cv2.VideoCapture(
        "rtsp://iho:1q2w3e4r%40iho@10.88.240.172/axis-media/media.amp?videocodec=h264&resolution=640x480")
    
    # Seek to ast frame from rtsp
    ct = 0
    while True:
        ct += 1
        rect = cap.grab()
        if ct % 5 == 0:
            rect, frame = cap.retrieve()
            #frame = imutils.resize(frame, height=640) // not using this since rtsp can resize itself.
            net = cv2.dnn.readNet("data/yolov5s.onnx")
            detections = pre_process(frame, net)
            img = post_process(frame.copy(), detections)
            t, _ = net.getPerfProfile()
            label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
            print(label)
     
        # Draw line
            cv2.line(img, [355, 360], [738, 360], RED, 2*THICKNESS)
            cv2.line(img, [192, 613], [970, 613], RED, 2*THICKNESS)
     
            cv2.putText(img, label, (20, 40), FONT_FACE, FONT_SCALE, RED, THICKNESS, cv2.LINE_AA)
            cv2.imshow('Detection', img)
     
            # Uncomment to save pic
            # savePic(img)
    

        if cv2.waitKey(30) == ord('q'):
            break
            
     

cap.release()
cv2.destroyAllWindows()
