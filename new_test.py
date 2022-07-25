from functions_ import *
import io
import base64
from bokeh.io import curdoc, export_png
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, DataTable, TableColumn, HoverTool
from bokeh.layouts import column, row, gridplot, layout
from bokeh.models.widgets import Tabs, Panel, FileInput
from fpdf import FPDF
import more_itertools
from datetime import datetime
from statistics import mean


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

def get_mean_df(input_list):

    input_1 = input_list[0]
    input_2 = input_list[1]
    input_3 = input_list[2]
    input_4 = None
    input_5 = None
    if len(input_list) >= 4:
        input_4 = input_list[3]
    if len(input_list) == 5:
        input_5 = input_list[4]
    mean_dict = {}
    min_dict = {}
    max_dict = {}
    column_names = input_list[0].columns.values.tolist()
    column_names_merged = []
    merged = {}
    for i in range(len(column_names)):
        column_names_merged.insert(i, str(column_names[i]) + "_merged")

    for j in column_names:
        dictionary_knee_flexion = {'a': input_1[j], 'b': input_2[j], 'c': input_3[j]}
        if input_4 is not None:
            dictionary_knee_flexion['d'] = input_4[j]
        if input_5 is not None:
            dictionary_knee_flexion['e'] = input_5[j]
        mean_tmp = {j + "_mean": [mean(values) for values in zip(*dictionary_knee_flexion.values())]}
        min_tmp = {j + "_min": [min(values) for values in zip(*dictionary_knee_flexion.values())]}
        max_tmp = {j + "_max": [max(values) for values in zip(*dictionary_knee_flexion.values())]}
        merged.update(mean_tmp)
        merged.update(min_tmp)
        merged.update(max_tmp)
    merged_df = pd.DataFrame(merged)
    merged_df = merged_df.apply(lambda x: savgol_filter(x, 5, 1))
    return merged_df

def work_done(input, biomechanic, lb=None, ub=None):
    data = input
    if lb and ub is not None:
        work_done = np.trapz(data[biomechanic][lb:ub])
    else:
        work_done = np.trapz(data[biomechanic])
    return work_done

parser = argparse.ArgumentParser(description="Read file form Command line.")
parser.add_argument("-p", "--pid", dest="pid", required=True, help="patient id", metavar="FILE")
parser.add_argument("-a", "--action", dest="action", required=True, help="desired action", metavar="FILE")
args = parser.parse_args()


file_list = {}
index = 0
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".pkl"):
        if filename.startswith(args.pid):
            if args.action in filename:
                file_list[index] = filename
                index += 1
biomechanics_list = []
for i in file_list.items():
    biomechanics_df = create_dataset_SMPL(joints_from_smpl(joblib.load(i[1])))
    biomechanics_df = biomechanics_df.apply(lambda x: savgol_filter(x, 5, 1))
    biomechanics_list.append(biomechanics_df)

biomechanics_df = get_mean_df(biomechanics_list)

#print(biomechanics_list)

#print(biomechanics_df)




source = ColumnDataSource(biomechanics_df)
columns = [TableColumn(field=col, title=col) for col in biomechanics_df.columns]

# Create Figures
"""
Always show 0 for Flexion/Extension Graph
Annotate Graph with which areas are Flexion and which areas are Extension

"""
KneeFig = figure(
    title='Knee Flexion',
    plot_height=720, plot_width=1280,
    x_axis_label='Frame',
    y_axis_label='Flexion (degrees)',
    toolbar_location='below')
    #y_range=(-10,100)
    #sizing_mode= "scale_both")
KneeFig.yaxis.axis_label_standoff=15
KneeFig.yaxis.axis_label_text_font_size="15pt"
KneeFig.xaxis.axis_label_text_font_size="15pt"
KneeFig.yaxis.major_label_text_font_size="15pt"
KneeVVFig = figure(
    title='Knee Varus/Valgus',
    plot_height=720, plot_width=1280,
    x_axis_label='Frame',
    y_axis_label='Varus/Valgus (degrees)',
    toolbar_location='below')
    #sizing_mode= "scale_both")

HipFig = figure(
    title='Hip Abduction',
    plot_height=720, plot_width=1280,
    x_axis_label='Frame',
    y_axis_label='Abduction (degrees)',
    toolbar_location='below')
    #sizing_mode="scale_both")

