import math
import numpy as np
from scipy.signal import savgol_filter
from scipy.spatial import distance
import pandas as pd
import more_itertools
import argparse
import os
import joblib


body_index = ["pelvis", "spine_naval", "spine_chest", "neck", "clavicle_l", "shoulder_l", "elbow_l", "wrist_l",
              "hand_l", "handtip_l",
              "thumb_l", "clavicle_r", "shoulder_r", "elbow_r", "wrist_r", "hand_r", "handtip_r", "thumb_r", "hip_l",
              "knee_l", "ankle_l",
              "foot_l", "hip_r", "knee_r", "ankle_r", "foot_r", "head", "nose", "eye_l", "ear_l", "eye_r", "ear_r"]

b_index =    ["pelvis_x","pelvis_y","pelvis_z","spine_naval_x","spine_naval_y","spine_naval_z","spine_chest_x","spine_chest_y","spine_chest_z","neck_x","neck_y","neck_z","clavicle_l_x",
              "clavicle_l_y","clavicle_l_z","shoulder_l_x","shoulder_l_y","shoulder_l_z","elbow_l_x","elbow_l_y","elbow_l_z","wrist_l_x","wrist_l_y","wrist_l_z", "hand_l_x","hand_l_y",
              "hand_l_z", "handtip_l_x","handtip_l_y","handtip_l_z","thumb_l_x","thumb_l_y","thumb_l_z", "clavicle_r_x","clavicle_r_y","clavicle_r_z","shoulder_r_x","shoulder_r_y","shoulder_r_z",
              "elbow_r_x","elbow_r_y","elbow_r_z", "wrist_r_x","wrist_r_y","wrist_r_z", "hand_r_x","hand_r_y","hand_r_z", "handtip_r_x","handtip_r_y","handtip_r_z","thumb_r_x","thumb_r_y","thumb_r_z",
              "hip_l_x","hip_l_y","hip_l_z", "knee_l_x","knee_l_y","knee_l_z", "ankle_l_x","ankle_l_y","ankle_l_z","foot_l_x","foot_l_y","foot_l_z", "hip_r_x","hip_r_y","hip_r_z","knee_r_x","knee_r_y","knee_r_z",
              "ankle_r_x","ankle_r_y","ankle_r_z", "foot_r_x","foot_r_y","foot_r_z", "head_x","head_y","head_z", "nose_x","nose_y","nose_z", "eye_l_x","eye_l_y","eye_l_z", "ear_l_x","ear_l_y","ear_l_z",
              "eye_r_x","eye_r_y","eye_r_z","ear_r_x","ear_r_y","ear_r_z"]
"""
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
"""
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

body_index_SMPL = list(range(146))


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
"""
def joints_from_smpl(input):
	data = input
	joints = data[1]['joints3d']
	lists = {}
	for i in range(len(joints)):
		lists[i] = list(more_itertools.collapse(joints[i]))
	df = pd.DataFrame(lists)
	df.reset_index(drop=True, inplace=True)
	df_transposed = df.T
	return df_transposed #output the transposed joints from SMPL in the desired file format
"""



def get_right_knee(frame, data):
	joint1 = [data.iloc[frame]['hip_l_x'], data.iloc[frame]['hip_l_y'], data.iloc[frame]['hip_l_z']]
	joint2 = [data.iloc[frame]['knee_l_x'], data.iloc[frame]['knee_l_y'], data.iloc[frame]['knee_l_z']]
	joint3 = [data.iloc[frame]['ankle_l_x'], data.iloc[frame]['ankle_l_y'], data.iloc[frame]['ankle_l_z']]
	HA = distance.euclidean(joint1, joint3)  # distance between hip and ankle
	HK = distance.euclidean(joint1, joint2)  # distance between hip and knee
	KA = distance.euclidean(joint2, joint3)  # distance between knee and ankle
	try:
		knee_angle_right = (math.degrees(math.acos((HK ** 2 + KA ** 2 - HA ** 2) / (2.0 * HK * KA))))  # use cosine rule
		return knee_angle_right
	except ValueError:
		return

