import joblib  # you may use native pickle here as well
import pandas as pd
import numpy as np
import itertools
import more_itertools

rename_dict_OP = {6: 'shoulder_r_x', 7: 'shoulder_r_y', 8: 'shoulder_r_z',
                  9: 'elbow_r_x', 10: 'elbow_r_y', 11: 'elbow_r_z',
                  12: 'wrist_r_x', 13: 'wrist_r_y', 14: 'wrist_r_x',
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

rename_dict_SPIN = {75: 'ankle_r_x',76: 'ankle_r_y',77: 'ankle_r_z',
                    78: 'knee_r_x',79: 'knee_r_y',80: 'knee_r_z',

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


output = joblib.load(r'C:\Users\Kai Armstrong\Desktop\DTP-KNEE-main\PKL\sit.pkl')

print(joints_from_smpl(output))
final_df = (joints_from_smpl(output))
final_df.to_csv('sit_smpl.csv')
print(list(joints_from_smpl(output).columns.values))

"""
joints = output[1]['joints3d']
#print(joints)
lists = {}
for i in range(len(joints)):
	lists[i] = list(more_itertools.collapse(joints[i]))
print(len(lists))
for i in lists:
	print(lists[i])
print(lists.keys())
#print(list(more_itertools.collapse(joints[0])))
df = pd.DataFrame(lists)
df.reset_index(drop=True, inplace=True)
df_transposed = df.T
print(df_transposed)

full_list = []
for i in range(len(output[1]['joints3d'])):
	empty_list = []
	#d[i] = list(more_itertools.collapse(output[1]['joints3d'][i]))
	for j in range(len(output[1]['joints3d'])):
		empty_list.append(list(more_itertools.collapse(output[1]['joints3d'][i])))
	full_list.append(empty_list)
#df = pd.DataFrame(d, index=list(range(len(output[1]['joints3d']))))
#print(df)
print(full_list)


collected_list = []
for i in range(len(output[1]['joints3d'])):
	collected_list.append(output[1]['joints3d'][i])
#print(collected_list)
flattened_list = list(itertools.chain.from_iterable(collected_list))
merged = list(itertools.chain(*collected_list))
df = pd.DataFrame(merged)
print(df)
"""
# print(output[1]['pose'])

# pose_three_d = pd.DataFrame(output[1]['pose'])

# pose_three_d.to_csv('pose.csv', index=False)

# print(output[1]['betas'])

# betas = pd.DataFrame(output[1]['betas'])

# betas.to_csv('betas.csv', index=False)

# test = output[1]['joints3d']
# print(np.shape(test))
# for i in test:
# print(np.shape(i))
# for j in i:
# print(np.shape(j))
# print(j)

# np.savetxt("test.txt", test, delimiter=',')

# joints = pd.DataFrame(joints_dict)

# joints.to_csv('joints.csv', index=False)

"""
import smplx
import trimesh
import pyrender

vertices = output[1]['verts'][0]

mesh = trimesh.Trimesh(vertices=vertices)
mesh_fname = 'my_mesh.obj'
#mesh.export(mesh_fname)



fuze_trimesh = trimesh.load('my_mesh.obj')
new_mesh = pyrender.Scene.from_trimesh_scene(fuze_trimesh)
#new_mesh = pyrender.Mesh.from_trimesh(fuze_trimesh)
scene = pyrender.Scene.from_trimesh_scene(fuze_trimesh)
#scene = pyrender.Scene()
#scene.add(new_mesh)
pyrender.Viewer(scene)
"""