ElbowFig = figure(
    title='Elbow Flexion',
    plot_height=720, plot_width=1280,
    x_axis_label='Frame',
    y_axis_label='Flexion (degrees)',
    toolbar_location='below')
    #sizing_mode="scale_both")

ArmFig = figure(
    title='Arm Abduction',
    plot_height=720, plot_width=1280,
    x_axis_label='Frame',
    y_axis_label='Abduction (degrees)',
    toolbar_location='below')
    #sizing_mode="scale_both")

HeadAngleFig = figure(
    title='Head Tilt',
    plot_height=720, plot_width=1280,
    x_axis_label='Frame',
    y_axis_label='Tilt (degrees)',
    toolbar_location='below')
    #sizing_mode="scale_both")

ShoulderAngleFig = figure(
    title='Shoulder Tilt',
    plot_height=720, plot_width=1280,
    x_axis_label='Frame',
    y_axis_label='Tilt (degrees)',
    toolbar_location='below')
    #sizing_mode="scale_both")

SpineArcFig = figure(
    title='Spine Arc',
    plot_height=720, plot_width=1280,
    x_axis_label='Frame',
    y_axis_label='Spine Arc (degrees)',
    toolbar_location='below')
    #sizing_mode="scale_both")

PelvisFlexFig = figure(
    title='Pelvis Flexion',
    plot_height=720, plot_width=1280,
    x_axis_label='Frame',
    y_axis_label='Pelvis Flexion (degrees)',
    toolbar_location='below')
    #sizing_mode="scale_both")

biomechanics_df.index.rename('Frame')
biomechanics_df['index'] = biomechanics_df.index
biomechanics_df = biomechanics_df[['index'] + [col for col in biomechanics_df.columns if col != 'index']]
source.data = biomechanics_df
#data_table.columns = [TableColumn(field=col, title=col) for col in df.columns]

KneeFig.line(x='index', y='left_knee_flexion_mean', line_width=5,
             color='#0000FF' , legend_label='Left (Mean)',
             source=source, muted_alpha=0.1, name='left_knee_flexion_mean')
KneeFig.line(x='index', y='right_knee_flexion_mean', line_width=5,
             color='#006400', legend_label='Right (Mean)',
             source=source, muted_alpha=0.1, name='left_knee_flexion_mean')
KneeFig.varea(x='index', y1='left_knee_flexion_min', y2='left_knee_flexion_max', source=source,
              fill_alpha=0.35, fill_color='#6495ED', legend_label="Range of Motion")
KneeFig.varea(x='index', y1='right_knee_flexion_min', y2='right_knee_flexion_max', source=source,
              fill_alpha=0.35, fill_color='#FFD700', legend_label="Range of Motion")

KneeVVFig.line(x='index', y='left_knee_varus_mean', line_width=5,
               color='#001BFF', legend_label='Left (Mean)',
               source=source, muted_alpha=0.1, name='left_knee_varus_mean')
KneeVVFig.varea(x='index', y1='left_knee_varus_min', y2='left_knee_varus_max', source=source,
              fill_alpha=0.35, fill_color='#6495ED', legend_label="Range of Motion")
KneeVVFig.line(x='index', y='right_knee_varus_mean', muted=False, line_width=5,
               color='#006400', legend_label='Right (Mean)',
               source=source, muted_alpha=0.1, name='right_knee_varus_mean')
KneeVVFig.varea(x='index', y1='right_knee_varus_min', y2='right_knee_varus_max', source=source,
              fill_alpha=0.35, fill_color='#FFD700', legend_label="Range of Motion")

HipFig.line(x='index', y='left_hip_abduction_mean', line_width=5,
            color='#001BFF', legend_label='Left (Mean)',
            source=source, muted_alpha=0.1, name='left_hip_abduction_mean')
HipFig.varea(x='index', y1='left_hip_abduction_min', y2='left_hip_abduction_max', source=source,
              fill_alpha=0.35, fill_color='#6495ED', legend_label="Range of Motion")
HipFig.line(x='index', y='right_hip_abduction_mean', line_width=5,
            color='#006400', legend_label='Right (Mean)', muted=False,
            source=source, muted_alpha=0.1, name='right_hip_abduction_mean')
