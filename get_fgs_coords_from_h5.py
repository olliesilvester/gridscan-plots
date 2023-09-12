import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
"""Read min/max/mean coordinate data or the instant coordinates. Also find the time between first and last trigger"""


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


def get_mmm_coords(hz, x_data, y_data):
    """Return min max mean data, as well as time between first and last trigger"""
    with h5.File(x_data) as data:
        
        
        x_mean = data['INENC3.VAL.Mean'][()]
        
        x_max = data['INENC3.VAL.Max'][()]
        x_min = data['INENC3.VAL.Min'][()]
        y_mean = data['INENC1.VAL.Mean'][()]
        y_max = data['INENC1.VAL.Max'][()]
        y_min = data['INENC1.VAL.Min'][()]
        overall_time= data['PCAP.TS_TRIG.Value'][()]
        overall_time = overall_time[-1] - overall_time[0]
        
        x_max = x_max - x_mean
        x_min = x_mean - x_min
        
        y_max = y_max - y_mean
        y_min = y_mean - y_min
        
        return x_min,x_max,x_mean,y_min,y_max,y_mean,overall_time
        
if __name__ == "__main__":
    coords = get_coords()
    plt.plot(coords[:, 0], coords[:, 1], label="Real data")
    plt.xlabel('X2 (mm)')
    plt.ylabel('Y (mm)')
    plt.legend()
    plt.show()
    
    
        
    
    
    