def get_left_knee(frame, data):  # calcualtes the knee angle using trig, for the left or right knee at time t
	joint1 = [data.iloc[frame]['hip_r_x'], data.iloc[frame]['hip_r_y'], data.iloc[frame]['hip_r_z']]
	joint2 = [data.iloc[frame]['knee_r_x'], data.iloc[frame]['knee_r_y'], data.iloc[frame]['knee_r_z']]
	joint3 = [data.iloc[frame]['ankle_r_x'], data.iloc[frame]['ankle_r_y'], data.iloc[frame]['ankle_r_z']]
	HA = distance.euclidean(joint1, joint3)  # distance between hip and ankle
	HK = distance.euclidean(joint1, joint2)  # distance between hip and knee
	KA = distance.euclidean(joint2, joint3)  # distance between knee and ankle
	try:
		knee_angle_left = (math.degrees(math.acos((HK ** 2 + KA ** 2 - HA ** 2) / (2.0 * HK * KA))))  # use cosine rule
		return knee_angle_left
	except ValueError:
		return

def get_flexion(side, file):
	if side == 'left':
		left_flexion = []
		for i in range(len(file)):
			left_flexion.append(180 - (get_left_knee(i, file)))
		return left_flexion
	if side == 'right':
		right_flexion = []
		for i in range(len(file)):
			right_flexion.append(180 - (get_right_knee(i, file)))
		return right_flexion

### REWRITE THIS FUNCTION
def get_velocity(frame_n, frame_m, joint, data):  # calcualtes the average velocity between two time points from a dataframe
	joint_x = ''.join((joint, '_x'))
	joint_y = ''.join((joint, '_y'))
	joint_z = ''.join((joint, '_z'))
	joint_t0 = (data.iloc[frame_n][joint_x], data.iloc[frame_n][joint_y], data.iloc[frame_n][joint_z])
	joint_t1 = (data.iloc[frame_m][joint_x], data.iloc[frame_m][joint_y], data.iloc[frame_m][joint_z])
	d_dist = math.dist(joint_t1, joint_t0)  # change in distance
	d_time = data['Time'].iloc[frame_m] - data['Time'].iloc[frame_n]  # change in time
	velocity = d_dist / d_time  # change in distance over change in time
	return velocity


def get_all_vel_times(data, joint):
	vel = []
	for i in range(len(data)):
		if data['Time'][i] <= data['Time'].iloc[0]:
			vel.append(None)
		else:
			vel.append(get_velocity(i - 1, i, joint, data))
	return vel



def get_middle_ground(frame, data):
	x1 = (data.iloc[frame]['ankle_l_x'])
	x2 = (data.iloc[frame]['ankle_l_x'])
	x_avg = (x1 + x2) / 2
	y = data.iloc[frame]['pelvis_y']
	z = data.iloc[frame]['pelvis_z']
	mid_pos = (x_avg, y, z)
	return mid_pos


def get_left_hip(frame, data):
	joint1 = [data.iloc[frame]['pelvis_x'], data.iloc[frame]['pelvis_y'], data.iloc[frame]['pelvis_z']]
	joint2 = [data.iloc[frame]['ankle_l_x'], data.iloc[frame]['ankle_l_y'], data.iloc[frame]['ankle_l_z']]
	joint3 = get_middle_ground(frame, data)
	PA = distance.euclidean(joint1, joint2)
	PF = distance.euclidean(joint1, joint3)
	AF = distance.euclidean(joint2, joint3)
	try:
		hip_angle_left = (math.degrees(math.acos((PA ** 2 + AF ** 2 - PF ** 2) / (2.0 * PA * AF))))
		return hip_angle_left
	except ValueError:
		return

def get_right_hip(frame, data):
	joint1 = [data.iloc[frame]['pelvis_x'], data.iloc[frame]['pelvis_y'], data.iloc[frame]['pelvis_z']]
	joint2 = [data.iloc[frame]['ankle_r_x'], data.iloc[frame]['ankle_r_y'], data.iloc[frame]['ankle_r_z']]
	joint3 = get_middle_ground(frame, data)
	PA = distance.euclidean(joint1, joint2)
	PF = distance.euclidean(joint1, joint3)
	AF = distance.euclidean(joint2, joint3)
	try:
		hip_angle_right = (math.degrees(math.acos((PA ** 2 + AF ** 2 - PF ** 2) / (2.0 * PA * AF))))
		return hip_angle_right
	except ValueError:
		return




