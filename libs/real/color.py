import numpy as np

def color(color_name):
    try:
        lower = np.load('color_values/lower_'+color_name+'.npy')
        upper = np.load('color_values/upper_'+color_name+'.npy')
    except:
        lower = np.array([0,0,0])
        upper = np.array([255,255,255])
    return lower, upper