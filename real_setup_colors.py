import cv2
import numpy as np
import sys

def write_files(lista, list_name):
    b = np.array([])
    g = np.array([])
    r = np.array([])
    for item in lista:
        b = np.append(b,item[0])
        g = np.append(g,item[1])
        r = np.append(r,item[2])
    lower = 0.9*np.array([b.min(),g.min(),r.min()])
    upper = 1.1*np.array([b.max(),g.max(),r.max()])
    lower = lower.astype(int)
    upper = upper.astype(int)
    np.save('color_values/' + 'lower_' + list_name, lower)
    np.save('color_values/' + 'upper_' + list_name, upper)


def colorSetup(event,x,y,flags,param):
    global colors_tmp, colors, samples, color_names
    if event == cv2.EVENT_LBUTTONDOWN:
        B = frame[y,x,0]
        G = frame[y,x,1]
        R = frame[y,x,2]
        colors_tmp.append([B,G,R])
        if(len(colors_tmp) == samples):
            colors.append(colors_tmp)
            colors_tmp = list()

        if(len(colors) == len(color_names)):
            for i, l in enumerate(colors):
                write_files(l, color_names[i])
            print("Okay!")
            capture.release()
            cv2.destroyAllWindows()
            exit(0)

cv2.namedWindow('colorSetup')
cv2.setMouseCallback('colorSetup',colorSetup)

capture = cv2.VideoCapture(0)
colors = list()
colors_tmp = list()
if(len(sys.argv) > 2):
    color_names = sys.argv[2:]
else:
    color_names = ['vermelho', 'azul']
samples = int(sys.argv[1])

while(True):

    ret, frame = capture.read()
    if ret:
        cv2.putText(frame,color_names[len(colors)],(10,40),cv2.FONT_HERSHEY_SIMPLEX, 1, [0,255,0],2)
        cv2.imshow('colorSetup', frame)

    if cv2.waitKey(1) == 27:
        break

capture.release()
cv2.destroyAllWindows()