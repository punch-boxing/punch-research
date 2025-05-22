import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


fft_data = pd.read_csv('./datas/stable.csv')
fft_time = fft_data['time']
fft_acceleration_x = fft_data['x']
fft_acceleration_y = fft_data['y']
fft_acceleration_z = fft_data['z']

# # Apply Fast Fourier Transform (FFT) to the acceleration data
# Compute the FFT
n = len(fft_time)

fft_x = np.fft.fft(fft_acceleration_x)
fft_x_single = np.abs(fft_x[:n//2])
fft_x_single[1:] = 2 * fft_x_single[1:]

fft_y = np.fft.fft(fft_acceleration_y)
fft_y_single = np.abs(fft_y[:n//2])
fft_y_single[1:] = 2 * fft_y_single[1:]

fft_z = np.fft.fft(fft_acceleration_z)
fft_z_single = np.abs(fft_z[:n//2])
fft_z_single[1:] = 2 * fft_z_single[1:]

frequencies = np.fft.fftfreq(len(fft_time), d=(fft_time[1] - fft_time[0]))

plt.figure(figsize=(16, 12))
plt.subplot(3, 1, 1)
plt.plot(frequencies, np.abs(fft_x/frequencies), label='FFT Acceleration X', color='red')
plt.title('FFT of Acceleration X')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.legend()
plt.grid()
plt.subplot(3, 1, 2)
plt.plot(frequencies, np.abs(fft_y/frequencies), label='FFT Acceleration Y', color='green')
plt.title('FFT of Acceleration Y')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.legend()
plt.grid()
plt.subplot(3, 1, 3)
plt.plot(frequencies, np.abs(fft_z/frequencies), label='FFT Acceleration Z', color='blue')
plt.title('FFT of Acceleration Z')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.legend()
plt.grid()
plt.show()




# data = pd.read_csv('./datas/up_down_fast.csv')
# time = data['time']
# acceleration_x = data['x']
# acceleration_y = data['y']
# acceleration_z = data['z']


# # Set a threshold to filter out high-frequency noise
# # threshold = 0.1
# # fft_x[np.abs(fft_x) < threshold] = 0
# # fft_y[np.abs(fft_y) < threshold] = 0
# # fft_z[np.abs(fft_z) < threshold] = 0


# # Apply inverse FFT to get the filtered acceleration data
# filtered_acceleration_x = np.fft.ifft(acceleration_x)
# filtered_acceleration_y = np.fft.ifft(acceleration_y)
# filtered_acceleration_z = np.fft.ifft(acceleration_z)

# plt.figure(figsize=(16, 12))
# plt.subplot(3, 1, 1)
# plt.plot(time, acceleration_x, label='Original Acceleration X', color='red')
# plt.plot(time, filtered_acceleration_x.real, label='Filtered Acceleration', color='blue')
# plt.title('Acceleration X vs Time')
# plt.xlabel('Time (s)')
# plt.ylabel('Acceleration (m/s²)')
# plt.legend()
# plt.grid()
# plt.subplot(3, 1, 2)
# plt.plot(time, acceleration_y, label='Original Acceleration Y', color='red')
# plt.plot(time, filtered_acceleration_y.real, label='Filtered Acceleration', color='blue')
# plt.title('Acceleration Y vs Time')
# plt.xlabel('Time (s)')
# plt.ylabel('Acceleration (m/s²)')
# plt.legend()
# plt.grid()
# plt.subplot(3, 1, 3)
# plt.plot(time, acceleration_z, label='Original Acceleration Z', color='red')
# plt.plot(time, filtered_acceleration_z.real, label='Filtered Acceleration', color='blue')
# plt.title('Acceleration Z vs Time')
# plt.xlabel('Time (s)')
# plt.ylabel('Acceleration (m/s²)')
# plt.legend()
# plt.grid()
# plt.show()
