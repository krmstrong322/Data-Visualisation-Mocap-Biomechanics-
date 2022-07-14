from functions_ import *
import statistics
from scipy.integrate import simps

data_pre = pd.read_csv("af_squat_stats.csv")
data_post = pd.read_csv("af_squat_post_stats.csv")
"""
for x in range(len(data["left_knee_flexion_mean"])):
    if x < len(data["left_knee_flexion_mean"]) -1:
        if ((data["left_knee_flexion_mean"][x+1] - data["left_knee_flexion_mean"][x]) / data["left_knee_flexion_mean"][x]) * 100 > 1:
            print("TRUE")
        else:
            print("FALSE")

for x in range(len(data["left_knee_flexion_mean"])):
    if x < len(data["left_knee_flexion_mean"]) -1:
        if (data["left_knee_flexion_mean"][x+1] > data["left_knee_flexion_mean"][x]):
            print("TRUE")
        else:
            print("FALSE")
"""
area = simps(data_pre["left_knee_flexion_mean"][65:])
print(area)
area2 = simps(data_pre["left_knee_flexion_mean"])
print(area2)

change = ((area2 - area) / area) * 100
print(change)
