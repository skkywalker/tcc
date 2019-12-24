import cv2
import numpy as np
import sys

def organise_data(lista):
    #lista = [ [[C1], [C2]], [[C1], [C2]], [[C1], [C2]] ]
    #objetivo = [ [C1,C1,C1],[C2,C2,C2] ]

    global color_names, color_location, samples

    tmp_list = [[] for i in color_names]
    # tmp_list = [ [],[] ]
    for color in range(len(color_names)):
        for samp in lista:
            # samp = [[C1], [C2]]
            tmp_list[color].append(samp[color][0])

    return tmp_list

def write_files(lista, list_name):
    b = np.array([])
    g = np.array([])
    r = np.array([])
    for item in lista:
        b = np.append(b,item[0])
        g = np.append(g,item[1])
        r = np.append(r,item[2])
    lower = 0.95*np.array([b.min(),g.min(),r.min()])
    upper = 1.05*np.array([b.max(),g.max(),r.max()])
    lower = lower.astype(int)
    upper = upper.astype(int)
    np.save('color_values/' + 'lower_' + list_name, lower)
    np.save('color_values/' + 'upper_' + list_name, upper)
    print("Salvando", list_name, "como:")
    print("Lower:", lower)
    print("Upper:", upper)


def colorSetup(event,x,y,flags,param):
    global colors_tmp, colors, samples, color_names, color_location
    if event == cv2.EVENT_LBUTTONDOWN:
        B = frame[y,x,0]
        G = frame[y,x,1]
        R = frame[y,x,2]
        colors_tmp.append([B,G,R])
        if(len(colors_tmp) == samples):
            colors.append(colors_tmp)
            colors_tmp = list()

        if(len(colors) == len(color_names)):
            color_location.append(colors)
            colors = list()
            colors_tmp = list()
            if(len(color_location) == locations):
                tmp = organise_data(color_location)
                for i, li in enumerate(tmp):
                    write_files(li, color_names[i])
                print("Okay!")
                capture.release()
                cv2.destroyAllWindows()
                exit(0)

cv2.namedWindow('colorSetup')
cv2.setMouseCallback('colorSetup',colorSetup)

capture = cv2.VideoCapture(0)
colors = list()
colors_tmp = list()
color_location = list()
if(len(sys.argv) == 1):
    print("------------------------------")
    print("Usage:")
    print("------------------------------")
    print("python foo.py [samples] [locations] [colors]")
    print("------------------------------")
    exit(1)
samples = int(sys.argv[1])
locations = int(sys.argv[2])
color_names = sys.argv[3:]

while(True):

    ret, frame = capture.read()
    if ret:
        cv2.putText(frame,color_names[len(colors)],(10,40),cv2.FONT_HERSHEY_SIMPLEX, 1, [0,255,0],2)
        cv2.imshow('colorSetup', frame)

    if cv2.waitKey(1) == 27:
        break

capture.release()
cv2.destroyAllWindows()