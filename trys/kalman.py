from pykalman import KalmanFilter
import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt

# Read the data
data = pd.read_csv('./datas/up_down.csv')

time = data['time']
acceleration_x = data['x']
acceleration_y = data['y']
acceleration_z = data['z']

# Enhanced low-pass filter using scipy.signal for better performance

# Design a Butterworth low-pass filter
fs = 1.0 / np.mean(np.diff(time))  # Calculate sampling frequency
cutoff = 0.5  # Cutoff frequency in Hz (adjust based on your data)
nyquist = 0.5 * fs
order = 4  # Higher order gives sharper frequency cutoff

# Normalize cutoff frequency
normal_cutoff = cutoff / nyquist
b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)

# Apply forward-backward filter to avoid phase shifts (zero-phase filter)
gravity_x = signal.filtfilt(b, a, acceleration_x)
gravity_y = signal.filtfilt(b, a, acceleration_y)
gravity_z = signal.filtfilt(b, a, acceleration_z)

# Alternative: Adaptive filtering with variable alpha based on signal dynamics
# Uncomment if the Butterworth filter is not suitable for your application
"""
alpha_base = 0.05  # Base filter coefficient
alpha_var = np.zeros(len(acceleration_x))
# Make alpha adaptive based on acceleration magnitude
for i in range(len(data)):
    accel_magnitude = np.sqrt(acceleration_x[i]**2 + acceleration_y[i]**2 + acceleration_z[i]**2)
    alpha_var[i] = alpha_base + min(0.2, accel_magnitude / 20)  # Cap at 0.25

gravity_x = np.zeros(len(acceleration_x))
gravity_y = np.zeros(len(acceleration_y))
gravity_z = np.zeros(len(acceleration_z))

# Better initialization using average of first few samples
n_init = min(10, len(data))
gravity_x[0] = np.mean(acceleration_x[:n_init])
gravity_y[0] = np.mean(acceleration_y[:n_init])
gravity_z[0] = np.mean(acceleration_z[:n_init])

for i in range(1, len(data)):
    gravity_x[i] = alpha_var[i] * acceleration_x[i] + (1 - alpha_var[i]) * gravity_x[i-1]
    gravity_y[i] = alpha_var[i] * acceleration_y[i] + (1 - alpha_var[i]) * gravity_y[i-1]
    gravity_z[i] = alpha_var[i] * acceleration_z[i] + (1 - alpha_var[i]) * gravity_z[i-1]
"""

# Remove gravity component from acceleration data
acceleration_x = acceleration_x - gravity_x
acceleration_y = acceleration_y - gravity_y
acceleration_z = acceleration_z - gravity_z

kf = KalmanFilter(
    transition_matrices=[1],
    observation_matrices=[1],
    initial_state_mean=0,
    initial_state_covariance=1,
    observation_covariance=1,
    transition_covariance=0.01,
)

# Apply Kalman filter to the data
state_means_x, state_covariances_x = kf.filter(acceleration_x)
state_means_y, state_covariances_y = kf.filter(acceleration_y)
state_means_z, state_covariances_z = kf.filter(acceleration_z)

# plt.figure(figsize=(10, 6))
# plt.subplot(3, 1, 1)
# plt.plot(data['time'], acceleration_x, label='Raw Data', color='blue')
# plt.plot(data['time'], state_means_x, label='Kalman Filtered Data', color='red')
# plt.xlabel('Time (s)')
# plt.ylabel('X Position (m)')
# plt.title('Kalman Filter on X Position Data')
# plt.legend()

# plt.subplot(3, 1, 2)
# plt.plot(data['time'], acceleration_y, label='Raw Data', color='blue')
# plt.plot(data['time'], state_means_y, label='Kalman Filtered Data', color='red')
# plt.xlabel('Time (s)')
# plt.ylabel('Y Position (m)')
# plt.title('Kalman Filter on Y Position Data')
# plt.legend()

# plt.subplot(3, 1, 3)
# plt.plot(data['time'], acceleration_z, label='Raw Data', color='blue')
# plt.plot(data['time'], state_means_z, label='Kalman Filtered Data', color='red')
# plt.xlabel('Time (s)')
# plt.ylabel('Z Position (m)')
# plt.title('Kalman Filter on Z Position Data')
# plt.legend()
# plt.show()

def numerical_integration(list, index):
    result = [0.0]
    for i in range(1, len(list)):
        result.append((list[i]+list[i-1])*(index[i]-index[i-1]) / 2 + result[i-1])
    return result

velocity_x = numerical_integration(acceleration_x, time)
velocity_y = numerical_integration(acceleration_y, time)
velocity_z = numerical_integration(acceleration_z, time)

position_x = numerical_integration(velocity_x, time)
position_y = numerical_integration(velocity_y, time)
position_z = numerical_integration(velocity_z, time)

# velocity_x = numerical_integration(state_mean_x[::,0], time)
# velocity_y = numerical_integration(state_mean_y[::,0], time)
# velocity_z = numerical_integration(state_mean_z[::,0], time)

# position_x = numerical_integration(velocity_x, time)
# position_y = numerical_integration(velocity_y, time)
# position_z = numerical_integration(velocity_z, time)

plt.figure(figsize=(16, 12))
plt.subplot(2, 1, 1)
plt.plot(time, velocity_x, label='Velocity X', color='red')
plt.plot(time, velocity_y, label='Velocity Y', color='green')
plt.plot(time, velocity_z, label='Velocity Z', color='blue')
plt.title('Velocity vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.legend()
plt.grid()
plt.subplot(2, 1, 2)
plt.plot(time, position_x, label='Position X', color='red')
plt.plot(time, position_y, label='Position Y', color='green')
plt.plot(time, position_z, label='Position Z', color='blue')
plt.title('Position vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.legend()
plt.grid()
plt.show()