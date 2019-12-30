import cv2
import numpy as np
import math
from .color import color

def rotateImage(image, angle, rotation_point):
  rot_mat = cv2.getRotationMatrix2D(rotation_point, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

pos = [] 

def getMap(event,x,y,flags,param):
    global pos
    if event == cv2.EVENT_LBUTTONDOWN:
        pos.append((x,y))

def get_map_clicking():
    global pos
    cv2.namedWindow('getMap')
    cv2.setMouseCallback('getMap',getMap)
    camera = cv2.VideoCapture(0)
    while(True):
        ret, frame = camera.read()
        frame = cv2.resize(frame,(640,480))
        if len(pos)==0:
            text = 'Top left'
        elif(len(pos)==1):
            text = 'Top right'
        else:
            text = 'error'
        if(len(pos) == 2):
            break
        cv2.putText(frame,text,(10,40),cv2.FONT_HERSHEY_SIMPLEX, 1, [0,255,0],2)
        cv2.imshow('getMap',frame)
        if cv2.waitKey(1) == 27:
            break

    tl,tr = pos

    rotate_angle = math.atan2(tr[1]-tl[1],tr[0]-tl[0])*180/math.pi
    pos = []

    while(True):
        ret, frame = camera.read()
        frame = cv2.resize(frame,(640,480))
        rotated_img = rotateImage(frame, rotate_angle, tl)
        if len(pos)==0:
            text = 'Bottom Right'
        else:
            text = 'error'
        if(len(pos) == 1):
            break
        cv2.putText(rotated_img,text,(10,40),cv2.FONT_HERSHEY_SIMPLEX, 1, [0,255,0],2)
        cv2.imshow('getMap',rotated_img)
        if cv2.waitKey(1) == 27:
            break

    br = pos[0]

    img = rotated_img[tl[1]:br[1],tl[0]:br[0]]
    camera.release()
    cv2.imshow('result', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return img, rotate_angle, tl, br