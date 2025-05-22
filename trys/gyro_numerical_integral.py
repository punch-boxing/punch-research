import pandas as pd
import matplotlib.pyplot as plt

import numerical_integral

data = pd.read_csv('./datas/up_down.csv')
time = data['time']
acceleration_x = data['x']
acceleration_y = data['y']
acceleration_z = data['z']
gyro_x = data['roll']
gyro_y = data['pitch']
gyro_z = data['yaw']

angle_x = numerical_integral.numerical_integration(gyro_x, time)
angle_y = numerical_integral.numerical_integration(gyro_y, time)
angle_z = numerical_integral.numerical_integration(gyro_z, time)

plt.figure(figsize=(16, 12))
plt.subplot(3, 1, 1)
plt.plot(time, angle_x, label='Angle X', color='red')
plt.plot(time, gyro_x, label='Gyro X', color='orange')
plt.title('Angle X vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Angle (rad)')
plt.legend()
plt.grid()
plt.subplot(3, 1, 2)
plt.plot(time, angle_y, label='Angle Y', color='green')
plt.plot(time, gyro_y, label='Gyro Y', color='yellow')
plt.title('Angle Y vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Angle (rad)')
plt.legend()
plt.grid()
plt.subplot(3, 1, 3)
plt.plot(time, angle_z, label='Angle Z', color='blue')
plt.plot(time, gyro_z, label='Gyro Z', color='purple')
plt.title('Angle Z vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Angle (rad)')
plt.legend()
plt.grid()
plt.show()