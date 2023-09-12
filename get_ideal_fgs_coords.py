import numpy as np
import matplotlib.pyplot as plt

"""get x2 and y positions from an ideal fgs, output is 2d array [[x0,y0], [x1,y1],...]
Coordinates here are the points where the eiger BEGINS to trigger
"""
def get_coords(x_start=0, y_start=0):
    
    #FGS variables from EDM screen
    x_steps = 30
    y_steps = 23
    x_step_size = 0.02
    y_step_size = 0.02
    dwell_time = 5
    x_start_pos = x_start
    y_start_pos = y_start
    
    x_counter = 0
    current_y = y_start_pos
    iteration = 0
    coordinates = []
    current_x = x_start_pos - x_step_size/2

    while current_y < (y_start_pos+(y_step_size*y_steps)):
        
        if iteration % 2 == 0:
            # Make x go from left to right
            while x_counter < x_steps:
                coordinates.append([current_x, current_y]) #trigger here
                current_x = x_start_pos + (x_step_size*(x_counter+1)) - (x_step_size/2)
                x_counter += 1
        
        else:
            #make x go from right to left
            while x_counter > 0:
                coordinates.append([current_x, current_y]) #trigger here
                x_counter -= 1
                current_x = x_start_pos + (x_counter*x_step_size) - (x_step_size/2) 
                                 
        iteration += 1
        current_y += y_step_size
            
    coordinates = np.array(coordinates)
    return coordinates

"""get x2 and y positions from an ideal fgs, output is 2d array [[x0,y0], [x1,y1],...]
Gives the min max mean coords of the smargon during each trigger point
"""
def get_mmm_coords(x_start_pos=0, y_start_pos=0):
    #FGS variables from EDM screen
    x_steps = 30
    y_steps = 23
    x_step_size = 0.02
    y_step_size = 0.02
    x_counter = 0
    current_y = y_start_pos
    iteration = 0
    current_x = x_start_pos
    x_min = [x_step_size/2]*x_steps*y_steps
    x_max = [x_step_size/2]*x_steps*y_steps #Min and max points are relative to mean
    x_mean = []
    y_mean = []
    

    while current_y < (y_start_pos+(y_step_size*y_steps)):
        
        if iteration % 2 == 0:
            # Make x go from left to right
            while x_counter < x_steps:
                x_mean.append(current_x)
                y_mean.append(current_y)
                current_x = x_start_pos + (x_step_size*(x_counter+1))
                x_counter += 1
        
        else:
            #make x go from right to left
            while x_counter > 0:
                x_counter -= 1
                current_x = x_start_pos + (x_counter*x_step_size)
                x_mean.append(current_x)
                y_mean.append(current_y)
                
                                 
        iteration += 1
        current_y += y_step_size
            

    return x_min, x_max, x_mean, y_mean
    
    
if __name__ == "__main__":
    coordinates = get_coords()
    plt.plot(coordinates[:, 0], coordinates[:, 1])
    plt.show()
    
    