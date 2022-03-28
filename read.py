import numpy as np
import os
import pandas as pd

directory = r'C:\Users\Kai Armstrong\Desktop\DTP-KNEE-main\271120-140147 (1)'

body_index =    ["pelvis", "spine_naval", "spine_chest", "neck", "clavicle_l", "shoulder_l", "elbow_l", "wrist_l", "hand_l", "handtip_l",
                "thumb_l", "clavicle_r", "shoulder_r", "elbow_r", "wrist_r", "hand_r", "handtip_r", "thumb_r", "hip_l", "knee_l", "ankle_l",
                "foot_l", "hip_r", "knee_r", "ankle_r", "foot_r", "head", "nose", "eye_l", "ear_l", "eye_r", "ear_r"]

b_index =    ["pelvis_x","pelvis_y","pelvis_z","spine_naval_x","spine_naval_y","spine_naval_z","spine_chest_x","spine_chest_y","spine_chest_z","neck_x","neck_y","neck_z","clavicle_l_x",
              "clavicle_l_y","clavicle_l_z","shoulder_l_x","shoulder_l_y","shoulder_l_z","elbow_l_x","elbow_l_y","elbow_l_z","wrist_l_x","wrist_l_y","wrist_l_z", "hand_l_x","hand_l_y",
              "hand_l_z", "handtip_l_x","handtip_l_y","handtip_l_z","thumb_l_x","thumb_l_y","thumb_l_z", "clavicle_r_x","clavicle_r_y","clavicle_r_z","shoulder_r_x","shoulder_r_y","shoulder_r_z",
              "elbow_r_x","elbow_r_y","elbow_r_z", "wrist_r_x","wrist_r_y","wrist_r_z", "hand_r_x","hand_r_y","hand_r_z", "handtip_r_x","handtip_r_y","handtip_r_z","thumb_r_x","thumb_r_y","thumb_r_z",
              "hip_l_x","hip_l_y","hip_l_z", "knee_l_x","knee_l_y","knee_l_z", "ankle_l_x","ankle_l_y","ankle_l_z","foot_l_x","foot_l_y","foot_l_z", "hip_r_x","hip_r_y","hip_r_z","knee_r_x","knee_r_y","knee_r_z",
              "ankle_r_x","ankle_r_y","ankle_r_z", "foot_r_x","foot_r_y","foot_r_z", "head_x","head_y","head_z", "nose_x","nose_y","nose_z", "eye_l_x","eye_l_y","eye_l_z", "ear_l_x","ear_l_y","ear_l_z",
              "eye_r_x","eye_r_y","eye_r_z","ear_r_x","ear_r_y","ear_r_z"]
"""
#split npy files consisting of frame 1 and frame 2, into two different csv files
for filename in os.listdir(directory): #for each file in specified directory
    if filename.endswith(".npy"): #for every file ending with .npy
        data = np.load(filename)
        split = filename.split("_")
        frame1 = data[0]
        frame2 = data[1]
        pd.DataFrame(frame1).T.to_csv('{0}.csv'.format(split[2]), index=False, header=False)
        pd.DataFrame(frame2).T.to_csv('{0}.csv'.format(split[3][:-4]), index=False, header=False)
"""
#restructure data for further use
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        input = pd.read_csv(filename, header=None, dtype="unicode", low_memory=False)
        #df = pd.DataFrame(input)
        input = input[input.index!=3] #remove the confidence level, leaving just xyz coordinates
        data_to_expand = []
        for cols in input: data_to_expand.append(input[cols].to_numpy().tolist())
        flattened = []
        for sublist in data_to_expand:
            for val in sublist:
                flattened.append(val)
        df_new = pd.DataFrame(flattened)
        transposed = df_new.T
        transposed.to_csv('restructured_{0}'.format(filename), index=False) #save restructured dataframe to csv

times = []
for filename in os.listdir(directory):
    if filename.endswith(".csv") and not filename.startswith("restructured"):
        times.append(filename[:-4])

dfs = [] #create empty list to store dataframes in
for filename in os.listdir(directory):
    if filename.startswith("restructured"): #only use restructured dataframes
        df = pd.read_csv(filename)
        dfs.append(df) #store restructured dataframes into one list

frame = pd.concat(dfs, axis=0, ignore_index=True) #concatenate list of dataframes into one dataframe
frame.insert(loc=0, column='Time', value=times) #add new column to use as the index
frame.set_index('Time', inplace=True, drop=True) #set newly added column as the inex
frame.columns = b_index
frame.to_csv('master.csv') #save final dataframe as master file of each joint and timeframe

print("Done") #just to know when finished
