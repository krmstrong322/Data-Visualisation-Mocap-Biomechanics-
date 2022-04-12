import io
import base64
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, DataTable, TableColumn, HoverTool
from bokeh.layouts import column
from bokeh.models.widgets import Tabs, Panel, FileInput
from functions_ import *
import joblib

df = pd.DataFrame()
source = ColumnDataSource(df)
columns = [TableColumn(field=col, title=col) for col in df.columns]

file_input = FileInput(accept='.csv, .json, .pkl', width=1600)

# Specify the selection tools to be made available
hover = HoverTool(tooltips=[('Line', '$name')])
select_tools = ['box_select', 'lasso_select', 'poly_select', 'tap', 'pan', 'wheel_zoom', 'undo', 'save', 'reset', hover]

# Create Figures
KneeFig = figure(
    title='Knee Flexion',
    plot_height=800, plot_width=1600,
    x_axis_label='Frame',
    y_axis_label='Flexion (degrees)',
    toolbar_location='below',
    tools=select_tools)

KneeVVFig = figure(
    title='Knee Varus/Valgus',
    plot_height=800, plot_width=1600,
    x_axis_label='Frame',
    y_axis_label='Varus/Valgus (degrees)',
    toolbar_location='below',
    tools=select_tools)

HipFig = figure(
    title='Hip Abduction',
    plot_height=800, plot_width=1600,
    x_axis_label='Frame',
    y_axis_label='Abduction (degrees)',
    toolbar_location='below',
    tools=select_tools)

ElbowFig = figure(
    title='Elbow Flexion',
    plot_height=800, plot_width=1600,
    x_axis_label='Frame',
    y_axis_label='Flexion (degrees)',
    toolbar_location='below',
    tools=select_tools)

ArmFig = figure(
    title='Arm Abduction',
    plot_height=800, plot_width=1600,
    x_axis_label='Frame',
    y_axis_label='Abduction (degrees)',
    toolbar_location='below',
    tools=select_tools)

HeadAngleFig = figure(
    title='Head Tilt',
    plot_height=800, plot_width=1600,
    x_axis_label='Frame',
    y_axis_label='Tilt (degrees)',
    toolbar_location='below',
    tools=select_tools)

ShoulderAngleFig = figure(
    title='Shoulder Tilt',
    plot_height=800, plot_width=1600,
    x_axis_label='Frame',
    y_axis_label='Tilt (degrees)',
    toolbar_location='below',
    tools=select_tools)

SpineArcFig = figure(
    title='Spine Arc',
    plot_height=800, plot_width=1600,
    x_axis_label='Frame',
    y_axis_label='Spine Arc (degrees)',
    toolbar_location='below',
    tools=select_tools)

PelvisFlexFig = figure(
    title='Pelvis Flexion',
    plot_height=800, plot_width=1600,
    x_axis_label='Frame',
    y_axis_label='Pelvis Flexion (degrees)',
    toolbar_location='below',
    tools=select_tools)

# Create Panels
KneePanel = Panel(child=KneeFig, title='Knee Flexion')
VarusValgusPanel = Panel(child=KneeVVFig, title='Knee Varus/Valgus')
HipPanel = Panel(child=HipFig, title='Hip Abduction')
ElbowPanel = Panel(child=ElbowFig, title='Elbow Flexion')
ArmPanel = Panel(child=ArmFig, title='Arm Abduction')
HeadAnglePanel = Panel(child=HeadAngleFig, title='Head Tilt')
Shoulder_AnglePanel = Panel(child=ShoulderAngleFig, title='Shoulder Tilt')
SpineArcPanel = Panel(child=SpineArcFig, title='Spine Arc')
PelvisFlexPanel = Panel(child=PelvisFlexFig, title='Pelvis Flexion')

# Create Tabs
tabs = Tabs(tabs=[KneePanel, VarusValgusPanel, HipPanel, ElbowPanel,
                  ArmPanel, HeadAnglePanel, Shoulder_AnglePanel,
                  SpineArcPanel, PelvisFlexPanel])


