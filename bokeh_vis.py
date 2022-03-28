import pandas as pd
import numpy as np
import io
import base64
import itertools
import csv
import sys
from pybase64 import b64decode
from bokeh.io import output_file, output_notebook, curdoc
from bokeh.palettes import inferno
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, DataTable, TableColumn, HoverTool, CDSView, GroupFilter
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel, FileInput

df = pd.DataFrame()
source = ColumnDataSource(df)
columns = [TableColumn(field=col, title=col) for col in df.columns]

file_input = FileInput(accept='.csv', width=900)

# Specify the selection tools to be made available
hover = HoverTool(tooltips=[('Line', '$name')])
select_tools = ['box_select', 'lasso_select', 'poly_select', 'tap', 'pan', 'wheel_zoom', 'undo', 'save', 'reset', hover]

# Create Figures
KneeFig = figure(  # x_axis_type='datetime',
    title='Knee Flexion',
    plot_height=600, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Flexion (degrees)',
    toolbar_location='below',
    tools=select_tools)

KneeVVFig = figure(  # x_axis_type='datetime',
    title='Knee Varus/Valgus',
    plot_height=600, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Varus/Valgus (degrees)',
    toolbar_location='below',
    tools=select_tools)

HipFig = figure(  # x_axis_type='datetime',
    title='Hip Abduction',
    plot_height=600, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Abduction (degrees)',
    toolbar_location='below',
    tools=select_tools)

ElbowFig = figure(  # x_axis_type='datetime',
    title='Elbow Flexion',
    plot_height=600, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Flexion (degrees)',
    toolbar_location='below',
    tools=select_tools)

ArmFig = figure(  # x_axis_type='datetime',
    title='Arm Abduction',
    plot_height=600, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Abduction (degrees)',
    toolbar_location='below',
    tools=select_tools)

HeadAngleFig = figure(  # x_axis_type='datetime',
    title='Head Tilt',
    plot_height=600, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Tilt (degrees)',
    toolbar_location='below',
    tools=select_tools)

ShoulderAngleFig = figure(  # x_axis_type='datetime',
    title='Shoulder Tilt',
    plot_height=600, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Tilt (degrees)',
    toolbar_location='below',
    tools=select_tools)

SpineArcFig = figure(  # x_axis_type='datetime',
    title='Spine Arc',
    plot_height=600, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Spine Arc (degrees)',
    toolbar_location='below',
    tools=select_tools)

PelvisFlexFig = figure(  # x_axis_type='datetime',
    title='Pelvis Flexion',
    plot_height=600, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Pelvis Flexion (degrees)',
    toolbar_location='below',
    tools=select_tools)
"""
VelocityFigArm = figure(
    title='Velocities',
    plot_height=600, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Velocity (mm/ms)',
    toolbar_location='below',
    tools=select_tools)

VelocityFigLeg = figure(
    title='Velocities',
    plot_height=600, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Velocity (mm/ms)',
    toolbar_location='below',
    tools=select_tools)
"""
# Create Panels
KneePanel = Panel(child=KneeFig, title='Knee Flexion')
VarusValgusPanel = Panel(child=KneeVVFig, title='Knee Varus/Valgus')
HipPanel = Panel(child=HipFig, title='Hip Abduction')
ElbowPanel = Panel(child=ElbowFig, title='Elbow Flexion')
ArmPanel = Panel(child=ArmFig, title='Arm Abduction')
HeadAnglePanel = Panel(child=HeadAngleFig, title='Head Tilt')
Shoulder_AnglePanel = Panel(child=ShoulderAngleFig, title='Shoulder Tilt')
SpineArcPanel = Panel(child=SpineArcFig, title='Spine Arc')
PelvisFelxPanel = Panel(child=PelvisFlexFig, title='Pelvis Flexion')
#VelocityPanelArm = Panel(child=VelocityFigArm, title='Arm Velocities')
#VelocityPanelLeg = Panel(child=VelocityFigLeg, title='Leg Velocities')
# Create Tabs
tabs = Tabs(tabs=[KneePanel, VarusValgusPanel, HipPanel, ElbowPanel,
                  ArmPanel, HeadAnglePanel, Shoulder_AnglePanel,
                  SpineArcPanel, PelvisFelxPanel])#, VelocityPanelArm, VelocityPanelLeg])

"""
# Data Upload Functions
def plot_velocities(df):
    velocities = df.iloc[:, -32:]
    arm_cols = velocities.iloc[:, 5:17]
    leg_cols = velocities.iloc[:, 18:25]
    arm_source = ColumnDataSource(arm_cols)
    leg_source = ColumnDataSource(leg_cols)
    armLines = len(arm_cols.columns)
    legLines = len(leg_cols.columns)
    colors = itertools.cycle(inferno(armLines))  # create a color iterator
    for i, j in zip(arm_cols[:-1], range(armLines)):
        VelocityFigArm.line(
            x='index', y=i,
            color=next(colors),  legend_label=i,
            source=arm_source, muted_alpha=0.1,
            name=i
        )
    for i, j in zip(leg_cols[:-1], range(legLines)):
        VelocityFigLeg.line(
            x='index', y=i,
            color=next(colors), legend_label=i,
            source=leg_source, muted_alpha=0.1,
            name=i
        )
    return
"""

