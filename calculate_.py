from functions_ import *
import argparse, os
from argparse import ArgumentParser
import joblib  # you may use native pickle here as well
import pandas as pd
import numpy as np
import more_itertools
import json

b_index =    ["pelvis_x","pelvis_y","pelvis_z","spine_naval_x","spine_naval_y","spine_naval_z","spine_chest_x","spine_chest_y","spine_chest_z","neck_x","neck_y","neck_z","clavicle_l_x",
              "clavicle_l_y","clavicle_l_z","shoulder_l_x","shoulder_l_y","shoulder_l_z","elbow_l_x","elbow_l_y","elbow_l_z","wrist_l_x","wrist_l_y","wrist_l_z", "hand_l_x","hand_l_y",
              "hand_l_z", "handtip_l_x","handtip_l_y","handtip_l_z","thumb_l_x","thumb_l_y","thumb_l_z", "clavicle_r_x","clavicle_r_y","clavicle_r_z","shoulder_r_x","shoulder_r_y","shoulder_r_z",
              "elbow_r_x","elbow_r_y","elbow_r_z", "wrist_r_x","wrist_r_y","wrist_r_z", "hand_r_x","hand_r_y","hand_r_z", "handtip_r_x","handtip_r_y","handtip_r_z","thumb_r_x","thumb_r_y","thumb_r_z",
              "hip_l_x","hip_l_y","hip_l_z", "knee_l_x","knee_l_y","knee_l_z", "ankle_l_x","ankle_l_y","ankle_l_z","foot_l_x","foot_l_y","foot_l_z", "hip_r_x","hip_r_y","hip_r_z","knee_r_x","knee_r_y","knee_r_z",
              "ankle_r_x","ankle_r_y","ankle_r_z", "foot_r_x","foot_r_y","foot_r_z", "head_x","head_y","head_z", "nose_x","nose_y","nose_z", "eye_l_x","eye_l_y","eye_l_z", "ear_l_x","ear_l_y","ear_l_z",
              "eye_r_x","eye_r_y","eye_r_z","ear_r_x","ear_r_y","ear_r_z"]

rename_dict_OP = {6: 'shoulder_r_x', 7: 'shoulder_r_y', 8: 'shoulder_r_z',
                  9: 'elbow_r_x', 10: 'elbow_r_y', 11: 'elbow_r_z',
                  12: 'wrist_r_x', 13: 'wrist_r_y', 14: 'wrist_r_z',
                  15: 'shoulder_l_x', 16: 'shoulder_l_y', 17: 'shoulder_l_z',
                  18: 'elbow_l_x', 19: 'elbow_l_y', 20: 'elbow_l_z',
                  21: 'wrist_l_x', 22: 'wrist_l_y', 23: 'wrist_l_z',
                  24: 'pelvis_x', 25: 'pelvis_y', 26: 'pelvis_z',
                  27: 'hip_r_x',28: 'hip_r_y',29: 'hip_r_z',
                  30: 'knee_r_x',31: 'knee_r_y',32: 'knee_r_z',
                  33: 'ankle_r_x',34: 'ankle_r_y',35: 'ankle_r_z',
                  36: 'hip_l_x', 37: 'hip_l_y', 38: 'hip_l_z',
                  39: 'knee_l_x',40: 'knee_l_y',41: 'knee_l_z',
                  42: 'ankle_l_x',43: 'ankle_l_y',44: 'ankle_l_z',
                  }

def joints_from_smpl(input):
	data = input
	joints = data[1]['joints3d']
	lists = {}
	for i in range(len(joints)):
		lists[i] = list(more_itertools.collapse(joints[i]))
	df = pd.DataFrame(lists)
	df.reset_index(drop=True, inplace=True)
	df_transposed = df.T
	df_transposed.rename(columns=rename_dict_OP, inplace=True)
	return df_transposed

def json_to_biomechanics(data):
	bone_list = []
	positions = []
	orientations = []
	bodies = []
	bone_list.append(data['bone_list'])
	for i in data['frames']:
		bodies.append(i['bodies'])
	for i in range(len(bodies)):
		orientations.append(bodies[i][0]['joint_orientations'])
		positions.append(np.array(bodies[i][0]['joint_positions']).flatten())
	df_pos = pd.DataFrame(positions)
	df_pos.columns = b_index
	return df_pos


def validate_file(f):
	if not os.path.exists(f):
		# Argparse uses the ArgumentTypeError to give a rejection message like:
		# error: argument input: x does not exist
		raise argparse.ArgumentTypeError("{0} does not exist".format(f))
	return f


if __name__ == "__main__":

	parser = ArgumentParser(description="Read file form Command line.")
	parser.add_argument("-i", "--input", dest="filename", required=True, type=validate_file,
	                    help="input file", metavar="FILE")
	args = parser.parse_args()
	file_input = args.filename
	if file_input.endswith(".json"):
		with open(file_input) as file: #json needs to open the file first
			data = json.load(file)
			df_pos = json_to_biomechanics(data)
			df_pos.to_csv("dataframe.csv")
			biomechanics = create_dataset(df_pos) #calculate biomechanics from joint positions
			biomechanics.to_csv((str(args.filename) + ".csv"), index=False)
			print("done")

	elif file_input.endswith(".pkl"): #logic for pkl file (from SMPL)
		biomechanics = create_dataset_SMPL(joints_from_smpl(joblib.load(file_input))) #calculate biomechanics from joint positions
		biomechanics.to_csv((str(args.filename) + ".csv"), index=False)
		print("done")

