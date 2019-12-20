import math
import numpy as np
import cv2

'''
Funções matemáticas gerais
'''

def norm(p1,p2):
    return(math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 ))

def absolute(point):
    return(math.sqrt(point[0]**2+point[1]**2))

def calculate_angle(current, nex, desired):
    n = (nex[0]-current[0], nex[1]-current[1])
    d = (desired[0]-current[0], desired[1]-current[1])
    sin_theta = (n[0]*d[1]-d[0]*n[1])/(absolute(n)*absolute(d))
    return np.arcsin(sin_theta)

def get_image_dims(im_path):
    im = cv2.imread(im_path)
    h, w, c = im.shape
    return h,w