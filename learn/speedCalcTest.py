from math import sqrt, pow
# camera_height = 3  # distance from camera in meters
# road_distance = 4  # road distance viewed from camera in meters
# distance = sqrt(camera_height**2 + road_distance**2)

# print(distance)

# using Euclidean
boxes = [[182, 92, 228, 130], [617, 123, 637, 158]]
def speedCalc(data):
    for i in data:
        center_x = i[0]+i[2]//2
        print(center_x)






# run function
speed = speedCalc(boxes)