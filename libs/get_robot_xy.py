import cv2
import numpy as np

def get_robot_xy(frame):
    
    lower_red = np.array([200,200,0])
    upper_red = np.array([255,255,100])
    mask1 = cv2.inRange(frame, lower_red, upper_red)
    return mask1