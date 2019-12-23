import numpy as np
import cv2

def get_center(frame):
    M = cv2.moments(frame)
    try:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    except:
        cX = 0
        cY = 0
    return (cX, cY)