def get_abduction(side, file):
	if side == 'left':
		left_abduction = []
		for i in range(len(file)):
			left_abduction.append(get_left_hip(i, file))
		return left_abduction
	if side == 'right':
		right_abduction = []
		for i in range(len(file)):
			right_abduction.append(get_right_hip(i, file))
		return right_abduction


def calculate_head_angle(data, frame):  # left leaning or right leaning vs left tilt (degrees) and right tilt (degrees)
	LE = [data.iloc[frame]['ear_l_x']], [data.iloc[frame]['ear_l_y']], [data.iloc[frame]['ear_l_z']]
	RE = [data.iloc[frame]['ear_r_x']], [data.iloc[frame]['ear_r_y']], [data.iloc[frame]['ear_r_z']]
	N = [data.iloc[frame]['neck_x']], [data.iloc[frame]['neck_y']], [data.iloc[frame]['neck_z']]
	LR = distance.euclidean(LE, RE)
	LN = distance.euclidean(LE, N)
	RN = distance.euclidean(RE, N)
	left_head_angle = (math.degrees(math.acos(((LN ** 2 + LR ** 2 - RN ** 2) / (2.0 * LN * LR)))))
	right_head_angle = (math.degrees(math.acos(((RN ** 2 + LR ** 2 - LN ** 2) / (2.0 * RN * LR)))))
	head_angle = None
	if left_head_angle > right_head_angle:
		head_angle = -abs(right_head_angle)
	elif right_head_angle > left_head_angle:
		head_angle = -abs(left_head_angle)
	return head_angle, left_head_angle, right_head_angle

def calculate_head_angle_new(data, frame):
	eye_r = [data.iloc[frame]['eye_r_x']],[data.iloc[frame]['eye_r_z']]
	eye_l = [data.iloc[frame]['eye_l_x']], [data.iloc[frame]['eye_l_z']]
	nose = [data.iloc[frame]['nose_x']], [data.iloc[frame]['nose_z']]
	head = [data.iloc[frame]['head_x']], [data.iloc[frame]['head_z']]
	neck = [data.iloc[frame]['neck_x']], [data.iloc[frame]['neck_z']]
	shoulder_r = [data.iloc[frame]['shoulder_r_x']], [data.iloc[frame]['shoulder_r_z']]
	shoulder_l = [data.iloc[frame]['shoulder_l_x']], [data.iloc[frame]['shoulder_l_z']]
	er_sr = distance.euclidean(eye_r, shoulder_r)
	el_sl = distance.euclidean(eye_l, shoulder_l)
	no_h = distance.euclidean(nose, head)
	no_ne = distance.euclidean(nose, neck)
	h_ne = distance.euclidean(head, neck)
	head_angle = math.degrees(math.acos((no_h ** 2 + no_ne ** 2 - h_ne ** 2)/(2 * no_h * no_ne)))
	if er_sr > el_sl:
		head_angle = -abs(head_angle)
	return head_angle

def calculate_head_angle_new_SMPL(data, frame):
	eye_r = [data.iloc[frame][138]], [data.iloc[frame][140]]
	eye_l = [data.iloc[frame][135]], [data.iloc[frame][137]]
	nose = [data.iloc[frame][132]], [data.iloc[frame][134]]
	head = [data.iloc[frame][129]], [data.iloc[frame][131]]
	neck = [data.iloc[frame][111]], [data.iloc[frame][113]]
	shoulder_r = [data.iloc[frame][99]], [data.iloc[frame][101]]
	shoulder_l = [data.iloc[frame][102]], [data.iloc[frame][104]]
	er_sr = distance.euclidean(eye_r, shoulder_r)
	el_sl = distance.euclidean(eye_l, shoulder_l)
	no_h = distance.euclidean(nose, head)
	no_ne = distance.euclidean(nose, neck)
	h_ne = distance.euclidean(head, neck)
	try:
		head_angle = math.degrees(math.acos((no_h ** 2 + no_ne ** 2 - h_ne ** 2)/(2 * no_h * no_ne)))
		if er_sr > el_sl:
			head_angle = -abs(head_angle)
		return head_angle
	except ValueError:
		print("error")
		return

def get_head_angles(data):
	head_tilt = []
	left_head_angle = []
	right_head_angle = []
	for i in range(len(data)):
		[x.append(y) for x, y in zip([head_tilt, left_head_angle, right_head_angle], calculate_head_angle(data, i))]
	return head_tilt, left_head_angle, right_head_angle

