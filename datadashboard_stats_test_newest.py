import io
import base64
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, DataTable, TableColumn, HoverTool
from bokeh.layouts import column, row, gridplot, layout
from bokeh.models.widgets import Tabs, Panel, FileInput
from functions_ import *
import joblib

df = pd.DataFrame()
source = ColumnDataSource(df)
columns = [TableColumn(field=col, title=col) for col in df.columns]

df2 = pd.DataFrame()
source2 = ColumnDataSource(df)
columns2 = [TableColumn(field=col, title=col) for col in df.columns]

file_input1 = FileInput(accept='.csv, .json, .pkl', sizing_mode= "scale_width")

# Specify the selection tools to be made available
hover = HoverTool(tooltips=[('Line', '$name')])
select_tools = ['box_select', 'lasso_select', 'poly_select', 'tap', 'pan', 'wheel_zoom', 'undo', 'save', 'reset', hover]

# Create Figures
KneeFig = figure(
    title='Knee Flexion',
    #plot_height=900, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Flexion (degrees)',
    toolbar_location='below',
	sizing_mode= "scale_both",
    tools=select_tools)

KneeVVFig = figure(
    title='Knee Varus/Valgus',
    #plot_height=900, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Varus/Valgus (degrees)',
    toolbar_location='below',
	sizing_mode= "scale_both",
    tools=select_tools)

HipFig = figure(
    title='Hip Abduction',
    #plot_height=900, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Abduction (degrees)',
    toolbar_location='below',
	sizing_mode="scale_both",
	tools=select_tools)

ElbowFig = figure(
    title='Elbow Flexion',
    #plot_height=900, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Flexion (degrees)',
    toolbar_location='below',
	sizing_mode="scale_both",
	tools=select_tools)

ArmFig = figure(
    title='Arm Abduction',
    #plot_height=900, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Abduction (degrees)',
    toolbar_location='below',
	sizing_mode="scale_both",
	tools=select_tools)

HeadAngleFig = figure(
    title='Head Tilt',
    #plot_height=900, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Tilt (degrees)',
    toolbar_location='below',
	sizing_mode="scale_both",
	tools=select_tools)

ShoulderAngleFig = figure(
    title='Shoulder Tilt',
    #plot_height=900, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Tilt (degrees)',
    toolbar_location='below',
	sizing_mode="scale_both",
	tools=select_tools)

SpineArcFig = figure(
    title='Spine Arc',
    #plot_height=900, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Spine Arc (degrees)',
    toolbar_location='below',
	sizing_mode="scale_both",
	tools=select_tools)
