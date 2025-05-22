import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler

def numerical_integration(list, index):
    result = [0.0]
    for i in range(1, len(list)):
        result.append((list[i]+list[i-1])*(index[i]-index[i-1]) / 2 + result[i-1])
        # result.append((list[i]+list[i-1])*(50) / 2 + result[i-1])
    return result

def visulize_integrals():
    plt.figure(figsize=(16, 12))
    plt.subplot(4, 2, 1)
    plt.plot(time, acceleration_x, label='Acceleration X', color='red')
    plt.plot(time, acceleration_y, label='Acceleration Y', color='green')
    plt.plot(time, acceleration_z, label='Acceleration Z', color='blue')
    plt.title('Acceleration vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s²)')
    plt.legend()
    plt.grid()
    plt.subplot(4, 2, 3)
    plt.plot(time, velocity_x, label='Velocity X', color='red')
    plt.plot(time, velocity_y, label='Velocity Y', color='green')
    plt.plot(time, velocity_z, label='Velocity Z', color='blue')
    plt.title('Velocity vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.legend()
    plt.grid()
    plt.subplot(4, 2, 5)
    plt.plot(time, position_x, label='Position X', color='red')
    plt.plot(time, position_y, label='Position Y', color='green')
    plt.plot(time, position_z, label='Position Z', color='blue')
    plt.title('Position vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Position (m)')
    plt.legend()
    plt.grid()
    
    plt.subplot(4, 2, 2)
    plt.plot(diff_time, diff_acceleration_x, label='Acceleration X', color='red')
    plt.plot(diff_time, diff_acceleration_y, label='Acceleration Y', color='green')
    plt.plot(diff_time, diff_acceleration_z, label='Acceleration Z', color='blue')
    plt.title('Diff Acceleration vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s²)')
    plt.legend()
    plt.grid()
    plt.subplot(4, 2, 4)
    plt.plot(diff_time, diff_velocity_x, label='Velocity X', color='red')
    plt.plot(diff_time, diff_velocity_y, label='Velocity Y', color='green')
    plt.plot(diff_time, diff_velocity_z, label='Velocity Z', color='blue')
    plt.title('Diff Velocity vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.legend()
    plt.grid()
    plt.subplot(4, 2, 6)
    plt.plot(diff_time, diff_position_x, label='Position X', color='red')
    plt.plot(diff_time, diff_position_y, label='Position Y', color='green')
    plt.plot(diff_time, diff_position_z, label='Position Z', color='blue')
    plt.title('Diff Position vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Position (m)')
    plt.legend()
    plt.grid()
    
    plt.subplot(4, 2, 7)
    plt.plot(time, gyro_x, label='Gyro X', color='red')
    plt.plot(time, gyro_y, label='Gyro Y', color='green')
    plt.plot(time, gyro_z, label='Gyro Z', color='blue')
    plt.title('Gyro vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Gyro (rad/s)')
    plt.legend()
    plt.grid()
    plt.subplot(4, 2, 8)
    plt.plot(time, angle_x, label='Angle X', color='red')
    plt.plot(time, angle_y, label='Angle Y', color='green')
    plt.plot(time, angle_z, label='Angle Z', color='blue')
    plt.title('Angle vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Angle (rad)')
    plt.legend()
    plt.grid()
    
    plt.tight_layout()
    plt.show()
    
def visulize_3d_path():
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(position_x, position_y, position_z, label='3D Path', color='blue')
    ax.plot(scale_data(diff_position_x), scale_data(diff_position_y), scale_data(diff_position_z), label='Diff Path', color='red')
    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Y Position (m)')
    ax.set_zlabel('Z Position (m)')
    ax.set_title('3D Path of the Object')
    plt.legend()
    plt.show()
    
def scale_data(data):
    scale = 100
    return np.array([i * scale for i in data])

data = pd.read_csv('./datas/stable.csv')

# integral by raw data
time = data['time']

gyro_x = data['roll']
gyro_y = data['pitch']
gyro_z = data['yaw']

angle_x = numerical_integration(gyro_x, time)
angle_y = numerical_integration(gyro_y, time)
angle_z = numerical_integration(gyro_z, time)

acceleration_x = data['x']
acceleration_y = data['y']
acceleration_z = data['z']

velocity_x = numerical_integration(acceleration_x, time)
velocity_y = numerical_integration(acceleration_y, time)
velocity_z = numerical_integration(acceleration_z, time)

position_x = numerical_integration(velocity_x, time)
position_y = numerical_integration(velocity_y, time)
position_z = numerical_integration(velocity_z, time)


diff_time = time
# integral by diff data
# diff_time = time[:-1]
# diff_acceleration_x = [acceleration_x[i] - acceleration_x[i-1] for i in range(1, len(acceleration_x))]
# diff_acceleration_y = [acceleration_y[i] - acceleration_y[i-1] for i in range(1, len(acceleration_y))]
# diff_acceleration_z = [acceleration_z[i] - acceleration_z[i-1] for i in range(1, len(acceleration_z))]

diff_acceleration_x = [acceleration_x[i] - acceleration_x[0] for i in range(len(acceleration_x))]
diff_acceleration_y = [acceleration_y[i] - acceleration_y[0] for i in range(len(acceleration_y))]
diff_acceleration_z = [acceleration_z[i] - acceleration_z[0] for i in range(len(acceleration_z))]

diff_velocity_x = numerical_integration(diff_acceleration_x, diff_time)
diff_velocity_y = numerical_integration(diff_acceleration_y, diff_time)
diff_velocity_z = numerical_integration(diff_acceleration_z, diff_time)

diff_position_x = numerical_integration(diff_velocity_x, diff_time)
diff_position_y = numerical_integration(diff_velocity_y, diff_time)
diff_position_z = numerical_integration(diff_velocity_z, diff_time)

def correct_acceleration_error(data):
    error_threshold = 0.1
    corrected_data = []
    
    for i in range(len(data)):
        if abs(data[i]) < error_threshold:
            corrected_data.append(0.0)
        else:
            corrected_data.append(data[i])
            
    
    
    # for i in range(1, len(data)):
    #     if abs(data[i] - data[i-1]) > error_threshold:
    #         corrected_data.append(data[i])
    #     else:
    #         corrected_data.append(corrected_data[i-1])
    return corrected_data


# def correct_velocity_error(data):
#     error_threshold = 0.07
#     corrected_data = []
    
#     for i in range(len(data)):
#         if abs(data[i]) < error_threshold:
#             corrected_data.append(0.0)
#         else:
#             corrected_data.append(data[i])
            
#     return corrected_data

# corrected_acceleration_x = correct_acceleration_error(acceleration_x)
# corrected_acceleration_y = correct_acceleration_error(acceleration_y)
# corrected_acceleration_z = correct_acceleration_error(acceleration_z)

# corrected_diff_acceleration_x = correct_acceleration_error(diff_acceleration_x)
# corrected_diff_acceleration_y = correct_acceleration_error(diff_acceleration_y)
# corrected_diff_acceleration_z = correct_acceleration_error(diff_acceleration_z)


# diff_acceleration_x = corrected_diff_acceleration_x
# diff_acceleration_y = corrected_diff_acceleration_y
# diff_acceleration_z = corrected_diff_acceleration_z

# plt.figure(figsize=(16, 12))
# plt.plot([i for i in range(len(diff_acceleration_x))], diff_acceleration_x, label='Diff Acceleration X', color='red')
# plt.plot([i for i in range(len(corrected_diff_acceleration_x))], corrected_diff_acceleration_x, label='Diff Acceleration X', color='green')
# plt.plot([i for i in range(len(acceleration_x))], acceleration_x, label='Acceleration X', color='blue')
# plt.show()


# diff_velocity_x = numerical_integration(corrected_diff_acceleration_x, diff_time)
# diff_velocity_y = numerical_integration(corrected_diff_acceleration_y, diff_time)
# diff_velocity_z = numerical_integration(corrected_diff_acceleration_z, diff_time)


# corrected_diff_velocity_x = correct_velocity_error(diff_velocity_x)
# corrected_diff_velocity_y = correct_velocity_error(diff_velocity_y)
# corrected_diff_velocity_z = correct_velocity_error(diff_velocity_z)


# diff_position_x = numerical_integration(corrected_diff_velocity_x, diff_time)
# diff_position_y = numerical_integration(corrected_diff_velocity_y, diff_time)
# diff_position_z = numerical_integration(corrected_diff_velocity_z, diff_time)


visulize_integrals()
# visulize_3d_path()