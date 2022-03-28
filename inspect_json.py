import json
import pandas as pd

"""
# Opening JSON file
f = open('sit.json')

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
for i in data:
	print(data["frames"])

# Closing file
f.close()
"""

from cherrypicker import CherryPicker
import json
import pandas as pd
import numpy as np
import argparse, os
import bvhtoolbox

b_index =    ["pelvis_x","pelvis_y","pelvis_z","spine_naval_x","spine_naval_y","spine_naval_z","spine_chest_x","spine_chest_y","spine_chest_z","neck_x","neck_y","neck_z","clavicle_l_x",
              "clavicle_l_y","clavicle_l_z","shoulder_l_x","shoulder_l_y","shoulder_l_z","elbow_l_x","elbow_l_y","elbow_l_z","wrist_l_x","wrist_l_y","wrist_l_z", "hand_l_x","hand_l_y",
              "hand_l_z", "handtip_l_x","handtip_l_y","handtip_l_z","thumb_l_x","thumb_l_y","thumb_l_z", "clavicle_r_x","clavicle_r_y","clavicle_r_z","shoulder_r_x","shoulder_r_y","shoulder_r_z",
              "elbow_r_x","elbow_r_y","elbow_r_z", "wrist_r_x","wrist_r_y","wrist_r_z", "hand_r_x","hand_r_y","hand_r_z", "handtip_r_x","handtip_r_y","handtip_r_z","thumb_r_x","thumb_r_y","thumb_r_z",
              "hip_l_x","hip_l_y","hip_l_z", "knee_l_x","knee_l_y","knee_l_z", "ankle_l_x","ankle_l_y","ankle_l_z","foot_l_x","foot_l_y","foot_l_z", "hip_r_x","hip_r_y","hip_r_z","knee_r_x","knee_r_y","knee_r_z",
              "ankle_r_x","ankle_r_y","ankle_r_z", "foot_r_x","foot_r_y","foot_r_z", "head_x","head_y","head_z", "nose_x","nose_y","nose_z", "eye_l_x","eye_l_y","eye_l_z", "ear_l_x","ear_l_y","ear_l_z",
              "eye_r_x","eye_r_y","eye_r_z","ear_r_x","ear_r_y","ear_r_z"]

def validate_file(f):
	if not os.path.exists(f):
		# Argparse uses the ArgumentTypeError to give a rejection message like:
		# error: argument input: x does not exist
		raise argparse.ArgumentTypeError("{0} does not exist".format(f))
	return f

parser = argparse.ArgumentParser(description="Read file form Command line.")
parser.add_argument("-i", "--input", dest="filename", required=True, type=validate_file,
	                    help="input file", metavar="FILE")
args = parser.parse_args()

def json_to_biomechanics():
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


with open('sit.json') as file:
	data = json.load(file)
"""
picker = CherryPicker(data)
flat = picker['frames'].flatten().get()
df = pd.DataFrame(flat)
df.to_csv("sit_json.csv", index=False)
"""

bone_list = []
positions = []
orientations = []
bodies = []
nested = []

bone_list.append(data['bone_list'])

for i in data['frames']:
	bodies.append(i['bodies'])

for i in range(len(bodies)):
	orientations.append(bodies[i][0]['joint_orientations'])
	positions.append(np.array(bodies[i][0]['joint_positions']).flatten())
"""
dict_pos = {}

for x in range(len(positions)):
	for i in positions:
		dict_pos[x] = i

print(dict_pos[0])
"""
df_ind = pd.DataFrame(bone_list)
df_ori = pd.DataFrame(orientations)
df_pos = pd.DataFrame(positions)


df_pos.columns = b_index
print(df_pos)



#df_ind.to_csv('hierarchy.csv', index=False)
#df_ori.to_csv('rotation.csv', index=False)
#df_pos.to_csv('position.csv', index=False)

#print(df_ind)
#print(df_ori)
#print(df_pos)
