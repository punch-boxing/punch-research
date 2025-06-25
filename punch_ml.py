import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
# from keras.models import Sequential
# from keras.layers import Dense, LSTM, Dropout, Convolution1D, Flatten, Conv2D



class PunchML:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = pd.read_csv(file_name)
        self.index = self.data['index']
        self.time = self.data['time']
        
        try:
            self.acceleration_x = self.data['acc x'].copy()
            self.acceleration_y = self.data['acc y'].copy()
            self.acceleration_z = self.data['acc z'].copy()
            
            self.orientation_x = self.data['sin ori x'].copy()
            self.orientation_y = self.data['sin ori y'].copy()
            self.orientation_z = self.data['sin ori z'].copy()
            
        except KeyError as e:
            input("Error: Missing column in the CSV file. Would you like to continue? (y/n): ")
            if input().lower() != 'y':
                raise e
    
    
            
    def find_local_maxima(self, data):
        _threshold = 2
        peaks, properties = find_peaks(data, height=np.mean(data), distance=5)
        print(peaks)
        return peaks
    
    def find_local_minima(self, data):
        _threshold = 1.5
        troughs, properties = find_peaks(-data, height=_threshold)
        print(troughs)
        return troughs
            
    def draw_local_minima(self, data):
        minima = self.find_local_minima(data)
        plt.figure(figsize=(20, 10))
        plt.plot(self.time, data, label='Data')
        plt.scatter(self.time[minima], data[minima], color='red', label='Local Minima')
        for i, min_idx in enumerate(minima):
            plt.annotate(f't={self.time[min_idx]:.3f}', 
                        (self.time[min_idx], data[min_idx]), 
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
            plt.annotate(f'i={min_idx}', 
                        (self.time[min_idx], data[min_idx]), 
                        xytext=(5, -5), textcoords='offset points', fontsize=8)
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title(f'{self.file_name} Local Minima(below -1.5)')
        plt.xticks(np.arange(0, self.time[len(self.time) - 1], step=0.25), rotation=90)
        plt.legend()
        plt.grid(True)
    
    def visualize_local_minima(self, data):
        self.draw_local_minima(data)
        plt.show()
        
    def save_graphs(self, folder, name):
        try:
            plt.savefig(f'./results/{folder}/{name}.png')
        except:
            os.mkdir(f'./results/{folder}')
            self.save_graphs(folder, name)
            
    def save_local_minima(self, data):
        self.draw_local_minima(data)
        name = self.file_name.split('.')[1].split('/')
        self.save_graphs('local_minima', f'{name[2]}_{name[3]}_local_minima')
    
    def visualize_acceleration_and_orientation(self):
        plt.figure(figsize=(20, 5))
        plt.subplot(1, 2, 1)
        plt.plot(self.time, self.acceleration_x, label='Acceleration X')
        plt.plot(self.time, self.acceleration_y, label='Acceleration Y')
        plt.plot(self.time, self.acceleration_z, label='Acceleration Z')
        plt.xlabel('Time')
        plt.ylabel('Acceleration')
        plt.title('Acceleration Data')
        plt.legend()
        plt.grid(True)
        plt.subplot(1, 2, 2)
        plt.plot(self.time, self.orientation_x, label='Orientation X')
        plt.plot(self.time, self.orientation_y, label='Orientation Y')
        plt.plot(self.time, self.orientation_z, label='Orientation Z')
        plt.xlabel('Time')
        plt.ylabel('Orientation')
        plt.title('Orientation Data')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
    def visualize_acceleration_with_orientation(self):
        plt.figure(figsize=(20, 10))
        plt.subplot(3, 1, 1)
        plt.plot(self.time, self.acceleration_x, label='Acceleration X')
        plt.plot(self.time, self.orientation_x, label='Orientation X')
        plt.xlabel('Time')
        plt.ylabel('Acceleration / Orientation')
        plt.title('Acceleration X and Orientation X')
        plt.legend()
        plt.grid(True)
        plt.subplot(3, 1, 2)
        plt.plot(self.time, self.acceleration_y, label='Acceleration Y')
        plt.plot(self.time, self.orientation_y, label='Orientation Y')
        plt.xlabel('Time')
        plt.ylabel('Acceleration / Orientation')
        plt.title('Acceleration Y and Orientation Y')
        plt.legend()
        plt.grid(True)
        plt.subplot(3, 1, 3)
        plt.plot(self.time, self.acceleration_z, label='Acceleration Z')
        plt.plot(self.time, self.orientation_z, label='Orientation Z')
        plt.xlabel('Time')
        plt.ylabel('Acceleration / Orientation')
        plt.title('Acceleration Z and Orientation Z')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
    def visualize_acceleration(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.time, self.acceleration_x, label='Acceleration X')
        plt.plot(self.time, self.acceleration_y, label='Acceleration Y')
        plt.plot(self.time, self.acceleration_z, label='Acceleration Z')
        plt.xlabel('Time')
        plt.ylabel('Acceleration')
        plt.title('Acceleration Data')
        plt.legend()
        plt.grid(True)
        plt.xticks(np.arange(0, self.time[len(self.time) - 1], step=0.25), rotation=90)
        plt.show()
        
    def visualize_orientation(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.time, self.orientation_x, label='Orientation X')
        plt.plot(self.time, self.orientation_y, label='Orientation Y')
        plt.plot(self.time, self.orientation_z, label='Orientation Z')
        plt.xlabel('Time')
        plt.ylabel('Orientation')
        plt.title('Orientation Data')
        plt.legend()
        plt.grid(True)
        plt.xticks(np.arange(0, self.time[len(self.time) - 1], step=0.25), rotation=90)
        plt.show()