from libs.real.robot import RealDifferentialDrive
from libs.real.get_robot_xy import get_robot_xyyaw
import cv2
import matplotlib.pyplot as plt
import math
import numpy as np

import time

camera = cv2.VideoCapture(0)
ret, frame = camera.read()
frame = cv2.resize(frame,(640,480))
robot = RealDifferentialDrive(get_robot_xyyaw(frame,1.0), \
        0.12, \
        0.18, \
        0.03, \
        1.5, 0.2)
now = time.time()

while(1):
    ret, frame = camera.read()
    frame = cv2.resize(frame,(640,480))
    h,w,c = frame.shape
    pos = get_robot_xyyaw(frame,1.0)
    robot.update_info(time.time()-now,pos)

    x = int(robot.x*h)
    y = int(h-robot.y*h)

    cv2.circle(frame,(x,y),4,[0,0,255],2)
    finish = (x + int(50*math.cos(robot.yaw)),y + int(50*math.sin(robot.yaw)))
    cv2.arrowedLine(frame,(x,y),finish,[0,0,255],1)

    cv2.imshow('robot',frame)

    if cv2.waitKey(30) & 0xff == 27:
        break
    now = time.time()

cv2.destroyAllWindows()