import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('./datas/stable.csv')

ax = data['x']
ay = data['y']
az = data['z']

pitch = math.atan2(-ax, math.sqrt(ay*ay + az*az))
roll  = math.atan2(ay, az)

mx2 = mx * math.cos(pitch) + mz * math.sin(pitch)
my2 = mx * math.sin(roll) * math.sin(pitch) + my * math.cos(roll) - mz * math.sin(roll) * math.cos(pitch)

yaw = math.atan2(-my2, mx2)