HipFig.varea(x='index', y1='right_hip_abduction_min', y2='right_hip_abduction_max', source=source,
              fill_alpha=0.35, fill_color='#FFD700', legend_label="Range of Motion")

ElbowFig.line(x='index', y='left_elbow_flexion_mean', line_width=5,
              color='#001BFF', legend_label='Left (Mean)',
              source=source, muted_alpha=0.1, name='left_elbow_flexion_mean')
ElbowFig.varea(x='index', y1='left_elbow_flexion_min', y2='left_elbow_flexion_max', source=source,
              fill_alpha=0.35, fill_color='#6495ED', legend_label="Range of Motion")
ElbowFig.line(x='index', y='right_elbow_flexion_mean', line_width=5,
              color='#006400', legend_label='Right (Mean)', muted=False,
              source=source, muted_alpha=0.1, name='right_elbow_flexion_mean')
ElbowFig.varea(x='index', y1='right_elbow_flexion_min', y2='right_elbow_flexion_max', source=source,
              fill_alpha=0.35, fill_color='#FFD700', legend_label="Range of Motion")

ArmFig.line(x='index', y='left_arm_abduction_mean', line_width=5,
            color='#001BFF', legend_label='Left (Mean)',
            source=source, muted_alpha=0.1, name='left_arm_abduction_mean')
ArmFig.varea(x='index', y1='left_arm_abduction_min', y2='left_arm_abduction_max', source=source,
              fill_alpha=0.35, fill_color='#6495ED', legend_label="Range of Motion")
ArmFig.line(x='index', y='right_arm_abduction_mean', line_width=5,
            color='#006400', legend_label='Right (Mean)', muted=False,
            source=source, muted_alpha=0.1, name='right_arm_abduction_mean')
ArmFig.varea(x='index', y1='right_arm_abduction_min', y2='right_arm_abduction_max', source=source,
              fill_alpha=0.35, fill_color='#FFD700', legend_label="Range of Motion")

HeadAngleFig.line(x='index', y='head_angle_new_mean', line_width=5,
                  color='#001BFF', legend_label='Head Angle (Mean)',
                  source=source, muted_alpha=0.1, name='head_angle_new_mean')
HeadAngleFig.varea(x='index', y1='head_angle_new_min', y2='head_angle_new_max', source=source,
              fill_alpha=0.35, fill_color='#FFD700', legend_label="Range of Motion")

ShoulderAngleFig.line(x='index', y='shoulder_angle_new_mean', line_width=5,
                      color='#001BFF', legend_label='Shoulder Angle (Mean)',
                      source=source, muted_alpha=0.1, name='shoulder_angle_new_mean')
ShoulderAngleFig.varea(x='index', y1='shoulder_angle_new_min', y2='shoulder_angle_new_max', source=source,
              fill_alpha=0.35, fill_color='#FFD700', legend_label="Range of Motion")

SpineArcFig.line(x='index', y='spine_arc_mean', line_width=5,
                 color='#001BFF', legend_label='Spine Arc (Mean)',
                 source=source, muted_alpha=0.1, name='spine_arc_mean')
SpineArcFig.varea(x='index', y1='spine_arc_min', y2='spine_arc_max', source=source,
              fill_alpha=0.35, fill_color='#FFD700', legend_label="Range of Motion")

PelvisFlexFig.line(x='index', y='pelvis_flexion_mean', line_width=5,
                   color='#001BFF', legend_label='Pelvis Flexion (Mean)',
                   source=source, muted_alpha=0.1, name='pelvis_flexion_mean')
PelvisFlexFig.varea(x='index', y1='pelvis_flexion_min', y2='pelvis_flexion_max', source=source,
                    fill_alpha=0.35, fill_color='#FFD700', legend_label="Range of Motion")

