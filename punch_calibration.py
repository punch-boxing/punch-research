import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

class PunchCalibration:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = pd.read_csv(file_name)
        
        self.index = self.data['index']
        self.time = self.data['time']
        
        try:
            self.raw_acceleration_x = self.data['acc x'].copy()
            self.raw_acceleration_y = self.data['acc y'].copy()
            self.raw_acceleration_z = self.data['acc z'].copy()
            
            self.acceleration_x = self.raw_acceleration_x.copy()
            self.acceleration_y = self.raw_acceleration_y.copy()
            self.acceleration_z = self.raw_acceleration_z.copy()
            
            self.gyro_x = self.data['gyro x'].copy()
            self.gyro_y = self.data['gyro y'].copy()
            self.gyro_z = self.data['gyro z'].copy()
            
            self.magnetometer_x = self.data['mag x'].copy()
            self.magnetometer_y = self.data['mag y'].copy()
            self.magnetometer_z = self.data['mag z'].copy()
            
        except KeyError as e:
            input("Error: Missing column in the CSV file. Would you like to continue? (y/n): ")
            if input().lower() != 'y':
                raise e
            
        self.initialize_orientation()
        self.calculate_gravity()
        
        self.remove_gravity()
        # self.correct_acceleration()
        
        self.calculate_velocity()
        self.calculate_position()
        
    # def correct_acceleration(self):
    #     _threshold = 0.1
    #     self.acceleration_x = [0.0 if abs(a) < _threshold else a for a in self.acceleration_x]
    #     self.acceleration_y = [0.0 if abs(a) < _threshold else a for a in self.acceleration_y]
    #     self.acceleration_z = [0.0 if abs(a) < _threshold else a for a in self.acceleration_z]

    def remove_gravity(self):
        self.acceleration_x = self.acceleration_x - self.gravity_x
        self.acceleration_y = self.acceleration_y - self.gravity_y
        self.acceleration_z = self.acceleration_z - self.gravity_z
        
    def calculate_gravity(self):
        _gravity_x = []
        _gravity_y = []
        _gravity_z = []
        
        for i in range(len(self.time)):
            _gravity_x.append(np.sin(self.rotation_z[i]))
            _gravity_y.append(- np.cos(self.rotation_x[i]) * np.cos(self.rotation_z[i]))
            _gravity_z.append(np.sin(self.rotation_x[i]) * np.cos(self.rotation_z[i]))
            
        self.gravity_x = pd.Series(_gravity_x, index=self.index)
        self.gravity_y = pd.Series(_gravity_y, index=self.index)
        self.gravity_z = pd.Series(_gravity_z, index=self.index)

    def calculate_velocity(self):
        self.velocity_x = self.numerical_integration(self.acceleration_x, self.time)
        self.velocity_y = self.numerical_integration(self.acceleration_y, self.time)
        self.velocity_z = self.numerical_integration(self.acceleration_z, self.time)

    def calculate_position(self):
        self.position_x = self.numerical_integration(self.velocity_x, self.time)
        self.position_y = self.numerical_integration(self.velocity_y, self.time)
        self.position_z = self.numerical_integration(self.velocity_z, self.time)
        
    def numerical_integration(self, integrand, index):
        result = [0.0]
        for i in range(1, len(integrand)):
            result.append((integrand[i]+integrand[i-1])*(index[i]-index[i-1]) / 2 + result[i-1])
        return result
    
    def short_integration(self, start, end):
        _x = self.numerical_integration_with_range(self.acceleration_x, start, end)
        _y = self.numerical_integration_with_range(self.acceleration_y, start, end)
        _z = self.numerical_integration_with_range(self.acceleration_z, start, end)
        
        plt.figure(figsize=(20, 12))
        plt.plot(self.time[start:end + 1], _x, label='Velocity X', color='red')
        plt.plot(self.time[start:end + 1], _y, label='Velocity Y', color='green')
        plt.plot(self.time[start:end + 1], _z, label='Velocity Z', color='blue')
        plt.title('Velocity vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (m/s)')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()
        
    
    def numerical_integration_with_range(self, integrand, start, end):
        result = [0.0]
        for idx, i in enumerate(range(start + 1, end + 1)):
            result.append((integrand[i] + integrand[i - 1]) * (self.time[i] - self.time[i - 1]) / 2 + result[idx - 1])
        return result
    
    def initialize_orientation(self):
        _initial_vector = np.array([self.acceleration_x[0], self.acceleration_y[0], self.acceleration_z[0]])
        _initial_vector = _initial_vector / np.linalg.norm(_initial_vector)
        
        self.initial_rotation_z = np.arcsin(_initial_vector[0])
        self.initial_rotation_y = 0.0
        self.initial_rotation_x = - np.pi - np.arctan2(_initial_vector[2], _initial_vector[1])
        
        print(f"Initial Vector: {_initial_vector}")
        print(f"Initial Rotation: {np.degrees(self.initial_rotation_x)}, {np.degrees(self.initial_rotation_y)}, {np.degrees(self.initial_rotation_z)}")
        
        self.rotation_x = [p + self.initial_rotation_x for p in self.numerical_integration(self.gyro_x, self.time)]
        self.rotation_y = [r + self.initial_rotation_y for r in self.numerical_integration(self.gyro_y, self.time)]
        self.rotation_z = [y + self.initial_rotation_z for y in self.numerical_integration(self.gyro_z, self.time)]
        
    def save_graphs(self, name):
        try:
            plt.savefig(f'./results/{self.file_name}/{name}.png')
        except:
            os.mkdir(f'./results/{self.file_name}')
            self.save_graphs(name)
        # plt.close('all')
        
    def visualize_position(self):
        plt.figure(figsize=(20, 12))
        plt.subplot(3, 1, 1)
        plt.plot(self.time, self.acceleration_x, label='Acceleration X', color='red')
        plt.plot(self.time, self.acceleration_y, label='Acceleration Y', color='green')
        plt.plot(self.time, self.acceleration_z, label='Acceleration Z', color='blue')
        plt.title('Acceleration vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration (m/s²)')
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.plot(self.time, self.velocity_x, label='Velocity X', color='red')
        plt.plot(self.time, self.velocity_y, label='Velocity Y', color='green')
        plt.plot(self.time, self.velocity_z, label='Velocity Z', color='blue')
        plt.title('Velocity vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (m/s)')
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.plot(self.time, self.position_x, label='Position X', color='red')
        plt.plot(self.time, self.position_y, label='Position Y', color='green')
        plt.plot(self.time, self.position_z, label='Position Z', color='blue')
        plt.title('Position vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Position (m)')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        self.save_graphs('position')
        plt.show()
        
    def visualize_removal_of_gravity(self):
        plt.figure(figsize=(20, 12))
        plt.subplot(3, 1, 1)
        plt.plot(self.time, self.raw_acceleration_x, label='Acceleration X', color='red')
        plt.plot(self.time, self.acceleration_x, label='Gravity Removed Acceleration X', color='orange')
        plt.title('Acceleration X vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration X (m/s²)')
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.plot(self.time, self.raw_acceleration_y, label='Acceleration Y', color='green')
        plt.plot(self.time, self.acceleration_y, label='Gravity Removed Acceleration Y', color='lime')
        plt.title('Acceleration Y vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration Y (m/s²)')
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.plot(self.time, self.raw_acceleration_z, label='Acceleration Z', color='blue')
        plt.plot(self.time, self.acceleration_z, label='Gravity Removed Acceleration Z', color='cyan')
        plt.title('Acceleration Z vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration Z (m/s²)')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        self.save_graphs('removal_of_gravity')
        plt.show()
        
    def visualize_rotation(self):
        plt.figure(figsize=(20, 12))
        plt.subplot(3, 1, 1)
        plt.plot(self.time, self.rotation_x, label='Pitch', color='red')
        plt.title('Pitch vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Pitch (rad)')
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.plot(self.time, self.rotation_y, label='Roll', color='green')
        plt.title('Roll vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Roll (rad)')
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.plot(self.time, self.rotation_z, label='Yaw', color='blue')
        plt.title('Yaw vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Yaw (rad)')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        self.save_graphs('rotation')
        plt.show()
        
    def visualize_gravity(self):
        plt.figure(figsize=(20, 12))
        plt.subplot(3, 1, 1)
        plt.plot(self.time, self.gravity_x, label='Gravity X', color='red')
        plt.title('Gravity X vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Gravity X (m/s²)')
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.plot(self.time, self.gravity_y, label='Gravity Y', color='green')
        plt.title('Gravity Y vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Gravity Y (m/s²)')
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.plot(self.time, self.gravity_z, label='Gravity Z', color='blue')
        plt.title('Gravity Z vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Gravity Z (m/s²)')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        self.save_graphs('gravity')
        plt.show()
        
    def remove_noise_by_kalman_filter(self):
        from pykalman import KalmanFilter
        
        kf_x = KalmanFilter(initial_state_mean=0, n_dim_obs=1)
        kf_x = kf_x.em(self.acceleration_x, n_iter=10)
        (filtered_state_means_x, filtered_state_covariances) = kf_x.filter(self.acceleration_x)
        
        kf_y = KalmanFilter(initial_state_mean=0, n_dim_obs=1)
        kf_y = kf_y.em(self.acceleration_y, n_iter=10)
        (filtered_state_means_y, filtered_state_covariances_y) = kf_y.filter(self.acceleration_y)
        
        kf_z = KalmanFilter(initial_state_mean=0, n_dim_obs=1)
        kf_z = kf_z.em(self.acceleration_z, n_iter=10)
        (filtered_state_means_z, filtered_state_covariances_z) = kf_z.filter(self.acceleration_z)
        
        kf_speed_x = self.numerical_integration(filtered_state_means_x.flatten(), self.time)
        kf_speed_y = self.numerical_integration(filtered_state_means_y.flatten(), self.time)
        kf_speed_z = self.numerical_integration(filtered_state_means_z.flatten(), self.time)
        
        kf_position_x = self.numerical_integration(kf_speed_x, self.time)
        kf_position_y = self.numerical_integration(kf_speed_y, self.time)
        kf_position_z = self.numerical_integration(kf_speed_z, self.time)
        
        # plt.figure(figsize=(20, 12))
        # plt.subplot(3, 1, 1)
        # plt.plot(self.time, self.acceleration_x, label='Raw Data', color='blue')
        # plt.plot(self.time, filtered_state_means_x, label='Kalman Filtered Data', color='red')
        # plt.xlabel('Time (s)')
        # plt.ylabel('Acceleration X (m/s²)')
        # plt.title('Kalman Filter on Acceleration X Data')
        # plt.legend()
        # plt.grid()
        # plt.subplot(3, 1, 2)
        # plt.plot(self.time, self.acceleration_y, label='Raw Data', color='blue')
        # plt.plot(self.time, filtered_state_means_y, label='Kalman Filtered Data', color='red')
        # plt.xlabel('Time (s)')
        # plt.ylabel('Acceleration Y (m/s²)')
        # plt.title('Kalman Filter on Acceleration Y Data')
        # plt.legend()
        # plt.grid()
        # plt.subplot(3, 1, 3)
        # plt.plot(self.time, self.acceleration_z, label='Raw Data', color='blue')
        # plt.plot(self.time, filtered_state_means_z, label='Kalman Filtered Data', color='red')
        # plt.xlabel('Time (s)')
        # plt.ylabel('Acceleration Z (m/s²)')
        # plt.title('Kalman Filter on Acceleration Z Data')
        # plt.legend()
        # plt.grid()
        # plt.tight_layout()
        # plt.show()
        
        plt.figure(figsize=(20, 12))
        plt.subplot(3, 1, 1)
        plt.plot(self.time, kf_speed_x, label='Kalman Filtered Velocity X', color='red')
        plt.plot(self.time, self.velocity_x, label='Raw Velocity X', color='orange')
        plt.title('Kalman Filtered Velocity X vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity X (m/s)')
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.plot(self.time, kf_speed_y, label='Kalman Filtered Velocity Y', color='green')
        plt.plot(self.time, self.velocity_y, label='Raw Velocity Y', color='lime')
        plt.title('Kalman Filtered Velocity Y vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity Y (m/s)')
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.plot(self.time, kf_speed_z, label='Kalman Filtered Velocity Z', color='blue')
        plt.plot(self.time, self.velocity_z, label='Raw Velocity Z', color='cyan')
        plt.title('Kalman Filtered Velocity Z vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity Z (m/s)')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()
        
        plt.figure(figsize=(20, 12))
        plt.subplot(3, 1, 1)
        plt.plot(self.time, kf_position_x, label='Kalman Filtered Position X', color='red')
        plt.plot(self.time, self.position_x, label='Raw Position X', color='orange')
        plt.title('Kalman Filtered Position X vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Position X (m)')
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.plot(self.time, kf_position_y, label='Kalman Filtered Position Y', color='green')
        plt.plot(self.time, self.position_y, label='Raw Position Y', color='lime')
        plt.title('Kalman Filtered Position Y vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Position Y (m)')
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.plot(self.time, kf_position_z, label='Kalman Filtered Position Z', color='blue')
        plt.plot(self.time, self.position_z, label='Raw Position Z', color='cyan')
        plt.title('Kalman Filtered Position Z vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Position Z (m)')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()
        
    def remove_noise_by_fft(self):
        from scipy.fft import fft, ifft
        
        def remove_noise(signal, threshold=0.1):
            signal_fft = fft(signal)
            signal_fft[np.abs(signal_fft) < threshold] = 0
            return ifft(signal_fft).real
        
        fft_x = remove_noise(self.acceleration_x)
        fft_y = remove_noise(self.acceleration_y)
        fft_z = remove_noise(self.acceleration_z)
        
        fft_speed_x = self.numerical_integration(fft_x, self.time)
        fft_speed_y = self.numerical_integration(fft_y, self.time)
        fft_speed_z = self.numerical_integration(fft_z, self.time)
        
        fft_position_x = self.numerical_integration(fft_speed_x, self.time)
        fft_position_y = self.numerical_integration(fft_speed_y, self.time)
        fft_position_z = self.numerical_integration(fft_speed_z, self.time)
        
        plt.figure(figsize=(20, 12))
        plt.subplot(3, 1, 1)
        plt.plot(self.time, fft_x, label='FFT Filtered Acceleration X', color='red')
        plt.plot(self.time, self.acceleration_x, label='Raw Acceleration X', color='orange')
        plt.title('FFT Filtered Acceleration X vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration X (m/s²)')
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.plot(self.time, fft_y, label='FFT Filtered Acceleration Y', color='green')
        plt.plot(self.time, self.acceleration_y, label='Raw Acceleration Y', color='lime')
        plt.title('FFT Filtered Acceleration Y vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration Y (m/s²)')
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.plot(self.time, fft_z, label='FFT Filtered Acceleration Z', color='blue')
        plt.plot(self.time, self.acceleration_z, label='Raw Acceleration Z', color='cyan')
        plt.title('FFT Filtered Acceleration Z vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration Z (m/s²)')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()
        
        plt.figure(figsize=(20, 12))
        plt.subplot(3, 1, 1)
        plt.plot(self.time, fft_speed_x, label='FFT Filtered Velocity X', color='red')
        plt.plot(self.time, self.velocity_x, label='Raw Velocity X', color='orange')
        plt.title('FFT Filtered Velocity X vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity X (m/s)')
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.plot(self.time, fft_speed_y, label='FFT Filtered Velocity Y', color='green')
        plt.plot(self.time, self.velocity_y, label='Raw Velocity Y', color='lime')
        plt.title('FFT Filtered Velocity Y vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity Y (m/s)')
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.plot(self.time, fft_speed_z, label='FFT Filtered Velocity Z', color='blue')
        plt.plot(self.time, self.velocity_z, label='Raw Velocity Z', color='cyan')
        plt.title('FFT Filtered Velocity Z vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity Z (m/s)')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()
        
        plt.figure(figsize=(20, 12))
        plt.subplot(3, 1, 1)
        plt.plot(self.time, fft_position_x, label='FFT Filtered Position X', color='red')
        plt.plot(self.time, self.position_x, label='Raw Position X', color='orange')
        plt.title('FFT Filtered Position X vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Position X (m)')
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.plot(self.time, fft_position_y, label='FFT Filtered Position Y', color='green')
        plt.plot(self.time, self.position_y, label='Raw Position Y', color='lime')
        plt.title('FFT Filtered Position Y vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Position Y (m)')
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.plot(self.time, fft_position_z, label='FFT Filtered Position Z', color='blue')
        plt.plot(self.time, self.position_z, label='Raw Position Z', color='cyan')
        plt.title('FFT Filtered Position Z vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Position Z (m)')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()