def get_head_angle(file):
	head_tilt = []
	for i in range(len(file)):
		head_tilt.append(calculate_head_angle_new(file, i))
	return head_tilt

def get_head_angle_SMPL(file):
	head_tilt = []
	for i in range(len(file)):
		head_tilt.append(calculate_head_angle_new_SMPL(file, i))
	return head_tilt


def shoulder_angle(data, frame):
	shoulder_tilt = None
	LS = [data.iloc[frame]['shoulder_l_x'], data.iloc[frame]['shoulder_l_y'], data.iloc[frame]['shoulder_l_z']]
	RS = [data.iloc[frame]['shoulder_r_x'], data.iloc[frame]['shoulder_r_y'], data.iloc[frame]['shoulder_r_z']]
	N = [data.iloc[frame]['neck_x'], data.iloc[frame]['neck_y'], data.iloc[frame]['neck_z']]
	LR = distance.euclidean(LS, RS)  # distane from left shoulder and right shoulder
	LN = distance.euclidean(LS, N)  # distance from left shoulder to neck
	RN = distance.euclidean(RS, N)  # distance from the right shoulder to the neck
	left_shoulder_angle = (math.degrees(math.acos((LN ** 2 + LR ** 2 - RN ** 2) / (2.0 * LN * LR))))
	right_shoulder_angle = (math.degrees(math.acos((RN ** 2 + LR ** 2 - LN ** 2) / (2.0 * RN * LR))))
	# these below may need changing, to give specific angle rather than just a binary response
	if left_shoulder_angle > right_shoulder_angle:
		shoulder_tilt = 1
		right_shoulder_angle = -abs(right_shoulder_angle)
	if left_shoulder_angle < right_shoulder_angle:
		shoulder_tilt = -1
		left_shoulder_angle = -abs(left_shoulder_angle)
	return shoulder_tilt, left_shoulder_angle, right_shoulder_angle

def calculate_shoulder_angle(data, frame):
	neck = [data.iloc[frame]['neck_x'], data.iloc[frame]['neck_y'], data.iloc[frame]['neck_z']]
	shoulder_l = [data.iloc[frame]['shoulder_l_x'], data.iloc[frame]['shoulder_l_y'], data.iloc[frame]['shoulder_l_z']]
	shoulder_r = [data.iloc[frame]['shoulder_r_x'], data.iloc[frame]['shoulder_r_y'], data.iloc[frame]['shoulder_r_z']]
	spine_chest = [data.iloc[frame]['spine_chest_x'], data.iloc[frame]['spine_chest_y'], data.iloc[frame]['spine_chest_z']]
	n_sl = distance.euclidean(neck, shoulder_l) #neck to left shoulder
	n_sr = distance.euclidean(neck, shoulder_r) #neck to right shoulder
	sr_sc = distance.euclidean(shoulder_r, spine_chest) #right shoulder to spine chest
	sl_sc = distance.euclidean(shoulder_l, spine_chest) #left shoulder to spine chest
	n_sc = distance.euclidean(neck, spine_chest) #neck to spine chest
	shoulder_angle = None
	shoulder_angle_right = math.degrees(math.acos((n_sr ** 2 + n_sc ** 2 - sr_sc ** 2)/(2 * n_sr * n_sc)))
	shoulder_angle_left = math.degrees(math.acos((n_sl ** 2 + n_sc ** 2 - sl_sc ** 2)/(2 * n_sl * n_sc)))
	shoulder_angle_right_adjusted = 90 - shoulder_angle_right
	shoulder_angle_left_adjusted = 90 - shoulder_angle_left
	if shoulder_l[1] <= shoulder_r[1]:
		left_shoulder_angle = -abs(shoulder_angle_left_adjusted)
		right_shoulder_angle = abs(shoulder_angle_right_adjusted)
		shoulder_angle = (left_shoulder_angle + right_shoulder_angle) / 2
	elif shoulder_r[1] <= shoulder_l[1]:
		right_shoulder_angle = -abs(shoulder_angle_right_adjusted)
		left_shoulder_angle = abs(shoulder_angle_left_adjusted)
		shoulder_angle = (left_shoulder_angle + right_shoulder_angle) / 2
	return shoulder_angle

