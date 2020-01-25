import cv2
import numpy as np
import sys
from libs.real.get_map import rotateImage


def write_files(lower, upper, color_name):
    np.save('color_values/' + 'lower_' + color_name, lower)
    np.save('color_values/' + 'upper_' + color_name, upper)

def load_map_setup():
    map_img = cv2.imread('map_setup/map.png')
    f = open('map_setup/rotate_angle', 'r')
    map_angle = float(f.read())
    f.close()
    f = open('map_setup/br', 'r')
    map_br = f.read()
    map_br = tuple(map(int, map_br[1:-1].split(',')))
    f.close()
    f = open('map_setup/tl', 'r')
    map_tl = f.read()
    map_tl = tuple(map(int, map_tl[1:-1].split(',')))
    f.close()
    return map_img, map_angle, map_tl, map_br

def get_frame():
    global camera, map_angle, map_tl, map_br
    ret, frame = camera.read()
    frame = cv2.resize(frame,(640,480))
    frame = rotateImage(frame,map_angle, map_tl)
    frame = frame[map_tl[1]:map_br[1],map_tl[0]:map_br[0]]
    kernel = np.ones((5,5),np.float32)/25
    frame = cv2.filter2D(frame,-1,kernel)
    return frame

def new_info(current):
    global lower, upper
    for i in range(3):
        lower[i] = int(current[i])-4 if current[i] < lower[i] else lower[i]
        upper[i] = int(current[i])+4 if current[i] > upper[i] else upper[i]

def colorSetup(event,x,y,flags,param):
    global lower,upper,on,control
    B = frame[y,x,0]
    G = frame[y,x,1]
    R = frame[y,x,2]
    if event == 1: # Mouse clicked
        if control == 0:
            lower = np.array([B,G,R])
            upper = np.array([B,G,R])
        on = 1
        control = 1
    elif event == 4: # mouse lifted
        on = 0
    elif event == 0 and on: # Dragging
        current = [B,G,R]
        new_info(current)

cv2.namedWindow('colorSetup')
cv2.setMouseCallback('colorSetup',colorSetup)

camera = cv2.VideoCapture(0)

color_name = sys.argv[1]
_, map_angle, map_tl, map_br = load_map_setup()
lower = np.array([120,120,120])
upper = np.array([120,120,120])
on = 0
control = 0
color = sys.argv[1]
while(True):
    frame = get_frame()
    framecp = frame.copy()
    c1 = cv2.inRange(frame, lower, upper)
    framecp[c1 > 0] = [0,100,100]
    cv2.imshow('colorSetup', frame)
    cv2.imshow('masks', framecp)

    if cv2.waitKey(1) == 27:
        write_files(lower,upper,color)
        break



camera.release()
cv2.destroyAllWindows()