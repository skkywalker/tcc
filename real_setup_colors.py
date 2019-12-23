import cv2
import numpy as np

def write_files(lista, list_name):
    print(list_name)
    b = np.array([])
    g = np.array([])
    r = np.array([])
    for item in lista:
        b = np.append(b,item[0])
        g = np.append(g,item[1])
        r = np.append(r,item[2])
    lower = 0.9*np.array([b.min(),g.min(),r.min()])
    upper = 1.1*np.array([b.max(),g.max(),r.max()])
    print(lower.astype(int))
    print(upper.astype(int))
    

def mouseRGB(event,x,y,flags,param):
    global red, blue, count, samples
    if event == cv2.EVENT_LBUTTONDOWN:
        B = frame[y,x,0]
        G = frame[y,x,1]
        R = frame[y,x,2]
        if(count >= samples):
            red.append([B,G,R])
        elif(count >= 0):
            blue.append([B,G,R])
        count += 1
        if(count == samples):
            print("Entre", samples,"exemplos de VERMELHO")
        elif(count == 2*samples):
            print("Beleza!")
            write_files(red, 'vermelho')
            write_files(blue, 'azul')
            capture.release()
            cv2.destroyAllWindows()
            exit(0)


cv2.namedWindow('mouseRGB')
cv2.setMouseCallback('mouseRGB',mouseRGB)

capture = cv2.VideoCapture(0)
red = []
blue = []
count = 0

samples = int(input("Quantas samples de cada cor? "))

print("Entre", samples,"exemplos de AZUL")
while(True):

    ret, frame = capture.read()
    if ret:
        cv2.imshow('mouseRGB', frame)

    if cv2.waitKey(1) == 27:
        break

capture.release()
cv2.destroyAllWindows()