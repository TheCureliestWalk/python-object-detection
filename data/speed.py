from math import sqrt, pow
import numpy as np
def calcEuclidean(center_x, center_y):
    output = sqrt(abs(pow(center_x, 2) + pow(center_y, 2)))
    return output

lastTracking = 0

for i in range(1,11): # 10 times

    c = [i*3, i*5]

    currentTracking = calcEuclidean(c[0], c[1])
    diff = currentTracking - lastTracking
    print(round(diff, 2))
    lastTracking = currentTracking
