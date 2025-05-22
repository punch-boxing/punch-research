import numpy as np
import pandas as pd

class SensorData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.index = self.data['index']
        self.time = self.data['time']
        self.acceleration_x = self.data['acc x']
        self.acceleration_y = self.data['acc y']
        self.acceleration_z = self.data['acc z']
        self.velocity_x = None
        self.velocity_y = None
        self.velocity_z = None
        self.position_x = None
        self.position_y = None
        self.position_z = None
        self.gyro_x = self.data['gyro x']
        self.gyro_y = self.data['gyro y']
        self.gyro_z = self.data['gyro z']
        self.pitch = None
        self.roll = None
        self.yaw = None
        self.magnetometer_x = self.data['mag x']
        self.magnetometer_y = self.data['mag y']
        self.magnetometer_z = self.data['mag z']

    def calculate_velocity(self):
        dt = np.diff(self.time)
        self.velocity_x = np.cumsum(self.acceleration_x[:-1] * dt)
        self.velocity_y = np.cumsum(self.acceleration_y[:-1] * dt)
        self.velocity_z = np.cumsum(self.acceleration_z[:-1] * dt)

    def calculate_position(self):
        dt = np.diff(self.time)
        self.position_x = np.cumsum(self.velocity_x[:-1] * dt)
        self.position_y = np.cumsum(self.velocity_y[:-1] * dt)
        self.position_z = np.cumsum(self.velocity_z[:-1] * dt)
    