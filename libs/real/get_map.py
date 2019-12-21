import cv2
import numpy as np
import math

def find_corners_from_points(points_init):
    points = []
    for point in points_init:
        points.append((point[0][0],point[0][1]))

    right_most = (0,0)
    second_right = (0,0)
    for point in points:
        x = point[0]
        if (x > right_most[0]):
            second_right = right_most
            right_most = point
        elif (x > second_right[0]):
            second_right = point
    if(right_most[1] > second_right[1]):
        br = right_most
        tr = second_right
    else:
        br = second_right
        tr = right_most
    
    points.remove(right_most)
    points.remove(second_right)
    if(points[0][1] > points[1][1]):
        bl = points[0]
        tl = points[1]
    else:
        bl = points[1]
        tl = points[0]
    return tr,tl,bl,br

def find_corners(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if (cv2.arcLength(contours[0], True) > cv2.arcLength(contours[1], True)):
        go_with = 0
    else:
        go_with = 1

    points = cv2.approxPolyDP(contours[go_with], 0.01*cv2.arcLength(contours[go_with], True), True)
    
    tr,tl,bl,br = find_corners_from_points(points)
    return tr,tl,bl,br

def rotateImage(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def first_filter(image, kernel, lower, upper):
    mask = cv2.inRange(image, lower, upper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    return mask

def get_map_img(path='libs/real/board.png'):
    img = cv2.imread(path)

    bounds = first_filter(img, np.ones([5,5]), np.array([0,0,100]), np.array([100,100,255]))
    tr,tl,bl,br = find_corners(bounds)
    rotate_angle = math.atan2(tr[1]-tl[1],tr[0]-tl[0])*180/math.pi
    
    rotated_img = rotateImage(img, rotate_angle)

    bounds = first_filter(rotated_img, np.ones([5,5]), np.array([0,0,100]), np.array([100,100,255]))
    tr,tl,bl,br = find_corners(bounds)

    img = rotated_img[tl[1]:br[1],tl[0]:br[0]]

    return img

def get_map_cam(cam_num=0):
    camera = cv2.VideoCapture(cam_num)
    ret, frame = camera.read()
    
    bounds = first_filter(frame, np.ones([5,5]), np.array([0,0,100]), np.array([100,100,255]))
    tr,tl,bl,br = find_corners(bounds)
    rotate_angle = math.atan2(tr[1]-tl[1],tr[0]-tl[0])*180/math.pi
    
    rotated_img = rotateImage(frame, rotate_angle)

    bounds = first_filter(rotated_img, np.ones([5,5]), np.array([0,0,100]), np.array([100,100,255]))
    tr,tl,bl,br = find_corners(bounds)

    img = rotated_img[tl[1]:br[1],tl[0]:br[0]]

    return img
