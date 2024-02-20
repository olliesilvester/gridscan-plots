import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
import argparse
import get_ideal_fgs_coords
"""Use with PandA PCAP produced h5py files which captures X over an exposure period, and its timestamp.
    Also plot X vs Y and compare to X vs Y coords. Assume INENC1 is x and INENC2 is y
"""

def get_y_coords(hz, y_name):
    #Get y-coords
    with h5.File(y_name) as y_data:
        return y_data['INENC1.VAL.Value'][()]
    

def get_x2_coords(hz, x_name):
    with h5.File(x_name) as x_data:
        return x_data['INENC3.VAL.Value'][()]

def get_coords(hz, x_data, y_data):
    y = get_y_coords(hz, y_data)
    x = get_x2_coords(hz, x_data)
    coords = []
    
    for i in range(len(y)):
        coords.append([x[i], y[i]])
    coords = np.array(coords)

    return coords


def get_mmm_coords(file):
    """Return min max mean data, as well as time between first and last trigger"""
    with h5.File(file) as data:
        
        all_data = {}
        
        all_data['x_mean'] = data['INENC1.VAL.Mean'][()]
        all_data['x_max'] = data['INENC1.VAL.Max'][()]
        all_data['x_min'] = data['INENC1.VAL.Min'][()]
        all_data['time_data'] = data['PCAP.TS_TRIG.Value'][()]   

        return all_data
    
def plot_x_against_time(data):
    plt.figure(1)
    plt.scatter(data['x_mean'], data['time_data'], label="Real data")
    plt.plot(data['x_mean'], data['time_data'])
    plt.xlabel('X (mm)')
    plt.ylabel('Time (s)')
    plt.title("X against time, real data")

def plot_ideal_coords(x_start=0, y_start=0):
    ideal_x_min, ideal_x_max, ideal_x_mean,ideal_y_mean = get_ideal_fgs_coords.get_mmm_coords(x_start, y_start) #enter starting x y positions as args here
    plt.figure(2)
    plt.scatter(ideal_x_mean, ideal_y_mean, label="Ideal data")
    plt.plot(ideal_x_mean, ideal_y_mean)
    plt.title("X against time, real data vs ideal data")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--x_start", default=0, type=float)
    parser.add_argument("--y_start", default=0, type=float)
    filename = parser.parse_args().filename
    x_start = parser.parse_args().x_start
    y_start = parser.parse_args().y_start
    data = get_mmm_coords(filename)
    plot_x_against_time(data)
    plot_ideal_coords(x_start, y_start)
    plt.legend()
    plt.show()

    # plt.scatter(data['x_mean'], data['time_data'], label="Real data")
    # plt.plot(data['x_mean'], data['time_data'], label="Real data")
    # plt.xlabel('X (mm)')
    # plt.ylabel('Time (s)')
    # plt.legend()
    # plt.show()
    
#arg name eg /dls/science/users/qqh35939/data_for_final_plots/flyscan-500hz-100-runup-mmm1.h5
    
        
    
    
    