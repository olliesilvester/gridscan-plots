import get_fgs_coords_from_h5
import get_ideal_fgs_coords
import matplotlib.pyplot as plt
import numpy as np
    
"""Plot min/max/mean data, calculate standard deviation between ideal and real coodrinates"""
def plot_y_and_x2(hz, x_data, y_data, x_pos, y_pos, runup,scantype):
    ideal_x_min, ideal_x_max, ideal_x_mean,ideal_y_mean = get_ideal_fgs_coords.get_mmm_coords(x_pos, y_pos)
    real_x_min,real_x_max,real_x_mean,real_y_min,real_y_max,real_y_mean,time  = get_fgs_coords_from_h5.get_mmm_coords(hz, x_data, y_data)
    
    
    plt.figure(2)
    plt.scatter(real_x_mean, real_y_mean, label='Real')
    plt.scatter(ideal_x_mean, ideal_y_mean, label="ideal")
    
    x_diff = []
    y_diff = []
    
    #Plot arrows between the mean points of real and ideal and capture the standard deviation.
    for index,_ in enumerate(ideal_x_mean):
        if index == 689: #First data point is always naan for some reason, maybe bug with panda hdf
            break
        plt.arrow(ideal_x_mean[index], ideal_y_mean[index],real_x_mean[index+1]-ideal_x_mean[index],
                  real_y_mean[index+1]-ideal_y_mean[index], length_includes_head =True, head_starts_at_zero=True)
        plt.annotate("", xy=(0.5, 0.5), xytext=(0, 0),arrowprops=dict(arrowstyle="->"))
        x_diff.append(abs(ideal_x_mean[index]- real_x_mean[index+1]))
        y_diff.append(abs(ideal_y_mean[index]- real_y_mean[index+1]))
        
    x_diff = np.array(x_diff)
    y_diff = np.array(y_diff)
    
    stdv_x = np.std(x_diff)
    stdv_y = np.std(y_diff)

    plt.figtext(0.01, 0.01, f'Runup distance: {runup}mm.\
                Time taken: {round(time,4)}s.\
                Standard dev in x: {round(stdv_x,4)}mm.\
                Standard dev in y: {round(stdv_y,4)}mm', fontsize=12, color='blue')
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.title(f"{hz} hz {scantype}")
    plt.legend()
    
    #Do errorbar plot
    plt.figure(1)

    plt.errorbar(real_x_mean, real_y_mean, yerr=(real_y_min, real_y_max), xerr=(real_x_min,real_x_max), fmt='o', color="red", capsize=3,
                 label= "Real coordinates")
    plt.errorbar(ideal_x_mean, ideal_y_mean, xerr=(ideal_x_min,ideal_x_max), fmt='o', label="Demand coordinates", capsize=3, color='blue') #ideal
    plt.figtext(0.01, 0.01, f'Runup distance: {runup}mm.\
                Time taken: {round(time,4)}s.\
                Standard dev in x: {round(stdv_x,4)}mm.\
                Standard dev in y: {round(stdv_y,4)}mm', fontsize=12, color='blue')
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.title(f"{hz} hz {scantype}")
    plt.legend()
    plt.show()
    
    
if __name__ == "__main__":
    
    #Parameters for specific data
    x_pos = 0
    y_pos = 0
    file_path = f"/dls/science/users/qqh35939/flyscan-hdf-files/flyscan-500hz-100-runup-mmm1.h5"
    hz = 500
    runup_distance = 0.1 #mm
    scantype = "Flyscan"
    
    plot_y_and_x2(hz, file_path, file_path, x_pos, y_pos,runup_distance,scantype)
    
    