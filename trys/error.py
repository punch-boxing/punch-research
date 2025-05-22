# first attempt

# # this file is used to calculate the range of error of acceleometer

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler


# data = pd.read_csv('./datas/error2.csv')
# time = data['time']

# acceleration_x = data['x']
# acceleration_y = data['y']
# acceleration_z = data['z']


# print(f"Median Acceleration X : {(max(acceleration_x) - min(acceleration_x))/2}")
# print(f"Median Acceleration Y : {(max(acceleration_y) - min(acceleration_y))/2}")
# print(f"Median Acceleration Z : {(max(acceleration_z) - min(acceleration_z))/2}")
# print(f"Median Acceleration : {(((max(acceleration_x) - min(acceleration_x))/2 + (max(acceleration_y) - min(acceleration_y))/2 + (max(acceleration_z) - min(acceleration_z))/2)/3)}")


# plt.figure(figsize=(16, 12))
# plt.subplot(3, 1, 1)
# plt.hist(acceleration_x, bins=100, alpha=0.5, label='Acceleration X', color='red')
# plt.grid()
# plt.subplot(3, 1, 2)
# plt.hist(acceleration_y, bins=100, alpha=0.5, label='Acceleration Y', color='green')
# plt.grid()
# plt.subplot(3, 1, 3)
# plt.hist(acceleration_z, bins=100, alpha=0.5, label='Acceleration Z', color='blue')
# plt.grid()
# plt.show()

# # Median Acceleration X : 0.6808624267578125
# # Median Acceleration Y : 0.3876190185546875
# # Median Acceleration Z : 0.5081558227539062
# # Median Acceleration : 0.5255457560221354
# # from the calculation, we can see that the error of the acceleometer is about 0.5 m/s^2
# # thus, we should drop the data that has less difference(absolute value of [current acceleration - previous acceleration]) than 0.5 m/s^2

# the error is not accurate since gravity envolves

# second attempt


data = pd.read_csv('./datas/up_down_fast.csv')
time = data['time']

acceleration_x = data['x']
acceleration_y = data['y']
acceleration_z = data['z']


print(f"Median Acceleration X : {(max(acceleration_x) - min(acceleration_x))/2}")
print(f"Median Acceleration Y : {(max(acceleration_y) - min(acceleration_y))/2}")
print(f"Median Acceleration Z : {(max(acceleration_z) - min(acceleration_z))/2}")
print(f"Median Acceleration : {(((max(acceleration_x) - min(acceleration_x))/2 + (max(acceleration_y) - min(acceleration_y))/2 + (max(acceleration_z) - min(acceleration_z))/2)/3)}")


plt.figure(figsize=(16, 12))
plt.subplot(3, 1, 1)
plt.hist(acceleration_x, bins=100, alpha=0.5, label='Acceleration X', color='red')
plt.grid()
plt.subplot(3, 1, 2)
plt.hist(acceleration_y, bins=100, alpha=0.5, label='Acceleration Y', color='green')
plt.grid()
plt.subplot(3, 1, 3)
plt.hist(acceleration_z, bins=100, alpha=0.5, label='Acceleration Z', color='blue')
plt.grid()
plt.show()