def calculate_shoulder_angle_SMPL(data, frame):
	neck = [data.iloc[frame][111], data.iloc[frame][112], data.iloc[frame][113]]
	shoulder_l = [data.iloc[frame][102], data.iloc[frame][103], data.iloc[frame][104]]
	shoulder_r = [data.iloc[frame][99], data.iloc[frame][100], data.iloc[frame][101]]
	spine_chest = [data.iloc[frame][120], data.iloc[frame][121], data.iloc[frame][122]] #thorax
	n_sl = distance.euclidean(neck, shoulder_l) #neck to left shoulder
	n_sr = distance.euclidean(neck, shoulder_r) #neck to right shoulder
	sr_sc = distance.euclidean(shoulder_r, spine_chest) #right shoulder to spine chest
	sl_sc = distance.euclidean(shoulder_l, spine_chest) #left shoulder to spine chest
	n_sc = distance.euclidean(neck, spine_chest) #neck to spine chest
	shoulder_angle = None
	shoulder_angle_right = math.degrees(math.acos((n_sr ** 2 + n_sc ** 2 - sr_sc ** 2)/(2 * n_sr * n_sc)))
	shoulder_angle_left = math.degrees(math.acos((n_sl ** 2 + n_sc ** 2 - sl_sc ** 2)/(2 * n_sl * n_sc)))
	shoulder_angle_right_adjusted = 90 - shoulder_angle_right
	shoulder_angle_left_adjusted = 90 - shoulder_angle_left
	if shoulder_l[1] <= shoulder_r[1]:
		left_shoulder_angle = -abs(shoulder_angle_left_adjusted)
		right_shoulder_angle = abs(shoulder_angle_right_adjusted)
		shoulder_angle = (left_shoulder_angle + right_shoulder_angle) / 2
	elif shoulder_r[1] <= shoulder_l[1]:
		right_shoulder_angle = -abs(shoulder_angle_right_adjusted)
		left_shoulder_angle = abs(shoulder_angle_left_adjusted)
		shoulder_angle = (left_shoulder_angle + right_shoulder_angle) / 2
	return shoulder_angle

def get_shoulder_angle_new(data):
	shoulder_angles = []
	for i in range(len(data)):
		shoulder_angles.append(calculate_shoulder_angle(data, i))
	return shoulder_angles

def get_shoulder_angle_new_SMPL(data):
	shoulder_angles = []
	for i in range(len(data)):
		shoulder_angles.append(calculate_shoulder_angle_SMPL(data, i))
	return shoulder_angles

def get_shoulder_angles(data):
	shoulder_tilt = []
	left_shoulder_angle = []
	right_shoulder_angle = []
	for i in range(len(data)):
		[x.append(y) for x, y in
		 zip([shoulder_tilt, left_shoulder_angle, right_shoulder_angle], shoulder_angle(data, i))]
	return shoulder_tilt, left_shoulder_angle, right_shoulder_angle


###Spine calculation needs work - need to come up with a new idea

def spine_arc(data, frame):
	top_spine = [data.iloc[frame]['spine_chest_x'], data.iloc[frame]['spine_chest_y'], data.iloc[frame]['spine_chest_z']]
	mid_spine = [data.iloc[frame]['spine_naval_x'], data.iloc[frame]['spine_naval_y'], data.iloc[frame]['spine_naval_z']]
	lower_spine = [data.iloc[frame]['pelvis_x'], data.iloc[frame]['pelvis_y'], data.iloc[frame]['pelvis_z']]
	TM = distance.euclidean(top_spine, mid_spine)
	ML = distance.euclidean(mid_spine, lower_spine)
	TL = distance.euclidean(top_spine, lower_spine)
	spine_angle = (math.degrees(math.acos((ML ** 2 + TM ** 2 - TL ** 2) / (2.0 * ML * TM))))
	return spine_angle

def spine_arc_SMPL(data, frame):
	top_spine = [data.iloc[frame][120], data.iloc[frame][121], data.iloc[frame][122]] #thorax
	mid_spine = [data.iloc[frame][123], data.iloc[frame][124], data.iloc[frame][125]] #spine
	lower_spine = [data.iloc[frame][117], data.iloc[frame][118], data.iloc[frame][119]] #hip
	TM = distance.euclidean(top_spine, mid_spine)
	ML = distance.euclidean(mid_spine, lower_spine)
	TL = distance.euclidean(top_spine, lower_spine)
	try:
		spine_angle = (math.degrees(math.acos((ML ** 2 + TM ** 2 - TL ** 2) / (2.0 * ML * TM))))
		return spine_angle
	except ValueError:
		return

