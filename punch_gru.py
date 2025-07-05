import pandas as pd
# from keras.models import Sequential
# from keras.layers import GRU, Dense, Dropout

class PunchGRU:
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
            
            self.user_input = self.data['user input'].copy()
            
        except KeyError as e:
            print("Error: Missing column in the CSV file.")
            exit()
            
        self.X = [self.acceleration_x, self.acceleration_y, self.acceleration_z]
        self.y = self.user_input
        
    def compile_model(self):
        self.model = Sequential()
        self.model.add(GRU(64, input_shape=(None, 3), return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(GRU(32))
        self.model.add(Dense(1, activation='sigmoid'))
        
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        
    # def train_model(self):
    #     model = Sequential()
    #     model.add(GRU(64, input_shape=(None, 3), return_sequences=True))
    #     model.add(Dropout(0.2))
    #     model.add(GRU(32))
    #     model.add(Dense(1, activation='sigmoid'))
        
    #     model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    #     model.summary()
        
    #     # Reshape data for GRU
    #     X_reshaped = pd.concat(self.X, axis=1).values.reshape(-1, len(self.X), 1)
    #     y_reshaped = self.y.values.reshape(-1, 1)
        
    #     model.fit(X_reshaped, y_reshaped, epochs=10, batch_size=32)
        
    #     return model