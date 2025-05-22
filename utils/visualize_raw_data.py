import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(f'./datas/{input("what file would you like to visualize\n: ")}.csv')
time = data['time']
acceleration_x = data['x']
acceleration_y = data['y']
acceleration_z = data['z']

plt.figure(figsize=(16, 12))
plt.subplot(3, 1, 1)
plt.plot(time, acceleration_x, label='Acceleration X', color='red')
plt.title('Acceleration X vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s²)')
plt.legend()
plt.grid()
plt.subplot(3, 1, 2)
plt.plot(time, acceleration_y, label='Acceleration Y', color='green')
plt.title('Acceleration Y vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s²)')
plt.legend()
plt.grid()
plt.subplot(3, 1, 3)
plt.plot(time, acceleration_z, label='Acceleration Z', color='blue')
plt.title('Acceleration Z vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s²)')
plt.legend()
plt.grid()
plt.show()