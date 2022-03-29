import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('master.csv')
headers = list(data)
"""
datalists = dict()
for item in headers:
	datalists[item] = []

print(datalists)
list = []
for x in range(97):
	list.append(x)

for i in datalists:
	for j in list:
		datalists[i].append(j)
print(datalists)
"""
def get_csv(name):
	data = pd.read_csv(name)
	return data

def get_left_knee(frame): #calcualtes the knee angle using trig, for the left or right knee at time t
	joint1 = [data.iloc[frame]['hip_r_x'], data.iloc[frame]['hip_r_y'], data.iloc[frame]['hip_r_z']]
	joint2 = [data.iloc[frame]['knee_r_x'], data.iloc[frame]['knee_r_y'], data.iloc[frame]['knee_r_z']]
	joint3 = [data.iloc[frame]['ankle_r_x'], data.iloc[frame]['ankle_r_y'], data.iloc[frame]['ankle_r_z']]
	HA = math.dist(joint1, joint3) #distance between hip and ankle
	HK = math.dist(joint1, joint2) #distance between hip and knee
	KA = math.dist(joint2, joint3) #distance between knee and ankle
	knee_angle_left = (math.degrees(math.acos((HK**2 + KA**2 - HA**2)/(2.0 * HK * KA)))) #use cosine rule
	return knee_angle_left

def get_right_knee(frame):
	joint1 = [data.iloc[frame]['hip_l_x'], data.iloc[frame]['hip_l_y'], data.iloc[frame]['hip_l_z']]
	joint2 = [data.iloc[frame]['knee_l_x'], data.iloc[frame]['knee_l_y'], data.iloc[frame]['knee_l_z']]
	joint3 = [data.iloc[frame]['ankle_l_x'], data.iloc[frame]['ankle_l_y'], data.iloc[frame]['ankle_l_z']]
	HA = math.dist(joint1, joint3)  # distance between hip and ankle
	HK = math.dist(joint1, joint2)  # distance between hip and knee
	KA = math.dist(joint2, joint3)  # distance between knee and ankle
	knee_angle_right = (math.degrees(math.acos((HK ** 2 + KA ** 2 - HA ** 2) / (2.0 * HK * KA))))  # use cosine rule
	return knee_angle_right

def get_middle_ground(frame):
	x1 = (data.iloc[frame] ['ankle_l_x'])
	x2 = (data.iloc[frame] ['ankle_l_x'])
	x_avg = (x1+x2)/2
	y = data.iloc[frame] ['pelvis_y']
	z = data.iloc[frame] ['pelvis_z']
	mid_pos = (x_avg,y,z)
	return mid_pos

def get_left_hip(frame):
	joint1 = [data.iloc[frame]['pelvis_x'],data.iloc[frame]['pelvis_y'],data.iloc[frame]['pelvis_z']]
	joint2 = [data.iloc[frame]['ankle_l_x'],data.iloc[frame]['ankle_l_y'],data.iloc[frame]['ankle_l_z']]
	joint3 = get_middle_ground(frame)
	PA = math.dist(joint1,joint2)
	PF = math.dist(joint1,joint3)
	AF = math.dist(joint2,joint3)
	hip_angle_left = (math.degrees(math.acos((PA ** 2 + AF ** 2 - PF ** 2) / (2.0 * PA * AF))))
	return hip_angle_left

def get_right_hip(frame):
	joint1 = [data.iloc[frame]['pelvis_x'],data.iloc[frame]['pelvis_y'],data.iloc[frame]['pelvis_z']]
	joint2 = [data.iloc[frame]['ankle_r_x'],data.iloc[frame]['ankle_r_y'],data.iloc[frame]['ankle_r_z']]
	joint3 = get_middle_ground(frame)
	PA = math.dist(joint1,joint2)
	PF = math.dist(joint1,joint3)
	AF = math.dist(joint2,joint3)
	hip_angle_right = (math.degrees(math.acos((PA ** 2 + AF ** 2 - PF ** 2) / (2.0 * PA * AF))))
	return hip_angle_right

def get_velocity(frame1, frame2, joint): #calcualtes the average velocity between two time points from a dataframe
	joint_x = ''.join((joint, '_x'))
	joint_y = ''.join((joint, '_y'))
	joint_z = ''.join((joint, '_z'))
	joint_t1 = (data.iloc[frame1] [joint_x],data.iloc[frame1] [joint_y],data.iloc[frame1] [joint_z])
	joint_t2 = (data.iloc[frame2] [joint_x],data.iloc[frame2] [joint_y],data.iloc[frame2] [joint_z])
	d_dist = math.dist(joint_t2, joint_t1) #change in distance
	d_time = frame2 - frame1 #change in time
	velocity = d_dist/d_time #change in distance over change in time
	return velocity

def get_acceleration(frame1, frame2, joint):
	velocity1 = get_velocity(frame1, frame1+1, joint) #velocity of joint x at time pair t+1 and t+2
	velocity2 = get_velocity(frame2+1, frame2+2, joint) #velocity of joint x at time pair t and t+1
	d_time = frame2+2 - frame1
	acceleration = (velocity2-velocity1) / (d_time) #change in velocity over change in time
	return acceleration

body_index =    ["pelvis", "spine_naval", "spine_chest", "neck", "clavicle_l", "shoulder_l", "elbow_l", "wrist_l", "hand_l", "handtip_l",
                "thumb_l", "clavicle_r", "shoulder_r", "elbow_r", "wrist_r", "hand_r", "handtip_r", "thumb_r", "hip_l", "knee_l", "ankle_l",
                "foot_l", "hip_r", "knee_r", "ankle_r", "foot_r", "head", "nose", "eye_l", "ear_l", "eye_r", "ear_r"]

hip_left = [] #create empty list to store knee angles
hip_right = []
for i in range(len(data)): #for each time point in the dataframe
	hip_left.append(get_left_hip(i)) #for each joint in the dataframe
for i in range(len(data)):
	hip_right.append(get_right_hip(i))
print(hip_left)
print(hip_right)
"""
vel_list = dict()
for item in body_index:
	vel_list[item] = []
for i in range(len(data)-1): #for each time in the dataframe until the last (time pairs)
	for item in vel_list: #for each joint in the dataframe
		vel_list[item].append(get_velocity(i, i+1, item)) #velocity of each joint at between each time pairs
df1 = pd.DataFrame.from_dict(vel_list)
print(df1)
df1.to_csv('velocities.csv', index=False,)

acc_list = dict()
for item in body_index:
	acc_list[item] = []
for i in range(len(data)-2):
	for item in acc_list:
		acc_list[item].append(get_acceleration(i,i,item))
df2 = pd.DataFrame.from_dict(acc_list)
print(df2)
df2.to_csv('accelerations.csv', index=False)
"""