import cv2
import numpy as np
import math
from ..get_center import get_center

def get_robot_xyyaw(frame, real_height):
    '''
    O robô tem duas cores para identificar o yaw. Primeiro identificamos
    o centro de cada uma, para depois identificar o xy e yaw.
    '''

    height, _, __ = frame.shape

    # Primeira cor
    lower_1 = np.array([0,0,100])
    upper_1 = np.array([100,100,255])
    c1 = cv2.inRange(frame, lower_1, upper_1)
    c1_x, c1_y = get_center(c1)

    # Segunda cor
    lower_2 = np.array([0,100,0])
    upper_2 = np.array([100,255,100])
    c2 = cv2.inRange(frame, lower_2, upper_2)
    c2_x, c2_y = get_center(c2)

    # X e Y serão a média dos dois centros
    Xi = 0.5*(c1_x + c2_x)
    Yi = 0.5*(c1_y + c2_y)

    # Yaw é o ângulo entre eles
    yaw = math.atan2(c2_y-c1_y,c2_x-c1_x)

    # Passamos X e Y para coordenadas em metro
    X = Xi*height/real_height
    Y = height - Yi*height/real_height

    return X, Y, yaw