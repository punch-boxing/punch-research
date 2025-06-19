import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

class Punch:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = pd.read_csv(f"./datas/{file_name}.csv")
        
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
        _initial_vector = _initial_vector
        
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
        
        