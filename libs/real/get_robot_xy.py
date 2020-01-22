import cv2
import numpy as np
import math
from ..get_center import get_center
from .color import color

def open_close(input_mask):
    kernel = np.ones([4,4])
    mask = cv2.morphologyEx(input_mask, cv2.MORPH_CLOSE, kernel, iterations=1)
    #mask = cv2.morphologyEx(mask, cv2.MORPH_ERODE, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    return mask

def get_robot_xyyaw(frame, real_height):
    '''
    O robô tem duas cores para identificar o yaw. Primeiro identificamos
    o centro de cada uma, para depois identificar o xy e yaw.
    '''

    height, _, __ = frame.shape

    # Primeira cor
    lower_1, upper_1 = color('azul')
    c1 = cv2.inRange(frame, lower_1, upper_1)
    c1 = open_close(c1)
    c1_x, c1_y = get_center(c1)

    # Segunda cor
    lower_2, upper_2 = color('vermelho')
    c2 = cv2.inRange(frame, lower_2, upper_2)
    c2 = open_close(c2)
    c2_x, c2_y = get_center(c2)

    # X e Y serão a média dos dois centros
    Xi = int(0.5*(c1_x + c2_x))
    Yi = int(0.5*(c1_y + c2_y))

    # Yaw é o ângulo entre eles
    yaw = -1*math.atan2(c1_y-c2_y,c1_x-c2_x)

    # Passamos X e Y para coordenadas em metro
    X = Xi*real_height/height
    Y = real_height - Yi*real_height/height

    framecp = frame.copy()
    
    framecp[c1 > 0] = [0,100,100]
    framecp[c2 > 0] = [0,255,0]

    cv2.circle(framecp,(c1_x,c1_y),2,[0,0,255],3)
    cv2.circle(framecp,(c2_x,c2_y),2,[255,0,0],3)

    cv2.circle(framecp,(Xi,Yi),3,[100,100,100],3)
    cv2.imshow('robot_pos', framecp)

    return X, Y, yaw