PelvisFlexFig = figure(
    title='Pelvis Flexion',
    #plot_height=900, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Pelvis Flexion (degrees)',
    toolbar_location='below',
	sizing_mode="scale_both",
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
left_tabs = Tabs(tabs=[KneePanel, VarusValgusPanel, HipPanel, ElbowPanel,
                  ArmPanel])

KneeFig2 = figure(
    title='Knee Flexion',
    #plot_height=900, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Flexion (degrees)',
    toolbar_location='below',
	sizing_mode="scale_both",
	tools=select_tools)

KneeVVFig2 = figure(
    title='Knee Varus/Valgus',
    #plot_height=900, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Varus/Valgus (degrees)',
    toolbar_location='below',
	sizing_mode="scale_both",
	tools=select_tools)

HipFig2 = figure(
    title='Hip Abduction',
    #plot_height=900, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Abduction (degrees)',
    toolbar_location='below',
	sizing_mode="scale_both",
	tools=select_tools)

ElbowFig2 = figure(
    title='Elbow Flexion',
    #plot_height=900, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Flexion (degrees)',
    toolbar_location='below',
	sizing_mode="scale_both",
	tools=select_tools)

ArmFig2 = figure(
    title='Arm Abduction',
    #plot_height=900, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Abduction (degrees)',
    toolbar_location='below',
	sizing_mode="scale_both",
	tools=select_tools)

HeadAngleFig2 = figure(
    title='Head Tilt',
    #plot_height=900, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Tilt (degrees)',
    toolbar_location='below',
	sizing_mode="scale_both",
	tools=select_tools)

ShoulderAngleFig2 = figure(
    title='Shoulder Tilt',
    #plot_height=900, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Tilt (degrees)',
    toolbar_location='below',
	sizing_mode="scale_both",
	tools=select_tools)

SpineArcFig2 = figure(
    title='Spine Arc',
    #plot_height=900, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Spine Arc (degrees)',
    toolbar_location='below',
	sizing_mode="scale_both",
	tools=select_tools)

PelvisFlexFig2 = figure(
    title='Pelvis Flexion',
    #plot_height=900, plot_width=900,
    x_axis_label='Frame',
    y_axis_label='Pelvis Flexion (degrees)',
    toolbar_location='below',
	sizing_mode="scale_both",
	tools=select_tools)

# Create Panels
KneePanel2 = Panel(child=KneeFig2, title='Knee Flexion')
VarusValgusPanel2 = Panel(child=KneeVVFig2, title='Knee Varus/Valgus')
HipPanel2 = Panel(child=HipFig2, title='Hip Abduction')
ElbowPanel2 = Panel(child=ElbowFig2, title='Elbow Flexion')
ArmPanel2 = Panel(child=ArmFig2, title='Arm Abduction')
HeadAnglePanel2 = Panel(child=HeadAngleFig2, title='Head Tilt')
Shoulder_AnglePanel2 = Panel(child=ShoulderAngleFig2, title='Shoulder Tilt')
SpineArcPanel2 = Panel(child=SpineArcFig2, title='Spine Arc')
PelvisFlexPanel2 = Panel(child=PelvisFlexFig2, title='Pelvis Flexion')

# Create Tabs
right_tabs = Tabs(tabs=[KneePanel2, VarusValgusPanel2, HipPanel2, ElbowPanel2,
                  ArmPanel2])

middle_tabs = Tabs(tabs=[HeadAnglePanel, Shoulder_AnglePanel,
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
    #data_table.columns = [TableColumn(field=col, title=col) for col in df.columns]

    KneeFig.line(x='index', y='left_knee_flexion_mean',
                 color='#0000FF' , legend_label='Left (Mean)',
                 source=source, muted_alpha=0.1, name='left_knee_flexion_mean')
    KneeFig.line(x='index', y='right_knee_flexion_mean',
                 color='#00FF00', legend_label='Right (Mean)',
                 source=source, muted_alpha=0.1, name='left_knee_flexion_mean')
    KneeFig.varea(x='index', y1='left_knee_flexion_min', y2='left_knee_flexion_max', source=source,
                  fill_alpha=0.5, fill_color='#6495ED', legend_label="Range of Motion")

    KneeFig2.line(x='index', y='right_knee_flexion_mean',
                 color='#00FF00', legend_label='Right (Mean)',
                 source=source, muted_alpha=0.1, name='right_knee_flexion_mean')
    KneeFig2.line(x='index', y='left_knee_flexion_mean',
                 color='#0000FF' , legend_label='Left (Mean)',
                 source=source, muted_alpha=0.1, name='left_knee_flexion_mean')
    KneeFig2.varea(x='index', y1='right_knee_flexion_min', y2='right_knee_flexion_max', source=source,
                  fill_alpha=0.5, fill_color='chartreuse', legend_label="Range of Motion")

    KneeVVFig.line(x='index', y='left_knee_varus_mean',
                   color='#001BFF', legend_label='Left (Mean)',
                   source=source, muted_alpha=0.1, name='left_knee_varus_mean')
    KneeVVFig.varea(x='index', y1='left_knee_varus_min', y2='left_knee_varus_max', source=source,
                  fill_alpha=0.5, fill_color='#6495ED', legend_label="Range of Motion")
    KneeVVFig2.line(x='index', y='right_knee_varus_mean', muted=False,
                   color='#00FF00', legend_label='Right (Mean)',
                   source=source, muted_alpha=0.1, name='right_knee_varus_mean')
    KneeVVFig2.varea(x='index', y1='right_knee_varus_min', y2='right_knee_varus_max', source=source,
                  fill_alpha=0.5, fill_color='chartreuse', legend_label="Range of Motion")

    HipFig.line(x='index', y='left_hip_abduction_mean',
                color='#001BFF', legend_label='Left (Mean)',
                source=source, muted_alpha=0.1, name='left_hip_abduction_mean')
    HipFig.varea(x='index', y1='left_hip_abduction_min', y2='left_hip_abduction_max', source=source,
                  fill_alpha=0.5, fill_color='#6495ED', legend_label="Range of Motion")
    HipFig2.line(x='index', y='right_hip_abduction_mean',
                color='#00FF00', legend_label='Right (Mean)', muted=False,
                source=source, muted_alpha=0.1, name='right_hip_abduction_mean')
    HipFig2.varea(x='index', y1='right_hip_abduction_min', y2='right_hip_abduction_max', source=source,
                  fill_alpha=0.5, fill_color='chartreuse', legend_label="Range of Motion")

    ElbowFig.line(x='index', y='left_elbow_flexion_mean',
                  color='#001BFF', legend_label='Left (Mean)',
                  source=source, muted_alpha=0.1, name='left_elbow_flexion_mean')
    ElbowFig.varea(x='index', y1='left_elbow_flexion_min', y2='left_elbow_flexion_max', source=source,
                  fill_alpha=0.5, fill_color='#6495ED', legend_label="Range of Motion")
    ElbowFig2.line(x='index', y='right_elbow_flexion_mean',
                  color='#00FF00', legend_label='Right (Mean)', muted=False,
                  source=source, muted_alpha=0.1, name='right_elbow_flexion_mean')
    ElbowFig2.varea(x='index', y1='right_elbow_flexion_min', y2='right_elbow_flexion_max', source=source,
                  fill_alpha=0.5, fill_color='chartreuse', legend_label="Range of Motion")

    ArmFig.line(x='index', y='left_arm_abduction_mean',
                color='#001BFF', legend_label='Left (Mean)',
                source=source, muted_alpha=0.1, name='left_arm_abduction_mean')
    ArmFig.varea(x='index', y1='left_arm_abduction_min', y2='left_arm_abduction_max', source=source,
                  fill_alpha=0.5, fill_color='#6495ED', legend_label="Range of Motion")
    ArmFig2.line(x='index', y='right_arm_abduction_mean',
                color='#00FF00', legend_label='Right (Mean)', muted=False,
                source=source, muted_alpha=0.1, name='right_arm_abduction_mean')
    ArmFig2.varea(x='index', y1='right_arm_abduction_min', y2='right_arm_abduction_max', source=source,
                  fill_alpha=0.5, fill_color='chartreuse', legend_label="Range of Motion")

    HeadAngleFig.line(x='index', y='head_angle_new_mean',
                      color='#001BFF', legend_label='Head Angle (Mean)',
                      source=source, muted_alpha=0.1, name='head_angle_new_mean')
    HeadAngleFig.varea(x='index', y1='head_angle_new_min', y2='head_angle_new_max', source=source,
                  fill_alpha=0.5, fill_color='chartreuse', legend_label="Range of Motion")

    ShoulderAngleFig.line(x='index', y='shoulder_angle_new_mean',
                          color='#001BFF', legend_label='Shoulder Angle (Mean)',
                          source=source, muted_alpha=0.1, name='shoulder_angle_new_mean')
    ShoulderAngleFig.varea(x='index', y1='shoulder_angle_new_min', y2='shoulder_angle_new_max', source=source,
                  fill_alpha=0.5, fill_color='chartreuse', legend_label="Range of Motion")

    SpineArcFig.line(x='index', y='spine_arc_mean',
                     color='#001BFF', legend_label='Spine Arc (Mean)',
                     source=source, muted_alpha=0.1, name='spine_arc_mean')
    SpineArcFig.varea(x='index', y1='spine_arc_min', y2='spine_arc_max', source=source,
                  fill_alpha=0.5, fill_color='chartreuse', legend_label="Range of Motion")

    PelvisFlexFig.line(x='index', y='pelvis_flexion_mean',
                       color='#001BFF', legend_label='Pelvis Flexion (Mean)',
                       source=source, muted_alpha=0.1, name='pelvis_flexion_mean')
    PelvisFlexFig.varea(x='index', y1='pelvis_flexion_min', y2='pelvis_flexion_max', source=source,
                  fill_alpha=0.5, fill_color='chartreuse', legend_label="Range of Motion")

    KneeFig.legend.location = 'top_left'
    KneeVVFig.legend.location = 'top_left'
    HipFig.legend.location = 'top_left'
    ElbowFig.legend.location = 'top_left'
    ArmFig.legend.location = 'top_left'
    HeadAngleFig.legend.location = 'top_left'
    ShoulderAngleFig.legend.location = 'top_left'
    SpineArcFig.legend.location = 'top_left'
    PelvisFlexFig.legend.location = 'top_left'

    KneeFig.legend.click_policy = 'hide'
    KneeVVFig.legend.click_policy = 'hide'
    HipFig.legend.click_policy = 'hide'
    ElbowFig.legend.click_policy = 'hide'
    ArmFig.legend.click_policy = 'hide'
    HeadAngleFig.legend.click_policy = 'hide'
    ShoulderAngleFig.legend.click_policy = 'hide'
    SpineArcFig.legend.click_policy = 'hide'

    KneeFig2.legend.location = 'top_left'
    KneeVVFig2.legend.location = 'top_left'
    HipFig2.legend.location = 'top_left'
    ElbowFig2.legend.location = 'top_left'
    ArmFig2.legend.location = 'top_left'
    HeadAngleFig2.legend.location = 'top_left'
    ShoulderAngleFig2.legend.location = 'top_left'
    SpineArcFig2.legend.location = 'top_left'
    PelvisFlexFig2.legend.location = 'top_left'

    KneeFig2.legend.click_policy = 'hide'
    KneeVVFig2.legend.click_policy = 'hide'
    HipFig2.legend.click_policy = 'hide'
    ElbowFig2.legend.click_policy = 'hide'
    ArmFig2.legend.click_policy = 'hide'
    HeadAngleFig2.legend.click_policy = 'hide'
    ShoulderAngleFig2.legend.click_policy = 'hide'
    SpineArcFig2.legend.click_policy = 'hide'


file_input1.on_change('value', upload_data1)

#data_table = DataTable(source=source, columns=columns, width=1600, height=300)
# curdoc().theme = 'dark_minimal'

curdoc().add_root(column(file_input1, row(children=[column(left_tabs), column(right_tabs), column(middle_tabs)])))

#curdoc().add_root(row(children=[column(file_input1), column(left_tabs), column(right_tabs), column(middle_tabs)]))

# Determine where the visualization will be rendered
# output_file('filename.html', title='Patient Biomechanics')  # Render to static HTML, or
# output_notebook()  # Render inline in a Jupyter Notebook


# Widget