def upload_data1(attr, old, new):
    decoded = base64.b64decode(new)
    f = io.BytesIO(decoded)
    df = pd.read_csv(f)
    df.index.rename('Frame')
    df['index'] = df.index
    df = df[['index'] + [col for col in df.columns if col != 'index']]
    #plot_velocities(df)
    source.data = df
    data_table.columns = [TableColumn(field=col, title=col) for col in df.columns]
    KneeFig.line(x='index', y='left_knee_flexion',
                 color='#CE1141', legend_label='Left',
                 source=source, muted_alpha=0.1, name='left_knee_flexion')
    KneeFig.line(x='index', y='right_knee_flexion',
                 color='#006BB6', legend_label='Right',
                 source=source, muted_alpha=0.1, name='right_knee_flexion')
    KneeVVFig.line(x='index', y='left_knee_varus',
                 color='#CE1141', legend_label='Left',
                 source=source, muted_alpha=0.1, name='left_knee_varus')
    KneeVVFig.line(x='index', y='right_knee_varus',
                 color='#006BB6', legend_label='Right',
                 source=source, muted_alpha=0.1, name='right_knee_varus')
    HipFig.line(x='index', y='left_hip_abduction',
                color='#CE1141', legend_label='Left',
                source=source, muted_alpha=0.1, name='left_hip_abduction')
    HipFig.line(x='index', y='right_hip_abduction',
                color='#006BB6', legend_label='Right',
                source=source, muted_alpha=0.1, name='right_hip_abduction')
    ElbowFig.line(x='index', y='left_elbow_flexion',
                  color='#CE1141', legend_label='Left',
                  source=source, muted_alpha=0.1, name='left_elbow_flexion')
    ElbowFig.line(x='index', y='right_elbow_flexion',
                  color='#006BB6', legend_label='Right',
                  source=source, muted_alpha=0.1, name='right_elbow_flexion')
    ArmFig.line(x='index', y='left_arm_abduction',
                color='#CE1141', legend_label='Left',
                source=source, muted_alpha=0.1, name='left_arm_abduction')
    ArmFig.line(x='index', y='right_arm_abduction',
                color='#006BB6', legend_label='Right',
                source=source, muted_alpha=0.1, name='right_arm_abduction')
    HeadAngleFig.line(x='index', y='head_angle_new',
                      color='#CE1141', legend_label='Head Angle',
                      source=source, muted_alpha=0.1, name='head_angle_new')
    ShoulderAngleFig.line(x='index', y='shoulder_angle_new',
                          color='#CE1141', legend_label='Shoulder Angle',
                          source=source, muted_alpha=0.1, name='shoulder_angle_new')
    """
    HeadAngleFig.line(x='index', y='left_head_angle',
                      color='#CE1141', legend_label='Left Head Angle',
                      source=source, muted_alpha=0.1, name='left_head_angle')
    HeadAngleFig.line(x='index', y='right_head_angle',
                      color='#CE1141', legend_label='Right Head Angle',
                      source=source, muted_alpha=0.1, name='right_head_angle')
    
    ShoulderAngleFig.line(x='index', y='left_shoulder_angle',
                          color='#CE1141', legend_label='Left Shoulder Angle',
                          source=source, muted_alpha=0.1, name='left_shoulder_angle')
    ShoulderAngleFig.line(x='index', y='right_shoulder_angle',
                          color='#CE1141', legend_label='Right Shoulder Angle',
                          source=source, muted_alpha=0.1, name='right_shoulder_angle')
    """
    SpineArcFig.line(x='index', y='spine_arc',
                     color='#CE1141', legend_label='Spine Arc',
                     source=source, muted_alpha=0.1, name='spine_arc')
    PelvisFlexFig.line(x='index', y='pelvis_flexion',
                     color='#CE1141', legend_label='Pelvis Flexion',
                     source=source, muted_alpha=0.1, name='pelvis_flexion')
    KneeFig.legend.location = 'top_left'
    KneeVVFig.legend.location = 'top_left'
    HipFig.legend.location = 'top_left'
    ElbowFig.legend.location = 'top_left'
    ArmFig.legend.location = 'top_left'
    HeadAngleFig.legend.location = 'top_left'
    ShoulderAngleFig.legend.location = 'top_left'
    SpineArcFig.legend.location = 'top_left'
    PelvisFlexFig.legend.location = 'top_left'
    #VelocityFigArm.legend.location = 'top_left'
    #VelocityFigLeg.legend.location = 'top_left'

    KneeFig.legend.click_policy = 'mute'
    KneeVVFig.legend.click_policy = 'mute'
    HipFig.legend.click_policy = 'mute'
    ElbowFig.legend.click_policy = 'mute'
    ArmFig.legend.click_policy = 'mute'
    HeadAngleFig.legend.click_policy = 'mute'
    ShoulderAngleFig.legend.click_policy = 'mute'
    SpineArcFig.legend.click_policy = 'mute'
    #VelocityFigArm.legend.click_policy = 'mute'
    #VelocityFigLeg.legend.click_policy = 'mute'


file_input.on_change('value', upload_data1)
data_table = DataTable(source=source, columns=columns, width=900, height=400)
#curdoc().theme = 'dark_minimal'
curdoc().add_root(column(file_input, tabs, data_table))

# Determine where the visualization will be rendered
# output_file('filename.html', title='Patient Biomechanics')  # Render to static HTML, or
# output_notebook()  # Render inline in a Jupyter Notebook


# Widget
