import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PunchML:
    PUNCH_TYPES = {
        "None": 0,
        "Straight": 1,
        "Hook": 2,
        "Body": 3,
        "Uppercut": 4,
    }
    
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = pd.read_csv(file_name)
        
        try:
            self.index = self.data['index'].copy()
            self.time = self.data['time'].copy()
            self.acceleration_x = self.data['acc x'].copy()
            self.acceleration_y = self.data['acc y'].copy()
            self.acceleration_z = self.data['acc z'].copy()
            self.orientation_x = self.data['ori x'].copy()
            self.orientation_z = self.data['ori z'].copy()
            self.punch = self.data['punch'].copy()
            
        except:
            print("Error: Missing column in the CSV file.")
            exit()
    
        self.preprocess_data()
            
    def preprocess_data(self):
        self.punch_enum = self.punch.map(self.PUNCH_TYPES).fillna(0).astype(int)
        self.straight = self.data[self.punch_enum == self.PUNCH_TYPES["Straight"]]
        self.hook = self.data[self.punch_enum == self.PUNCH_TYPES["Hook"]]
        self.body = self.data[self.punch_enum == self.PUNCH_TYPES["Body"]]
        self.uppercut = self.data[self.punch_enum == self.PUNCH_TYPES["Uppercut"]]
        self.none = self.data[self.punch_enum == self.PUNCH_TYPES["None"]]
        
    def import_all_data(self):
        self.datas = []
        for i in range(1, 20):
            try:
                file_name = f"./datas/{i}.csv"
                self.datas.append(pd.read_csv(file_name))
            except:
                pass
            
            
    # def compile_gru(self):
        
    #     self.model = Sequential()
    #     self.model.add(GRU(64, input_shape=(None, 3), return_sequences=True))
    #     self.model.add(Dropout(0.2))
    #     self.model.add(GRU(32))
    #     self.model.add(Dense(1, activation='sigmoid'))
        
    #     self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
            
    def visualize_data(self):
        fig, axs = plt.subplots(5, 1, figsize=(15, 22.7))
        axs[0].plot(self.time, self.acceleration_x, label='Acceleration X')
        axs[0].set_title('Acceleration X')
        axs[0].set_xlabel('Time')
        axs[0].set_ylabel('Acceleration (m/s²)')
        axs[0].scatter(self.straight['time'], self.straight['acc x'], color='red', label='Straight Punch')
        axs[0].scatter(self.hook['time'], self.hook['acc x'], color='green', label='Hook Punch')
        axs[0].scatter(self.body['time'], self.body['acc x'], color='blue', label='Body Punch')
        axs[0].scatter(self.uppercut['time'], self.uppercut['acc x'], color='orange', label='Uppercut Punch')
        axs[0].legend()
        axs[0].grid(True)
        axs[1].plot(self.time, self.acceleration_y, label='Acceleration Y')
        axs[1].set_title('Acceleration Y')
        axs[1].set_xlabel('Time')
        axs[1].set_ylabel('Acceleration (m/s²)')
        axs[1].scatter(self.straight['time'], self.straight['acc y'], color='red', label='Straight Punch')
        axs[1].scatter(self.hook['time'], self.hook['acc y'], color='green', label='Hook Punch')
        axs[1].scatter(self.body['time'], self.body['acc y'], color='blue', label='Body Punch')
        axs[1].scatter(self.uppercut['time'], self.uppercut['acc y'], color='orange', label='Uppercut Punch')
        axs[1].legend()
        axs[1].grid(True)
        axs[2].plot(self.time, self.acceleration_z, label='Acceleration Z')
        axs[2].set_title('Acceleration Z')
        axs[2].set_xlabel('Time')
        axs[2].set_ylabel('Acceleration (m/s²)')
        axs[2].scatter(self.straight['time'], self.straight['acc z'], color='red', label='Straight Punch')
        axs[2].scatter(self.hook['time'], self.hook['acc z'], color='green', label='Hook Punch')
        axs[2].scatter(self.body['time'], self.body['acc z'], color='blue', label='Body Punch')
        axs[2].scatter(self.uppercut['time'], self.uppercut['acc z'], color='orange', label='Uppercut Punch')
        axs[2].legend()
        axs[2].grid(True)
        axs[3].plot(self.time, self.orientation_x, label='Orientation X')
        axs[3].set_title('Orientation X')
        axs[3].set_xlabel('Time')
        axs[3].set_ylabel('Orientation (rad)')
        axs[3].scatter(self.straight['time'], self.straight['ori x'], color='red', label='Straight Punch')
        axs[3].scatter(self.hook['time'], self.hook['ori x'], color='green', label='Hook Punch')
        axs[3].scatter(self.body['time'], self.body['ori x'], color='blue', label='Body Punch')
        axs[3].scatter(self.uppercut['time'], self.uppercut['ori x'], color='orange', label='Uppercut Punch')
        axs[3].legend()
        axs[3].grid(True)
        axs[4].plot(self.time, self.orientation_z, label='Orientation Z')
        axs[4].set_title('Orientation Z')
        axs[4].set_xlabel('Time')
        axs[4].set_ylabel('Orientation (rad)')
        axs[4].scatter(self.straight['time'], self.straight['ori z'], color='red', label='Straight Punch')
        axs[4].scatter(self.hook['time'], self.hook['ori z'], color='green', label='Hook Punch')
        axs[4].scatter(self.body['time'], self.body['ori z'], color='blue', label='Body Punch')
        axs[4].scatter(self.uppercut['time'], self.uppercut['ori z'], color='orange', label='Uppercut Punch')
        axs[4].legend()
        axs[4].grid(True)
        plt.tight_layout()
        plt.show()