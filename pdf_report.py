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
from statistics import mean

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

def get_mean_df(file1, file2, file3, file4=None, file5=None):
    mean_dict = {}
    min_dict = {}
    max_dict = {}

    df_1 = create_dataset_SMPL(joints_from_smpl(joblib.load(file1)))
    df_1 = df_1.apply(lambda x: savgol_filter(x, 5, 1))
    df_2 = create_dataset_SMPL(joints_from_smpl(joblib.load(file2)))
    df_2 = df_2.apply(lambda x: savgol_filter(x, 5, 1))
    df_3 = create_dataset_SMPL(joints_from_smpl(joblib.load(file3)))
    df_3 = df_3.apply(lambda x: savgol_filter(x, 5, 1))
    if file4 is not None:
        df_4 = create_dataset_SMPL(joints_from_smpl(joblib.load(file4)))
        df_4 = df_4.apply(lambda x: savgol_filter(x, 5, 1))
    if file5 is not None:
        df_5 = create_dataset_SMPL(joints_from_smpl(joblib.load(file5)))
        df_5 = df_5.apply(lambda x: savgol_filter(x, 5, 1))

    column_names = df_1.columns.values.tolist()
    column_names_merged = []
    merged = {}
    for i in range(len(column_names)):
        column_names_merged.insert(i, str(column_names[i]) + "_merged")

    for j in column_names:
        dictionary_knee_flexion = {'a': list(df_1[j]), 'b': list(df_2[j]), 'c': list(list(df_3[j]))}
        mean_tmp = {j + "_mean": [mean(values) for values in zip(*dictionary_knee_flexion.values())]}
        min_tmp = {j + "_min": [min(values) for values in zip(*dictionary_knee_flexion.values())]}
        max_tmp = {j + "_max": [max(values) for values in zip(*dictionary_knee_flexion.values())]}
        merged.update(mean_tmp)
        merged.update(min_tmp)
        merged.update(max_tmp)
    merged_df = pd.DataFrame(merged)
    merged_df = merged_df.apply(lambda x: savgol_filter(x, 5, 1))
    return merged_df

def work_done(input, biomechanic):
    data = input
    work_done = np.trapz(data[biomechanic])
    return work_done


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Read file form Command line.")
    parser.add_argument("-n", "--name", dest="name", required=True, help="input file",
                        metavar="FILE")
    args = parser.parse_args()
    """
    parser.add_argument("-i1", "--input1", dest="filename1", required=True, type=validate_file, help="input file",
                        metavar="FILE")
    parser.add_argument("-i2", "--input2", dest="filename2", required=True, type=validate_file, help="input file",
                        metavar="FILE")
    parser.add_argument("-i3", "--input3", dest="filename3", required=True, type=validate_file, help="input file",
                        metavar="FILE")
    parser.add_argument("-i4", "--input4", dest="filename4", required=False, type=validate_file, help="input file",
                        metavar="FILE")
    parser.add_argument("-i5", "--input5", dest="filename5", required=False, type=validate_file, help="input file",
                        metavar="FILE")
    parser.add_argument("-o", "--output", dest="output", required=False, default="out.csv", help="output file name")
    args = parser.parse_args()
    file_input_1 = args.filename1
    biomechanics1 = create_dataset_SMPL(joints_from_smpl(joblib.load(file_input_1)))
    file_input_2 = args.filename2
    biomechanics2 = create_dataset_SMPL(joints_from_smpl(joblib.load(file_input_2)))
    file_input_3 = args.filename3
    biomechanics3 = create_dataset_SMPL(joints_from_smpl(joblib.load(file_input_3)))

    if args.filename4 is not None:
        file_input_4 = args.filename4
        biomechanics4 = create_dataset_SMPL(joints_from_smpl(joblib.load(file_input_1)))

    if args.filename5 is not None:
        file_input_5 = args.filename5
        biomechanics5 = create_dataset_SMPL(joints_from_smpl(joblib.load(file_input_1)))

    if args.filename5 is not None and args.filename4 is not None:
        file_input_5 = args.filename5
        file_input_4 = args.filename4
        #get_mean_df(file_input_1, file_input_2, file_input_3, file_input_4, file_input_5).to_csv(args.output)
        df = get_mean_df(file_input_1, file_input_2, file_input_3, file_input_4, file_input_5)

    elif args.filename5 is None and args.filename4 is None:
        #get_mean_df(file_input_1, file_input_2, file_input_3).to_csv(args.output)
        df = get_mean_df(file_input_1, file_input_2, file_input_3)

    elif args.filename5 is None and args.filename4 is not None:
        #get_mean_df(file_input_1, file_input_2, file_input_3, file_input_4).to_csv(args.output)
        df = get_mean_df(file_input_1, file_input_2, file_input_3, file_input_4)

    source = ColumnDataSource(df)
    columns = [TableColumn(field=col, title=col) for col in df.columns]

    # Create Figures
    KneeFig = figure(
        title='Knee Flexion',
        plot_height=720, plot_width=1280,
        x_axis_label='Frame',
        y_axis_label='Flexion (degrees)',
        toolbar_location='below')
        #sizing_mode= "scale_both")

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

    df.index.rename('Frame')
    df['index'] = df.index
    df = df[['index'] + [col for col in df.columns if col != 'index']]
    source.data = df
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



    pdf = FPDF(orientation = 'P', unit = 'mm', format = 'A4')
    pdf.add_page()
    #pdf.set_font('helvetica', 10)
    #pdf.set_text_color(255, 255, 255)
    pdf.image('KneeFig.png', x = 0, y = 0, w = 120, h = 90)
    pdf.output('Automated PDF Report.pdf')
    #os.remove("KneeFig.png")
"""
    class PDF(FPDF):
        def header(self):
            # Logo
            self.image('mskdoctors.png', 10, 8, 50)
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Move to the right
            self.cell(80)
            # Title
            self.cell(30, 10, 'Biomechanics Report', 0, 0, 'C')
            self.ln(10)
            self.cell(63)
            self.cell(30, 10, args.name , 0, 0, 'C')
            # Line break
            self.ln(50)

        # Page footer
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Page number
            self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')



# Instantiation of inherited class
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    pdf.image("KneeFig.png", x= 40, y=40,  link='', type='', w=120, h=90)
    pdf.image("KneeVVFig.png", x= 40, y=160,  link='', type='', w=120, h=90)
    pdf.add_page()
    pdf.image("HipFig.png", x= 40, y=40,  link='', type='', w=120, h=90)
    pdf.image("ElbowFig.png", x= 40, y=160,  link='', type='', w=120, h=90)
    #for i in range(1, 41):
        #pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)
    pdf.output('tuto2.pdf', 'F')







