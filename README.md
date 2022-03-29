# Data-Visualisation-Mocap-Biomechanics-

## How to install:
```
pip install requirements.txt
```
## How to use data dashboard:

If the data source is .json: 
```
bokeh serve --show datadashboard_json.py
```
If the data source is .pkl: 
```
bokeh serve --show datadashboard_smpl.py
```

Once the data dashboard is running, simply select the file you wish to display

## How to use biomechanics calculator
```
python calculate_.py -i [FILE PATH]
```

## How to use data smoothing
```
python data_smoothing.py -i [FILE PATH], -s [SMOOTHING TYPE], -m [SMOOTHING METHOD]
```
-i = input file path

-s = smoothing type (simple or complex)

-m = complex smoothing method (filter or rolling) 
