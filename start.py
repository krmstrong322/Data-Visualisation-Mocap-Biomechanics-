import time
from matplotlib import pyplot as plt
import matplotlib
import multiprocessing as mp
from multiprocessing import shared_memory
import ctypes
import numpy as np
from pycpd import AffineRegistration
import scipy
import cv2
from cppyy import add_include_path, load_library, include, gbl, addressof, add_library_path
import threading
import os
from os.path import exists,join
from concurrent.futures import ThreadPoolExecutor
from pyk4a import PyK4A
from helpers import colorize
from pyk4a import Config, PyK4A

dirname = time.strftime("%d%m%y-%H%M%S")  # Create Data Directory by name of "%d%m%y-%H%M%S"
if not exists(dirname):
    os.mkdir(dirname)


def get_tracker(device, config, tracker_config):
    calibration = device.get_calibration(config.depth_mode, config.color_resolution)
    return gbl.k4abt.tracker.create(calibration, tracker_config)

def get_skeletons(trackers,captures):
    total_num_bodies=[]  # shape(2) [number of bodies main camera, number of bodies sub camera]
    bodies_joints_xyz_conf=[]  # N: total number of bodies from two camera, 32 joints, xyz+confidence shape(N,32,4)
    body_ids=[]   # id generated from tracker, shape(N)
    cv_images=[]
    cv_images_time=[]
    depth_imgs=[]
    depth_imgs_time=[]
    ir_imgs=[]
    ir_imgs_time=[]
    for i in range(0,2):
        trackers[i].enqueue_capture(captures[i],-1)
        frame=trackers[i].pop_result(-1)

        num_bodies=frame.get_num_bodies()
        capture = frame.get_capture()

        c_image=capture.get_color_image()
        cv_images_time.append(c_image.get_device_timestamp().count())
        c_image_size=4 * c_image.get_height_pixels() * c_image.get_width_pixels()
        b_c_image=c_image.get_buffer()
        b_c_image.reshape((4 * c_image.get_height_pixels() * c_image.get_width_pixels(),))
        np_c_buf = np.frombuffer(b_c_image, dtype=np.uint8, count=c_image_size)
        cv_image = np_c_buf.reshape(c_image.get_height_pixels(), c_image.get_width_pixels(), 4)[:, :, :3]
        cv_images.append(cv_image)

        d_image=capture.get_depth_image()
        depth_imgs_time.append(d_image.get_device_timestamp().count())
        d_image_size= d_image.get_height_pixels() * d_image.get_width_pixels()
        b_d_image = d_image.get_buffer()
        b_d_image.reshape((2*d_image.get_height_pixels() * d_image.get_width_pixels(),))
        np_d_buf = np.frombuffer(b_d_image, dtype=np.uint16, count=d_image_size)
        depth_img = np_d_buf.reshape(d_image.get_height_pixels(), d_image.get_width_pixels())
        depth_imgs.append(depth_img)


        ir_image=capture.get_ir_image()
        ir_imgs_time.append(ir_image.get_device_timestamp().count())
        ir_image_size= ir_image.get_height_pixels() * ir_image.get_width_pixels()
        b_ir_image = ir_image.get_buffer()

        b_ir_image.reshape((2*ir_image.get_height_pixels() * ir_image.get_width_pixels(),))
        np_ir_buf = np.frombuffer(b_ir_image, dtype=np.uint16, count=ir_image_size)
        ir_img = np_ir_buf.reshape(ir_image.get_height_pixels(), ir_image.get_width_pixels())
        ir_imgs.append(ir_img)


        total_num_bodies.append(num_bodies)

        for j in range(0,num_bodies):
            body_id=frame.get_body_id(j)
            body_ids.append(body_id)
            body_skeleton=frame.get_body_skeleton(j)
            joints_xyz_conf=[] # (32,4)

            for joint in body_skeleton.joints:
                joints_xyz_conf.append([joint.position.xyz.x,joint.position.xyz.y,joint.position.xyz.z,joint.confidence_level])
            bodies_joints_xyz_conf.append(joints_xyz_conf)

    bodies_joints_xyz_conf = np.array(bodies_joints_xyz_conf,dtype=np.float16)
    return bodies_joints_xyz_conf,body_ids,total_num_bodies,cv_images,depth_imgs,ir_imgs,cv_images_time,depth_imgs_time,ir_imgs_time

add_include_path(r'C:\Program Files\Azure Kinect Body Tracking SDK\sdk\include')    # Use Windows
add_include_path(r'C:\Program Files\Azure Kinect SDK v1.4.1\sdk\include')    # Use Windows, Make sure verison is correct
add_library_path(r'C:\Program Files\Azure Kinect Body Tracking SDK\sdk\windows-desktop\amd64\release\bin')   # Use Windows
add_library_path(r'C:\Program Files\Azure Kinect SDK v1.4.1\sdk\windows-desktop\amd64\release\bin')  # Use Windows, Make sure verison is correct

load_library('k4a')  # Use cppyy to import cpp liberary and include files
load_library('k4abt')
include('k4a/k4a.hpp')
include('k4abt.hpp')
include('main.cpp')  # Config settings.

color_exposure_usec = 10000  # Change RGB exposure time, higher value for brighter.
device_indices = [1]  # Define the device to use
powerline_freq = 1  # 1 for 50Hz, UK standard, do not change.

# Get the next capture (blocking function)

def main():
    k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.OFF,
            depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
            synchronized_images_only=False,
        )
    )
    k4a.start()

    k4a.whitebalance = 4500
    assert k4a.whitebalance == 4500
    k4a.whitebalance = 4510
    assert k4a.whitebalance == 4510

    while True:
        capture = k4a.get_capture()
        if np.any(capture.depth):
            cv2.imshow("k4a", colorize(capture.depth, (None, 5000), cv2.COLORMAP_HSV))
            key = cv2.waitKey(10)
            if key != -1:
                cv2.destroyAllWindows()
                break
    k4a.stop()


if __name__ == "__main__":
    main()