def get_spine_arcs(file):
	spine = []
	for i in range(len(file)):
		spine.append(spine_arc(file, i))
	return spine

def get_spine_arcs_SMPL(file):
	spine = []
	for i in range(len(file)):
		spine.append(spine_arc_SMPL(file, i))
	return spine

def l_elbow_flexion(data, frame):
	LS_flex = [data.iloc[frame]['shoulder_l_x']], [data.iloc[frame]['shoulder_l_y']], [data.iloc[frame]['shoulder_l_z']]
	LE_flex = [data.iloc[frame]['elbow_l_x']], [data.iloc[frame]['elbow_l_y']], [data.iloc[frame]['elbow_l_z']]
	LW_flex = [data.iloc[frame]['wrist_l_x']], [data.iloc[frame]['wrist_l_y']], [data.iloc[frame]['wrist_l_z']]
	LSE_flex = distance.euclidean(LS_flex, LE_flex)
	LEW_flex = distance.euclidean(LE_flex, LW_flex)
	LSW_flex = distance.euclidean(LS_flex, LW_flex)
	try:
		l_e_flex = (math.degrees(math.acos((LEW_flex ** 2 + LSE_flex ** 2 - LSW_flex ** 2) / (2.0 * LEW_flex * LSE_flex))))
		return l_e_flex
	except ValueError:
		return

def r_elbow_flexion(data, frame):
	RS_flex = [data.iloc[frame]['shoulder_r_x']], [data.iloc[frame]['shoulder_r_y']], [data.iloc[frame]['shoulder_r_z']]
	RE_flex = [data.iloc[frame]['elbow_r_x']], [data.iloc[frame]['elbow_r_y']], [data.iloc[frame]['elbow_r_z']]
	RW_flex = [data.iloc[frame]['wrist_r_x']], [data.iloc[frame]['wrist_r_y']], [data.iloc[frame]['wrist_r_z']]
	RSE_flex = distance.euclidean(RS_flex, RE_flex)
	REW_flex = distance.euclidean(RE_flex, RW_flex)
	RSW_flex = distance.euclidean(RS_flex, RW_flex)
	try:
		r_e_flex = (math.degrees(math.acos((REW_flex ** 2 + RSE_flex ** 2 - RSW_flex ** 2) / (2.0 * REW_flex * RSE_flex))))
		return r_e_flex
	except ValueError:
		return

def get_elbow_flexion(side, file):
	if side == 'left':
		left_elbow_flexion = []
		for i in range(len(file)):
			left_elbow_flexion.append(l_elbow_flexion(file, i))
		return left_elbow_flexion
	if side == 'right':
		right_elbow_flexion = []
		for i in range(len(file)):
			right_elbow_flexion.append(r_elbow_flexion(file, i))
		return right_elbow_flexion


def l_arm_abduction(data, frame):
	LS_abd = [data.iloc[frame]['shoulder_l_x']], [data.iloc[frame]['shoulder_l_y']], [data.iloc[frame]['shoulder_l_z']]
	LW_abd = [data.iloc[frame]['wrist_l_x']], [data.iloc[frame]['wrist_l_y']], [data.iloc[frame]['wrist_l_z']]
	LH_abd = [data.iloc[frame]['hip_l_x']], [data.iloc[frame]['hip_l_y']], [data.iloc[frame]['hip_l_z']]
	LSW_abd = distance.euclidean(LS_abd, LW_abd)
	LWH_abd = distance.euclidean(LW_abd, LH_abd)
	LSH_abd = distance.euclidean(LS_abd, LH_abd)
	try:
		l_arm_abd = (math.degrees(math.acos((LSH_abd ** 2 + LSW_abd ** 2 - LWH_abd ** 2) / (2.0 * LSH_abd * LSW_abd))))
		return l_arm_abd
	except ValueError:
		return

