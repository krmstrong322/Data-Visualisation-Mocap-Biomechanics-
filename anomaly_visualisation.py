import plotly.graph_objects as go
import argparse
import pandas as pd
from sklearn import svm
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from functions_ import *

parser = argparse.ArgumentParser()
parser.add_argument("--colour", type=str)
parser.add_argument("--ID", type=int)
args = parser.parse_args()

body_index =    ["pelvis", "spine_naval", "spine_chest", "neck", "clavicle_l", "shoulder_l", "elbow_l", "wrist_l", "hand_l", "handtip_l",
                "thumb_l", "clavicle_r", "shoulder_r", "elbow_r", "wrist_r", "hand_r", "handtip_r", "thumb_r", "hip_l", "knee_l", "ankle_l",
                "foot_l", "hip_r", "knee_r", "ankle_r", "foot_r", "head", "nose", "eye_l", "ear_l", "eye_r", "ear_r"]

outliers_fraction = 0.15
anomaly_algorithms = [
    ("Robust covariance", EllipticEnvelope(contamination=outliers_fraction,
                                           random_state=42)),
    ("One-Class SVM", svm.OneClassSVM(nu=outliers_fraction, kernel="rbf",
                                      gamma=0.1)),
    ("Isolation Forest", IsolationForest(contamination=outliers_fraction, random_state=42,
                                         bootstrap=False, verbose=0)),
    ("Local Outlier Factor", LocalOutlierFactor(n_neighbors=35, contamination=outliers_fraction,
                                                novelty=True))]

def test_anomalies(data,anomaly_list):
	algorithm_names = ["Robust covariance","One-Class SVM","Isolation Forest","Local Outlier Factor"]
	for i in range(len(anomaly_list)):
		clf = anomaly_list[i][1]
		clf.fit(data)
		pred = clf.predict(data)
		data[algorithm_names[i]] = pred
		outliers = data.loc[data[algorithm_names[i]] == -1]
		outlier_index = list(outliers.index)
	return outlier_index

#dataset = create_dataset(pd.read_csv("nokneekg_normal_1_master.csv"))

#print(dataset)

data = pd.read_csv("nokneekg_normal_1_master.csv")
nested_list = {}

d = {}
for i in body_index:
	d["{0}".format(i)] = get_all_vel_times(data,i)
	#print(d["{0}".format(i)])
#df = pd.DataFrame.from_dict(d, orient='columns', columns=body_index)
print(d.keys())
print(len(d.keys()))
for item in body_index:
	print(d[item])
"""
flexion = pd.read_csv("ml_test.csv")
x = flexion.filter(like="Flexion")
dataset = test_anomalies(x,anomaly_algorithms)


dataset['index1'] = dataset.index


colorsIdx = {-1: 'rgb(215,48,39)', 1: 'rgb(0,128,0)'}
cols      = dataset['Robust covariance'].map(colorsIdx)
#print(df.columns)
#fig = px.scatter(df, y="Flexion", color="Robust covariance")
fig = go.Figure()
fig.add_trace(go.Scatter(x=dataset["index1"], y=dataset["Flexion"],
                         mode='lines',
                         line=dict(width=1, color="#000000")))
fig.add_trace(go.Scatter(x=dataset["index1"], y=dataset["Flexion"],
                         mode="markers",
                         marker=dict(size=5, color=cols)))

fig.update_layout(showlegend=False)

fig.write_html("figure_rc.html", auto_open=True)

"""
