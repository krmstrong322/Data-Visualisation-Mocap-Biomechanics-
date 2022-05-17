from functions_ import *
import argparse
import joblib  # you may use native pickle here as well
import pandas as pd
import numpy as np
import more_itertools
from statistics import mean

b_index = ["pelvis_x", "pelvis_y", "pelvis_z", "spine_naval_x", "spine_naval_y", "spine_naval_z", "spine_chest_x",
           "spine_chest_y", "spine_chest_z", "neck_x", "neck_y", "neck_z", "clavicle_l_x",
           "clavicle_l_y", "clavicle_l_z", "shoulder_l_x", "shoulder_l_y", "shoulder_l_z", "elbow_l_x", "elbow_l_y",
           "elbow_l_z", "wrist_l_x", "wrist_l_y", "wrist_l_z", "hand_l_x", "hand_l_y",
           "hand_l_z", "handtip_l_x", "handtip_l_y", "handtip_l_z", "thumb_l_x", "thumb_l_y", "thumb_l_z",
           "clavicle_r_x", "clavicle_r_y", "clavicle_r_z", "shoulder_r_x", "shoulder_r_y", "shoulder_r_z",
           "elbow_r_x", "elbow_r_y", "elbow_r_z", "wrist_r_x", "wrist_r_y", "wrist_r_z", "hand_r_x", "hand_r_y",
           "hand_r_z", "handtip_r_x", "handtip_r_y", "handtip_r_z", "thumb_r_x", "thumb_r_y", "thumb_r_z",
           "hip_l_x", "hip_l_y", "hip_l_z", "knee_l_x", "knee_l_y", "knee_l_z", "ankle_l_x", "ankle_l_y", "ankle_l_z",
           "foot_l_x", "foot_l_y", "foot_l_z", "hip_r_x", "hip_r_y", "hip_r_z", "knee_r_x", "knee_r_y", "knee_r_z",
           "ankle_r_x", "ankle_r_y", "ankle_r_z", "foot_r_x", "foot_r_y", "foot_r_z", "head_x", "head_y", "head_z",
           "nose_x", "nose_y", "nose_z", "eye_l_x", "eye_l_y", "eye_l_z", "ear_l_x", "ear_l_y", "ear_l_z",
           "eye_r_x", "eye_r_y", "eye_r_z", "ear_r_x", "ear_r_y", "ear_r_z"]

rename_dict_OP = {6: 'shoulder_r_x', 7: 'shoulder_r_y', 8: 'shoulder_r_z',
                  9: 'elbow_r_x', 10: 'elbow_r_y', 11: 'elbow_r_z',
                  12: 'wrist_r_x', 13: 'wrist_r_y', 14: 'wrist_r_z',
                  15: 'shoulder_l_x', 16: 'shoulder_l_y', 17: 'shoulder_l_z',
                  18: 'elbow_l_x', 19: 'elbow_l_y', 20: 'elbow_l_z',
                  21: 'wrist_l_x', 22: 'wrist_l_y', 23: 'wrist_l_z',
                  24: 'pelvis_x', 25: 'pelvis_y', 26: 'pelvis_z',
                  27: 'hip_r_x', 28: 'hip_r_y', 29: 'hip_r_z',
                  30: 'knee_r_x', 31: 'knee_r_y', 32: 'knee_r_z',
                  33: 'ankle_r_x', 34: 'ankle_r_y', 35: 'ankle_r_z',
                  36: 'hip_l_x', 37: 'hip_l_y', 38: 'hip_l_z',
                  39: 'knee_l_x', 40: 'knee_l_y', 41: 'knee_l_z',
                  42: 'ankle_l_x', 43: 'ankle_l_y', 44: 'ankle_l_z'}


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


