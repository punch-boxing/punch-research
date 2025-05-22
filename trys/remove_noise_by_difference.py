import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def numerical_integration(list, index):
    result = [0.0]
    for i in range(1, len(list)):
        result.append((list[i]+list[i-1])*(index[i]-index[i-1]) / 2 + result[i-1])
    return result

def correct_acceleration(acceleration):
    result = [0.0]
    for i in range(1, len(acceleration)):
        result.append(acceleration[i-1] - acceleration[i])
    return result

data = pd.read_csv('./datas/stable.csv')
time = data['time']

acceleration_x = data['x']
acceleration_y = data['y']
acceleration_z = data['z']

corrected_acceleration_x = correct_acceleration(acceleration_x)
corrected_acceleration_y = correct_acceleration(acceleration_y)
corrected_acceleration_z = correct_acceleration(acceleration_z)

corrected_velocity_x = numerical_integration(corrected_acceleration_x, time)
corrected_velocity_y = numerical_integration(corrected_acceleration_y, time)
corrected_velocity_z = numerical_integration(corrected_acceleration_z, time)

corrected_position_x = numerical_integration(corrected_velocity_x, time)
corrected_position_y = numerical_integration(corrected_velocity_y, time)
corrected_position_z = numerical_integration(corrected_velocity_z, time)

plt.figure(figsize=(16, 12))
plt.subplot(3, 1, 1)
plt.plot(time, corrected_acceleration_x, label='Corrected Acceleration X', color='red')
plt.plot(time, corrected_acceleration_y, label='Corrected Acceleration Y', color='green')
plt.plot(time, corrected_acceleration_z, label='Corrected Acceleration Z', color='blue')
plt.title('Acceleration vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s²)')
plt.legend()
plt.grid()
plt.subplot(3, 1, 2)
plt.plot(time, corrected_velocity_x, label='Corrected Acceleration X', color='red')
plt.plot(time, corrected_velocity_y, label='Corrected Acceleration Y', color='green')
plt.plot(time, corrected_velocity_z, label='Corrected Acceleration Z', color='blue')
plt.title('Corrected Acceleration vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Corrected Acceleration (m/s²)')
plt.legend()
plt.grid()
plt.subplot(3, 1, 3)
plt.plot(time, corrected_position_x, label='Corrected Acceleration X', color='red')
plt.plot(time, corrected_position_y, label='Corrected Acceleration Y', color='green')
plt.plot(time, corrected_position_z, label='Corrected Acceleration Z', color='blue')
plt.title('Corrected Acceleration vs Time') 
plt.xlabel('Time (s)')
plt.ylabel('Corrected Acceleration (m/s²)')
plt.legend()
plt.grid()
plt.show()