def r_arm_abduction(data, frame):
	RS_abd = [data.iloc[frame]['shoulder_r_x']], [data.iloc[frame]['shoulder_r_y']], [data.iloc[frame]['shoulder_r_z']]
	RW_abd = [data.iloc[frame]['wrist_r_x']], [data.iloc[frame]['wrist_r_y']], [data.iloc[frame]['wrist_r_z']]
	RH_abd = [data.iloc[frame]['hip_r_x']], [data.iloc[frame]['hip_r_y']], [data.iloc[frame]['hip_r_z']]
	RSW_abd = distance.euclidean(RS_abd, RW_abd)
	RWH_abd = distance.euclidean(RW_abd, RH_abd)
	RSH_abd = distance.euclidean(RS_abd, RH_abd)
	try:
		r_arm_abd = (math.degrees(math.acos((RSH_abd ** 2 + RSW_abd ** 2 - RWH_abd ** 2) / (2.0 * RSH_abd * RSW_abd))))
		return r_arm_abd
	except ValueError:
		return


def get_arm_abduction(side, file):
	if side == 'left':
		left_arm_abduction = []
		for i in range(len(file)):
			left_arm_abduction.append(l_arm_abduction(file, i))
		return left_arm_abduction
	if side == 'right':
		right_arm_abduction = []
		for i in range(len(file)):
			right_arm_abduction.append(r_arm_abduction(file, i))
		return right_arm_abduction

def calculate_knee_varus(data, frame, side):
	if side == 'left':
		l_hip = [data.iloc[frame]['hip_l_x']], [data.iloc[frame]['hip_l_z']]
		l_knee = [data.iloc[frame]['knee_l_x']], [data.iloc[frame]['knee_l_z']]
		l_pelvis = [data.iloc[frame]['pelvis_x']], [data.iloc[frame]['pelvis_z']]
		lh_lk = distance.euclidean(l_hip,l_knee)
		lh_lp = distance.euclidean(l_hip,l_pelvis)
		lk_lp = distance.euclidean(l_knee,l_pelvis)
		l_k_varus = (math.degrees(math.acos((lh_lk ** 2 + lk_lp ** 2 - lh_lp ** 2) / (2 * lh_lk * lk_lp))))

		if l_knee[0] < l_hip[0]:
			l_k_varus = -abs(l_k_varus)
		elif l_knee[0] > l_hip[0]:
			l_k_varus = abs(l_k_varus)

		return l_k_varus

	if side == 'right':
		r_hip = [data.iloc[frame]['hip_r_x']], [data.iloc[frame]['hip_r_z']]
		r_knee = [data.iloc[frame]['knee_r_x']], [data.iloc[frame]['knee_r_z']]
		r_pelvis = [data.iloc[frame]['pelvis_x']], [data.iloc[frame]['pelvis_z']]
		rh_rk = distance.euclidean(r_hip,r_knee)
		rh_rp = distance.euclidean(r_hip,r_pelvis)
		rk_rp = distance.euclidean(r_knee,r_pelvis)
		try:
			r_k_varus = (math.degrees(math.acos((rh_rk ** 2 + rk_rp ** 2 - rh_rp ** 2) / (2 * rh_rk * rk_rp))))

			if r_knee[0] > r_hip[0]:
				r_k_varus = -abs(r_k_varus)
			if r_knee[0] < r_hip[0]:
				r_k_varus = abs(r_k_varus)

			return r_k_varus
		except ValueError:
			print("error")
			return

def get_knee_varus(side,file):
	if side == 'left':
		left_knee_varus_valgus = []
		for i in range(len(file)):
			left_knee_varus_valgus.append(calculate_knee_varus(file, i, side))
			#if len(left_knee_varus_valgus) > 3:
				#if left_knee_varus_valgus[-1] and left_knee_varus_valgus[-3] > 0:
					#left_knee_varus_valgus[-1] = abs(left_knee_varus_valgus[-1])
				#elif left_knee_varus_valgus[-1] and left_knee_varus_valgus[-3] < 0:
					#left_knee_varus_valgus[-1] = -abs(left_knee_varus_valgus[-1])
		return left_knee_varus_valgus
	if side == 'right':
		right_knee_varus_valgus = []
		for i in range(len(file)):
			right_knee_varus_valgus.append(calculate_knee_varus(file, i, side))
		#if len(right_knee_varus_valgus) > 3:
			#if right_knee_varus_valgus[-1] and right_knee_varus_valgus[-3] > 0:
				#right_knee_varus_valgus[-1] = abs(right_knee_varus_valgus[-1])
			#elif right_knee_varus_valgus[-1] and right_knee_varus_valgus[-3] < 0:
				#right_knee_varus_valgus[-1] = -abs(right_knee_varus_valgus[-1])
		return right_knee_varus_valgus