def get_mean_df(file1, file2, file3, file4=None, file5=None):

	mean_dict = {}
	min_dict = {}
	max_dict = {}

	df_1 = create_dataset_SMPL(joints_from_smpl(joblib.load(file_input_1)))
	df_1 = df_1.apply(lambda x: savgol_filter(x, 5, 1))
	df_2 = create_dataset_SMPL(joints_from_smpl(joblib.load(file_input_2)))
	df_2 = df_2.apply(lambda x: savgol_filter(x, 5, 1))
	df_3 = create_dataset_SMPL(joints_from_smpl(joblib.load(file_input_3)))
	df_3 = df_3.apply(lambda x: savgol_filter(x, 5, 1))
	if file4 is not None:
		df_4 = create_dataset_SMPL(joints_from_smpl(joblib.load(file_input_4)))
		df_4 = df_4.apply(lambda x: savgol_filter(x, 5, 1))
	if file5 is not None:
		df_5 = create_dataset_SMPL(joints_from_smpl(joblib.load(file_input_5)))
		df_5 = df_5.apply(lambda x: savgol_filter(x, 5, 1))

	column_names = df_1.columns.values.tolist()
	column_names_merged = []
	merged = {}
	for i in range(len(column_names)):
		column_names_merged.insert(i, str(column_names[i]) + "_merged")

	for j in column_names:
		# temp1 = df_1[j].to_list()
		# temp2 = df_2[j].to_list()
		# temp3 = df_3[j].to_list()
		dictionary_knee_flexion = {'a': list(df_1[j]), 'b': list(df_2[j]), 'c': list(list(df_3[j]))}
		# print(dictionary_knee_flexion)
		mean_tmp = {j + "_mean": [mean(values) for values in zip(*dictionary_knee_flexion.values())]}
		min_tmp = {j + "_min": [min(values) for values in zip(*dictionary_knee_flexion.values())]}
		max_tmp = {j + "_max": [max(values) for values in zip(*dictionary_knee_flexion.values())]}
		merged.update(mean_tmp)
		merged.update(min_tmp)
		merged.update(max_tmp)
	merged_df = pd.DataFrame(merged)
	merged_df = merged_df.apply(lambda x: savgol_filter(x, 5, 1))
	return merged_df

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Read file form Command line.")
	parser.add_argument("-i1", "--input1", dest="filename1", required=True, type=validate_file, help="input file",
	                    metavar="FILE")
	parser.add_argument("-i2", "--input2", dest="filename2", required=True, type=validate_file, help="input file",
	                    metavar="FILE")
	parser.add_argument("-i3", "--input3", dest="filename3", required=True, type=validate_file, help="input file",
	                    metavar="FILE")
	parser.add_argument("-i4", "--input4", dest="filename1", required=False, type=validate_file, help="input file",
	                    metavar="FILE")
	parser.add_argument("-i5", "--input5", dest="filename2", required=False, type=validate_file, help="input file",
	                    metavar="FILE")
	parser.add_argument("-o", "--output", dest="output", required=False, default="out.csv", help="output file name")
	args = parser.parse_args()
	file_input_1 = args.filename1
	biomechanics1 = create_dataset_SMPL(joints_from_smpl(joblib.load(file_input_1)))
	file_input_2 = args.filename2
	biomechanics2 = create_dataset_SMPL(joints_from_smpl(joblib.load(file_input_2)))
	file_input_3 = args.filename3
	biomechanics3 = create_dataset_SMPL(joints_from_smpl(joblib.load(file_input_3)))

	if args.filename4 is not None:
		file_input_4 = args.filename4
		biomechanics4 = create_dataset_SMPL(joints_from_smpl(joblib.load(file_input_1)))

	if args.filename5 is not None:
		file_input_5 = args.filename5
		biomechanics5 = create_dataset_SMPL(joints_from_smpl(joblib.load(file_input_1)))

	if args.filename5 is not None and args.filename4 is not None:
		file_input_5 = args.filename5
		file_input_4 = args.filename4
		get_mean_df(file_input_1, file_input_2, file_input_3, file_input_4, file_input_5).to_csv(args.output)

	elif args.filename5 is None and args.filename4 is None:
		get_mean_df(file_input_1, file_input_2, file_input_3).to_csv(args.output)

