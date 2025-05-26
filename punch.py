import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Punch:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        
        self.index = self.data['index']
        self.time = self.data['time']
        
        try:
            self.acceleration_x = self.data['acc x'].copy()
            self.acceleration_y = self.data['acc y'].copy()
            self.acceleration_z = self.data['acc z'].copy()
            
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
    
    def initialize_orientation(self):
        _initial_vector = np.array([self.acceleration_x[0], self.acceleration_y[0], self.acceleration_z[0]])
        _initial_vector = _initial_vector / np.linalg.norm(_initial_vector)
        _initial_vector = _initial_vector
        
        self.initial_rotation_z = np.arcsin(_initial_vector[0])
        self.initial_rotation_y = 0.0
        self.initial_rotation_x = np.pi - np.arctan2(_initial_vector[2], _initial_vector[1])
        
        print(f"Initial Vector: {_initial_vector}")
        print(f"Initial Rotation: {np.degrees(self.initial_rotation_x)}, {np.degrees(self.initial_rotation_y)}, {np.degrees(self.initial_rotation_z)}")
        
        self.rotation_x = [p + self.initial_rotation_x for p in self.numerical_integration(self.gyro_x, self.time)]
        self.rotation_y = [r + self.initial_rotation_y for r in self.numerical_integration(self.gyro_y, self.time)]
        self.rotation_z = [y + self.initial_rotation_z for y in self.numerical_integration(self.gyro_z, self.time)]
        
    def visualize_position(self):
        plt.figure(figsize=(16, 12))
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
        plt.show()
        
    def visualize_rotation(self):
        plt.figure(figsize=(16, 12))
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
        plt.show()
        
    def visualize_gravity(self):
        plt.figure(figsize=(16, 12))
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
        plt.show()
        
        
        