def calculate_pelvis_flexion(data, frame):
	chest = [data.iloc[frame]['spine_chest_x']], [data.iloc[frame]['spine_chest_y']], [data.iloc[frame]['spine_chest_z']]
	naval = [data.iloc[frame]['spine_naval_x']], [data.iloc[frame]['spine_naval_y']], [data.iloc[frame]['spine_naval_z']]
	pelvis = [data.iloc[frame]['pelvis_x']], [data.iloc[frame]['pelvis_y']], [data.iloc[frame]['pelvis_z']]
	C_N = distance.euclidean(chest, naval)
	C_P = distance.euclidean(chest, pelvis)
	N_P = distance.euclidean(naval, pelvis)
	pelvis_flexion = (math.degrees(math.acos((N_P ** 2 + C_P ** 2 - C_N ** 2)/(2 * N_P * C_P))))
	return pelvis_flexion

def calculate_pelvis_flexion_SMPL(data, frame):
	chest = [data.iloc[frame][120]], [data.iloc[frame][121]], [data.iloc[frame][122]] #thorax
	naval = [data.iloc[frame][123]], [data.iloc[frame][124]], [data.iloc[frame][125]] #spine (H36M)
	pelvis = [data.iloc[frame][117]], [data.iloc[frame][118]], [data.iloc[frame][119]] #hip
	C_N = distance.euclidean(chest, naval)
	C_P = distance.euclidean(chest, pelvis)
	N_P = distance.euclidean(naval, pelvis)
	try:
		pelvis_flexion = (math.degrees(math.acos((N_P ** 2 + C_P ** 2 - C_N ** 2)/(2 * N_P * C_P))))
		return pelvis_flexion
	except ValueError:
		return

def get_pelvis_flexion(file):
	pelvis_flex = []
	for i in range(len(file)):
		pelvis_flex.append(calculate_pelvis_flexion(file, i))
	return pelvis_flex

def get_pelvis_flexion_SMPL(file):
	pelvis_flex = []
	for i in range(len(file)):
		pelvis_flex.append(calculate_pelvis_flexion_SMPL(file, i))
	return pelvis_flex

def create_dataset(file):
	dataset = pd.DataFrame({
		'left_knee_flexion': get_flexion("left", file),
		'right_knee_flexion': get_flexion("right", file),
		'left_hip_abduction': get_abduction('left', file),
		'right_hip_abduction': get_abduction('right', file),
		'left_elbow_flexion': get_elbow_flexion("left", file),
		'right_elbow_flexion': get_elbow_flexion("right", file),
		'left_arm_abduction': get_arm_abduction("left", file),
		'right_arm_abduction': get_abduction("right", file),
		'spine_arc': get_spine_arcs(file),
		'left_knee_varus': get_knee_varus("left", file),
		'right_knee_varus': get_knee_varus("right", file),
		'pelvis_flexion': get_pelvis_flexion(file),
		'head_angle_new': get_head_angle(file),
		'shoulder_angle_new': get_shoulder_angle_new(file)
	})
	return dataset
def create_dataset_SMPL(file):
	dataset = pd.DataFrame({
		'left_knee_flexion': get_flexion("left", file),
		'right_knee_flexion': get_flexion("right", file),
		'left_hip_abduction': get_abduction('left', file),
		'right_hip_abduction': get_abduction('right', file),
		'left_elbow_flexion': get_elbow_flexion("left", file),
		'right_elbow_flexion': get_elbow_flexion("right", file),
		'left_arm_abduction': get_arm_abduction("left", file),
		'right_arm_abduction': get_arm_abduction("right", file),
		'spine_arc': get_spine_arcs_SMPL(file),
		'left_knee_varus': get_knee_varus("left", file),
		'right_knee_varus': get_knee_varus("right", file),
		'pelvis_flexion': get_pelvis_flexion_SMPL(file),
		'head_angle_new': get_head_angle_SMPL(file),
		'shoulder_angle_new': get_shoulder_angle_new_SMPL(file)
	})
	return dataset
