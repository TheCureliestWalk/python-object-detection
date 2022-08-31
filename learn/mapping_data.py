# keys
from msilib.schema import Error


data1 = ["Iho", "Pui", "Keq", "Raph"]
# values
data2 = [3.8, 3.7, 2.0, 2.3, 5]


data = {}

# map name with gpx
# for i, j in enumerate(name):
#     print(i, j)


# print(data)

# check range of data1 and data2 must be equal
if range(len(data1)) == range(len(data2)):
     for counter, index  in enumerate(data1):
          data[data1[counter]] = data2[counter]
     print(data)
else:
     raise Exception("The number of keys or values are not same.")