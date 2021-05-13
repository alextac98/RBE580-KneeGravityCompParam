#!/usr/bin/env python
from Vicon.Mocap import Vicon

from GaitCore.Core.PointArray import PointArray
from GaitCore.Core import Point

from Vicon.Tools.AnimateModel import AnimateModel

import numpy as np
from scipy.optimize import curve_fit

import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D as plot3d
import matplotlib.animation as animation

import json

animate_points = True
plot_knee_angles = False
plot_knee_angle_torque = False

def parse_data():
    l_knee_data = {
        "l_knee_angle": [],
        "l_knee_force": [],
        "l_knee_moment": [],
        "l_knee_power": []
    }

    for subject in range(0, 11):
        for trial in range(0, 3):
            print(f"Looking at: subject_{subject:02d}_walk_{trial:02d}")
            file_name = f"_GaitData/Gaiting_stairs/subject_{subject:02d}/subject_{subject:02d}_walk_{trial:02d}.csv"
            try:
                data = Vicon.Vicon(file_name, interpolate=False)
                l_knee_data.get("l_knee_angle").append(data.data_dict.get('Model Outputs').get('LKneeAngles'))
                l_knee_data.get("l_knee_force").append(data.data_dict.get('Model Outputs').get('LKneeForce'))
                l_knee_data.get("l_knee_moment").append(data.data_dict.get('Model Outputs').get('LKneeMoment'))
                l_knee_data.get("l_knee_power").append(data.data_dict.get('Model Outputs').get('LKneePower'))
            except OSError as e:
                print(e)
                continue
            
    with open('mocap-data/l_knee_data.json', 'w') as outfile:
        json.dump(l_knee_data, outfile)

