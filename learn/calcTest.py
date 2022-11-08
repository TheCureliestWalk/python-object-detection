from math import sqrt
a = 2.645833e-7
b = 2.7778e-4
#a = 0.001
#b = 2.7778e-4
#print(a/b)
def calcEuclidean(current_x, current_y, last_x, last_y):
    output = sqrt(abs(pow(current_x - last_x, 2) + pow(current_y - last_y, 2)))
    return output

dist = [(566,285), (566,289), (563,292), (561,292)]

for i in range(len(dist)):
    d = calcEuclidean(dist[i+1][0], dist[i+1][1], dist[i][0], dist[i][1])
    print(d)
