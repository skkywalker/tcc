from libs.get_robot_xy import get_robot_xy
import cv2
import numpy as np

camera = cv2.VideoCapture(0)

while(1):
    ret, frame = camera.read()
    frame = cv2.resize(frame,(640,480))
    blue = frame[:,:,0]
    ret, blue_mask = cv2.threshold(blue,220,255,cv2.THRESH_BINARY)
    #mask = get_robot_xy(frame)
    print(blue_mask)
    cv2.imshow('blob', blue_mask)
    
    #cv2.imshow('frame',frame)

    if cv2.waitKey(30) & 0xff == 27:
        break
 
camera.release()
cv2.destroyAllWindows()
