import pandas as pd
import numpy as np
import os

def calculate_gravity(orientation_x, orientation_z):
    orientation_x = np.arcsin(orientation_x)
    orientation_z = np.arcsin(orientation_z)
    return np.array([- np.sin(orientation_z), - np.cos(orientation_x) * np.cos(orientation_z), np.sin(orientation_x) * np.cos(orientation_z)])
    

if not os.path.exists("./processed_data"):
    os.makedirs("./processed_data")
            
datas = []

for i in range(1, 20):
    try:
        file_name = f"./datas/{i}.csv"
        data = pd.read_csv(file_name)
        datas.append(data)
        print(f"Data from {file_name} loaded successfully.")
    except FileNotFoundError:
        print(f"File {file_name} not found. Skipping.")
    except pd.errors.EmptyDataError:
        print(f"File {file_name} is empty. Skipping.")
    except Exception as e:
        print(f"An error occurred while processing {file_name}: {e}")

if len(datas) == 0:
    print("No data files were loaded. Exiting.")
    exit()
    

for i, data in enumerate(datas):
    try:
        _gravity_x = []
        _gravity_y = []
        _gravity_z = []
        
        for j in range(len(data)):
            orientation_x = np.arcsin(data['ori x'][j])
            orientation_z = np.arcsin(data['ori z'][j])
            _gravity_x.append(- np.sin(orientation_z))
            _gravity_y.append(- np.cos(orientation_x) * np.cos(orientation_z))
            _gravity_z.append(np.sin(orientation_x) * np.cos(orientation_z))

        gravity_x = pd.Series(_gravity_x, index=data['index'])
        gravity_y = pd.Series(_gravity_y, index=data['index'])
        gravity_z = pd.Series(_gravity_z, index=data['index'])

        data['raw acc x'] = data['acc x']
        data['raw acc y'] = data['acc y']
        data['raw acc z'] = data['acc z']
        
        data['acc x'] -= gravity_x
        data['acc y'] -= gravity_y
        data['acc z'] -= gravity_z
        
        output_file_name = f"./processed_data/{i+1}.csv"
        data.to_csv(output_file_name, index=False)
        print(f"Processed data saved to {output_file_name}.")
    except KeyError as e:
        print(f"Missing expected column in file {i+1}: {e}")
    except Exception as e:
        print(f"An error occurred while processing file {i+1}: {e}")


        