export_png(KneeFig, filename="KneeFig.png", width=1280, height=720)
export_png(KneeVVFig, filename="KneeVVFig.png", width=1280, height=720)
export_png(HipFig, filename="HipFig.png", width=1280, height=720)
export_png(ElbowFig, filename="ElbowFig.png", width=1280, height=720)
export_png(ArmFig, filename="ArmFig.png", width=1280, height=720)
export_png(PelvisFlexFig, filename="PelvisFlexFig.png", width=1280, height=720)
export_png(SpineArcFig, filename="SpineArcFig.png", width=1280, height=720)
export_png(HeadAngleFig, filename="HeadAngleFig.png", width=1280, height=720)

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('mskdoctors.png', 10, 8, 50)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        #self.cell(80)
        # Title
        self.text(70, 15, 'Biomechanics Report')
        #self.ln(10)
        #self.cell(60)
        self.text(70, 25, args.pid)
        # Line break
        #self.ln(50)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.text(190, 290, 'Page ' + str(self.page_no()))
        self.text(5, 290, 'Report generated: ' + str(datetime.today().strftime('%d-%m-%Y')))

l_f_wd = work_done(biomechanics_df, 'left_knee_flexion_mean')
r_f_wd = work_done(biomechanics_df, 'right_knee_flexion_mean')
l_f_rom = max(biomechanics_df['left_knee_flexion_mean']) - min(biomechanics_df['left_knee_flexion_mean'])
r_f_rom = max(biomechanics_df['right_knee_flexion_mean']) - min(biomechanics_df['right_knee_flexion_mean'])
vv_alignment = None
if mean(biomechanics_df['left_knee_varus_mean'][:100]) and mean(biomechanics_df['right_knee_varus_mean']) < 0:
    vv_alignment = "Valgus"
elif mean(biomechanics_df['left_knee_varus_mean'][:100]) and mean(biomechanics_df['right_knee_varus_mean']) > 0:
    vv_alignment = "Varus"
l_ext = None
r_ext = None
if min(biomechanics_df['left_knee_flexion_mean']) > 0:
    l_ext = "The left knee never goes to true extension"
if min(biomechanics_df['right_knee_flexion_mean']) > 0:
    r_ext = "the right knee never goes to true extension"

# Instantiation of inherited class
pdf = PDF()
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_font('Times', '', 10)
pdf.image("KneeFig.png", x= 40, y=40,  link='', type='', w=120, h=90)
pdf.text(30, 135, "Knee Flexion shows the left knee work done is: {0:0.2f} and right knee of: {1:0.2f}".format(l_f_wd, r_f_wd))
if l_f_wd > r_f_wd:
    pdf.text(30,140, "this shows that there is a difference of {0:0.2f} favouring the left side".format(l_f_wd-r_f_wd))
elif r_f_wd > l_f_wd:
    pdf.text(30,140, "this shows that there is a difference of {0:0.2f} favouring the left side".format(r_f_wd-l_f_wd))
pdf.text(30,145, "The average range of motion on the left side is: {0:0.2f}° and right side: {1:0.2f}°".format(l_f_rom, r_f_rom))
if l_f_wd > r_f_wd:
    pdf.text(30,150, "this shows that there is a difference of {0:0.2f}° favouring the left side".format(l_f_rom-r_f_rom))
elif r_f_wd > l_f_wd:
    pdf.text(30,150, "this shows that there is a difference of {0:0.2f}° favouring the left side".format(r_f_rom-l_f_rom))
if l_ext is not None and r_ext is not None:
    pdf.text(30,155, "{0} and {1}.".format(l_ext, r_ext))

pdf.image("KneeVVFig.png", x= 40, y=160,  link='', type='', w=120, h=90)
pdf.text(30, 260, "Knee Varus/Valgus shows a natrual {0} alignment".format(vv_alignment))
pdf.add_page()
pdf.image("HipFig.png", x= 40, y=40,  link='', type='', w=120, h=90)
pdf.text(30, 140, "Hip Abduction shows...")
pdf.image("PelvisFlexFig.png", x= 40, y=160,  link='', type='', w=120, h=90)
pdf.text(30, 260, "Pelvis Flexion shows...")
#for i in range(1, 41):
    #pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)
pdf.output('{0}_{1}.pdf'.format(args.pid, args.action), 'F')



os.remove("KneeFig.png")
os.remove("KneeVVFig.png")
os.remove("ElbowFig.png")
os.remove("HipFig.png")
os.remove("ArmFig.png")
os.remove("PelvisFlexFig.png")
os.remove("SpineArcFig.png")
os.remove("HeadAngleFig.png")