if __name__ == '__main__':

    # parse_data()

    # l_knee_data = {}
    # with open('mocap-data/l_knee_data.json', 'r') as file:
    #     l_knee_data = json.load(file)

    # l_knee_angle = {'X': {'data': []},
    #                 'Y': {'data': []},
    #                 'Z': {'data': []}}

    # for i in range(0, len(l_knee_data.get('l_knee_angle')[0].get('X').get('data'))):
    #     size = len(l_knee_data.get('l_knee_angle'))
    #     l_knee_angle_x_sum = 0
    #     l_knee_angle_y_sum = 0
    #     l_knee_angle_z_sum = 0
    #     for j in range(0, size):
    #         l_knee_angle_x_sum += l_knee_data.get('l_knee_angle')[j].get('X').get('data')[i]
    #         l_knee_angle_y_sum += l_knee_data.get('l_knee_angle')[j].get('Y').get('data')[i]
    #         l_knee_angle_z_sum += l_knee_data.get('l_knee_angle')[j].get('Z').get('data')[i]

    #     l_knee_angle.get('X').get('data').append(l_knee_angle_x_sum/size)
    #     l_knee_angle.get('Y').get('data').append(l_knee_angle_y_sum/size)
    #     l_knee_angle.get('Z').get('data').append(l_knee_angle_z_sum/size)
    

    # data = Vicon.Vicon("mocap-data/s0_walk.csv", interpolate=False)
    # data = Vicon.Vicon("_GaitData/Gaiting_stairs/subject_00/subject_00 stairconfig1_00.csv", interpolate=False)
    data = Vicon.Vicon("mocap-data/data/Walking06.csv", interpolate=False)
    # data = Vicon.Vicon("_GaitData/Gaiting_stairs/subject_00/subject_00_walk_00.csv", interpolate=False)

    knee_l_data = data._joint_objs.get('L_Femur_L_Tibia')
    l_knee_angle = data.data_dict.get('Model Outputs').get('LKneeAngles')
    l_knee_force = data.data_dict.get('Model Outputs').get('LKneeForce')
    l_knee_moment = data.data_dict.get('Model Outputs').get('LKneeMoment')
    l_knee_power = data.data_dict.get('Model Outputs').get('LKneePower')

    # l_knee_angle = []
    # l_knee_force = []
    # l_knee_moment = []
    # l_knee_power = []

    # # Low Pass Filter
    # filter_threshold = 50
    # for i in range(0, len(l_knee_angle_raw)):
    #     if l_knee_moment_raw[i] > filter_threshold:
    #         l_knee_angle.append(l_knee_angle_raw[i])
    #         l_knee_force.append(l_knee_force_raw[i])
    #         l_knee_moment.append(l_knee_moment_raw[i])
    #         l_knee_power.append(l_knee_power_raw[i])
            

    # ----- Plot Knee Angles ----- #
    if plot_knee_angles:
        knee_angle_x = l_knee_angle.get('X').get('data')
        knee_angle_y = l_knee_angle.get('Y').get('data')
        knee_angle_z = l_knee_angle.get('Z').get('data')
        knee_torque_x = l_knee_moment.get('X').get('data')
        knee_torque_y = l_knee_moment.get('Y').get('data')
        knee_torque_z = l_knee_moment.get('Z').get('data')

        knee_angles_fig = plot.figure()
        knee_angle_x_plot = knee_angles_fig.add_subplot(321)
        knee_angle_x_plot.plot(knee_angle_x)
        knee_angle_x_plot.set_title('Knee Angle X')

        knee_angle_y_plot = knee_angles_fig.add_subplot(323)
        knee_angle_y_plot.plot(knee_angle_y)
        knee_angle_y_plot.set_title('Knee Angle Y')

        knee_angle_z_plot = knee_angles_fig.add_subplot(325)
        knee_angle_z_plot.plot(knee_angle_z)
        knee_angle_z_plot.set_title('Knee Angle Z')
        
        knee_torque_x_plot = knee_angles_fig.add_subplot(322)
        knee_torque_x_plot.plot(knee_torque_x)

        knee_torque_y_plot = knee_angles_fig.add_subplot(324)
        knee_torque_y_plot.plot(knee_torque_y)

        knee_torque_z_plot = knee_angles_fig.add_subplot(326)
        knee_torque_z_plot.plot(knee_torque_z)


        # plot.show()

    # ----- Plot Angle vs Torque ----- #
    if plot_knee_angle_torque:
        knee_angle_x = l_knee_angle.get('X').get('data')
        knee_angle_y = l_knee_angle.get('Y').get('data')
        knee_angle_z = l_knee_angle.get('Z').get('data')

        knee_moment_x = l_knee_moment.get('X').get('data')
        # knee_moment_x_abs = [abs(e) for e in knee_moment_x]
        knee_moment_y = l_knee_moment.get('Y').get('data')
        # knee_moment_y_abs = [abs(e) for e in knee_moment_y]
        knee_moment_z = l_knee_moment.get('Z').get('data')
        # knee_moment_z_abs = [abs(e) for e in knee_moment_z]

        # Low Pass filter:
        knee_angle_x_filtered = []
        knee_moment_x_filtered = []

        lpf_threshold = -1
        for i in range(len(knee_angle_x)):
            if abs(knee_moment_x[i]) > lpf_threshold:
                knee_angle_x_filtered.append(knee_angle_x[i])
                knee_moment_x_filtered.append(knee_moment_x[i])

        best_fit = np.poly1d(np.polyfit(knee_angle_x_filtered, knee_moment_x_filtered, 5))
        best_fit_x = np.linspace(min(knee_angle_x_filtered), max(knee_angle_x_filtered), num=70)
        best_fit_y = best_fit(best_fit_x)

        knee_angle_moment_plot = plot.figure()

        knee_angle_moment_x_plot = knee_angle_moment_plot.add_subplot(111)

        knee_angle_moment_x_plot.plot(best_fit_x, best_fit_y, color='r')

        knee_angle_moment_x_plot.scatter(knee_angle_x_filtered, knee_moment_x_filtered, marker='.')
        knee_angle_moment_x_plot.set_title('Knee Moment vs Angle during Walking')
        knee_angle_moment_x_plot.set_xlabel('Angle [deg]')
        knee_angle_moment_x_plot.set_ylabel('Moment [N.mm/kg]')

        # knee_angle_moment_y_plot = knee_angle_moment_plot.add_subplot(312)
        # knee_angle_moment_y_plot.scatter(knee_angle_y, knee_moment_y_abs)
        # knee_angle_moment_y_plot.set_title('Knee Moment vs Angle Y')
        # knee_angle_moment_y_plot.set_xlabel('Angle [deg]')
        # knee_angle_moment_y_plot.set_ylabel('Moment [N.mm/kg]')

        # knee_angle_moment_z_plot = knee_angle_moment_plot.add_subplot(313)
        # knee_angle_moment_z_plot.scatter(knee_angle_z, knee_moment_z_abs)
        # knee_angle_moment_z_plot.set_title('Knee Moment vs Angle Z')
        # knee_angle_moment_z_plot.set_xlabel('Angle [deg]')
        # knee_angle_moment_z_plot.set_ylabel('Moment [N.mm/kg]')

    plot.show()


    # ----- 3D Animation of points ---- #
    if animate_points:
        animation = AnimateModel(x_limit=(-1200, 1200), y_limit=(-1200, 1200), z_limit=(0, 1200))
        animation.import_markers(data.data_dict.get('Trajectories'))
        animation.draw()
  
    print("Done!")