def upload_data1(attr, old, new):
    decoded = base64.b64decode(new)
    f = io.BytesIO(decoded)
    #data = joblib.load(f)
    #mpl_df = joints_from_smpl(data)
    #df = create_dataset_SMPL(smpl_df)
    df = pd.read_csv(f)
    df.index.rename('Frame')
    df['index'] = df.index
    df = df[['index'] + [col for col in df.columns if col != 'index']]
    source.data = df
    data_table.columns = [TableColumn(field=col, title=col) for col in df.columns]
    KneeFig.line(x='index', y='left_knee_flexion_mean',
                 color='#006BB6', legend_label='Left (Mean)',
                 source=source, muted_alpha=0.1, name='left_knee_flexion_mean')
    KneeFig.line(x='index', y='left_knee_flexion_min',
                 color='#006BB6', legend_label='Left (Min)',
                 source=source, muted_alpha=0.1, name='left_knee_flexion_min')
    KneeFig.line(x='index', y='left_knee_flexion_max',
                 color='#006BB6', legend_label='Left (Max)',
                 source=source, muted_alpha=0.1, name='left_knee_flexion_max')
    KneeFig.line(x='index', y='right_knee_flexion_mean (Mean)',
                 color='#CE1141', legend_label='Right',
                 source=source, muted_alpha=0.1, name='right_knee_flexion_mean')
    KneeFig.line(x='index', y='right_knee_flexion_min (Min)',
                 color='#CE1141', legend_label='Right',
                 source=source, muted_alpha=0.1, name='right_knee_flexion_min')
    KneeFig.line(x='index', y='right_knee_flexion_max',
                 color='#CE1141', legend_label='Right (Max)',
                 source=source, muted_alpha=0.1, name='right_knee_flexion_max')
    KneeVVFig.line(x='index', y='left_knee_varus_mean',
                   color='#006BB6', legend_label='Left',
                   source=source, muted_alpha=0.1, name='left_knee_varus_mean')
    KneeVVFig.line(x='index', y='left_knee_varus_min',
                   color='#006BB6', legend_label='Left',
                   source=source, muted_alpha=0.1, name='left_knee_varus_min')
    KneeVVFig.line(x='index', y='left_knee_varus_max',
                   color='#006BB6', legend_label='Left',
                   source=source, muted_alpha=0.1, name='left_knee_varus_max')
    KneeVVFig.line(x='index', y='right_knee_varus_mean',
                   color='#CE1141', legend_label='Right',
                   source=source, muted_alpha=0.1, name='right_knee_varus_mean')
    KneeVVFig.line(x='index', y='right_knee_varus_min',
                   color='#CE1141', legend_label='Right',
                   source=source, muted_alpha=0.1, name='right_knee_varus_min')
    KneeVVFig.line(x='index', y='right_knee_varus_max',
                   color='#CE1141', legend_label='Right',
                   source=source, muted_alpha=0.1, name='right_knee_varus_max')
    HipFig.line(x='index', y='left_hip_abduction_mean',
                color='#006BB6', legend_label='Left',
                source=source, muted_alpha=0.1, name='left_hip_abduction_mean')
    HipFig.line(x='index', y='left_hip_abduction_min',
                color='#006BB6', legend_label='Left',
                source=source, muted_alpha=0.1, name='left_hip_abduction_min')
    HipFig.line(x='index', y='left_hip_abduction_max',
                color='#006BB6', legend_label='Left',
                source=source, muted_alpha=0.1, name='left_hip_abduction_max')
    HipFig.line(x='index', y='right_hip_abduction_mean',
                color='#CE1141', legend_label='Right',
                source=source, muted_alpha=0.1, name='right_hip_abduction_mean')
    HipFig.line(x='index', y='right_hip_abduction_min',
                color='#CE1141', legend_label='Right',
                source=source, muted_alpha=0.1, name='right_hip_abduction_min')
    HipFig.line(x='index', y='right_hip_abduction_max',
                color='#CE1141', legend_label='Right',
                source=source, muted_alpha=0.1, name='right_hip_abduction_max')
    ElbowFig.line(x='index', y='left_elbow_flexion_mean',
                  color='#006BB6', legend_label='Left',
                  source=source, muted_alpha=0.1, name='left_elbow_flexion_mean')
    ElbowFig.line(x='index', y='left_elbow_flexion_min',
                  color='#006BB6', legend_label='Left',
                  source=source, muted_alpha=0.1, name='left_elbow_flexion_min')
    ElbowFig.line(x='index', y='left_elbow_flexion_max',
                  color='#006BB6', legend_label='Left',
                  source=source, muted_alpha=0.1, name='left_elbow_flexion_max')
    ElbowFig.line(x='index', y='right_elbow_flexion_mean',
                  color='#CE1141', legend_label='Right',
                  source=source, muted_alpha=0.1, name='right_elbow_flexion_mean')
    ElbowFig.line(x='index', y='right_elbow_flexion_min',
                  color='#CE1141', legend_label='Right',
                  source=source, muted_alpha=0.1, name='right_elbow_flexion_min')
    ElbowFig.line(x='index', y='right_elbow_flexion_max',
                  color='#CE1141', legend_label='Right',
                  source=source, muted_alpha=0.1, name='right_elbow_flexion_max')
    ArmFig.line(x='index', y='left_arm_abduction_mean',
                color='#006BB6', legend_label='Left',
                source=source, muted_alpha=0.1, name='left_arm_abduction_mean')
    ArmFig.line(x='index', y='left_arm_abduction_min',
                color='#006BB6', legend_label='Left',
                source=source, muted_alpha=0.1, name='left_arm_abduction_min')
    ArmFig.line(x='index', y='left_arm_abduction_max',
                color='#006BB6', legend_label='Left',
                source=source, muted_alpha=0.1, name='left_arm_abduction_max')
    ArmFig.line(x='index', y='right_arm_abduction_mean',
                color='#CE1141', legend_label='Right',
                source=source, muted_alpha=0.1, name='right_arm_abduction_mean')
    ArmFig.line(x='index', y='right_arm_abduction_min',
                color='#CE1141', legend_label='Right',
                source=source, muted_alpha=0.1, name='right_arm_abduction_min')
    ArmFig.line(x='index', y='right_arm_abduction_max',
                color='#CE1141', legend_label='Right',
                source=source, muted_alpha=0.1, name='right_arm_abduction_max')
    HeadAngleFig.line(x='index', y='head_angle_new_mean',
                      color='#CE1141', legend_label='Head Angle',
                      source=source, muted_alpha=0.1, name='head_angle_new_mean')
    HeadAngleFig.line(x='index', y='head_angle_new_min',
                      color='#CE1141', legend_label='Head Angle',
                      source=source, muted_alpha=0.1, name='head_angle_new_min')
    HeadAngleFig.line(x='index', y='head_angle_new_max',
                      color='#CE1141', legend_label='Head Angle',
                      source=source, muted_alpha=0.1, name='head_angle_new_max')
    ShoulderAngleFig.line(x='index', y='shoulder_angle_new_mean',
                          color='#CE1141', legend_label='Shoulder Angle',
                          source=source, muted_alpha=0.1, name='shoulder_angle_new_mean')
    ShoulderAngleFig.line(x='index', y='shoulder_angle_new_min',
                          color='#CE1141', legend_label='Shoulder Angle',
                          source=source, muted_alpha=0.1, name='shoulder_angle_new_min')
    ShoulderAngleFig.line(x='index', y='shoulder_angle_new_max',
                          color='#CE1141', legend_label='Shoulder Angle',
                          source=source, muted_alpha=0.1, name='shoulder_angle_new_max')
    SpineArcFig.line(x='index', y='spine_arc_mean',
                     color='#CE1141', legend_label='Spine Arc',
                     source=source, muted_alpha=0.1, name='spine_arc_mean')
    SpineArcFig.line(x='index', y='spine_arc_min',
                     color='#CE1141', legend_label='Spine Arc',
                     source=source, muted_alpha=0.1, name='spine_arc_min')
    SpineArcFig.line(x='index', y='spine_arc_max',
                     color='#CE1141', legend_label='Spine Arc',
                     source=source, muted_alpha=0.1, name='spine_arc_max')
    PelvisFlexFig.line(x='index', y='pelvis_flexion_mean',
                       color='#CE1141', legend_label='Pelvis Flexion (Mean)',
                       source=source, muted_alpha=0.1, name='pelvis_flexion_mean')
    PelvisFlexFig.line(x='index', y='pelvis_flexion_min',
                       color='#CE1141', legend_label='Pelvis Flexion (Min)',
                       source=source, muted_alpha=0.1, name='pelvis_flexion_min')
    PelvisFlexFig.line(x='index', y='pelvis_flexion_max',
                       color='#CE1141', legend_label='Pelvis Flexion (Max)',
                       source=source, muted_alpha=0.1, name='pelvis_flexion_max')

    KneeFig.legend.location = 'top_left'
    KneeVVFig.legend.location = 'top_left'
    HipFig.legend.location = 'top_left'
    ElbowFig.legend.location = 'top_left'
    ArmFig.legend.location = 'top_left'
    HeadAngleFig.legend.location = 'top_left'
    ShoulderAngleFig.legend.location = 'top_left'
    SpineArcFig.legend.location = 'top_left'
    PelvisFlexFig.legend.location = 'top_left'

    KneeFig.legend.click_policy = 'mute'
    KneeVVFig.legend.click_policy = 'mute'
    HipFig.legend.click_policy = 'mute'
    ElbowFig.legend.click_policy = 'mute'
    ArmFig.legend.click_policy = 'mute'
    HeadAngleFig.legend.click_policy = 'mute'
    ShoulderAngleFig.legend.click_policy = 'mute'
    SpineArcFig.legend.click_policy = 'mute'


file_input.on_change('value', upload_data1)
data_table = DataTable(source=source, columns=columns, width=1600, height=300)
# curdoc().theme = 'dark_minimal'
curdoc().add_root(column(file_input, tabs, data_table))

# Determine where the visualization will be rendered
# output_file('filename.html', title='Patient Biomechanics')  # Render to static HTML, or
# output_notebook()  # Render inline in a Jupyter Notebook


# Widget
