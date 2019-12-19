from libs.path_finding import path_find
from libs.robot import DifferentialDrive
from libs.plot_arrow import plot_arrow
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import math
import numpy as np
import cv2

def get_image_dims(im_path):
    im = cv2.imread(im_path)
    h, w, c = im.shape
    return h,w

def norm(p1,p2):
    return(math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 ))

def absolute(point):
    return(math.sqrt(point[0]**2+point[1]**2))

def lookahead(path,la,i, max_la):
    x = path[i][0]
    y = path[i][1]
    for j,pos in enumerate(path[i:]):
        if(norm((x,y),pos) < la):
            continue
        else:
            return i+j,pos
    return len(path)-1, finish

def calculate_angle(current, nex, desired, ganho):
    n = (nex[0]-current[0], nex[1]-current[1])
    d = (desired[0]-current[0], desired[1]-current[1])
    sin_theta = (n[0]*d[1]-d[0]*n[1])/(absolute(n)*absolute(d))
    return np.arcsin(sin_theta) * ganho

def update(frame):
    global last_updated, init_time
    global robot
    global path,pathx,pathy, finish
    global real_map_width, real_map_height
    
    # Desenha as coisas que precisa
    ax1.clear()
    ax1.imshow(img,extent=[0, real_map_width, 0, real_map_height])
    ax1.set_ylim([0, real_map_height])
    ax1.set_xlim([0, real_map_width])
    ax1.set_title(str(round(time.time()-init_time,1)) + " segundos")
    ax1.plot(pathx,pathy, "-k", label="path")
    ax1.plot(robot.x_hist, robot.y_hist, "-b", label="trajectory")
    plot_arrow(robot,ax1)
    if(norm((robot.x, robot.y), finish) < 0.01):
        ani.event_source.stop()

    # Correções do pure pursuit

    closest = robot.find_closest(path, 0.2)
    pos, desired = lookahead(path, 0.1, closest, finish)

    ax1.plot([pathx[closest]],[pathy[closest]], marker='o', markersize=3, color="red")
    ax1.plot([pathx[pos]],[pathy[pos]], marker='x', markersize=5, color="green")

    current_pos = (robot.x, robot.y)
    next_pos = robot.next_position()

    robot.omega = calculate_angle(current_pos,next_pos,desired,1)

    # Update das posições do robo
    robot.update(time.time()-last_updated)
    last_updated = time.time()
    
'''
Variáveis importantes da simulação
'''

map_source = 'map-pics/test2.png'

robot_features = {
    'largura' : 0.1,
    'comprimento' : 0.1,
    'raio_roda' : 0.06
}

real_map_width = 2 # em metros


img_height, img_width = get_image_dims(map_source)
real_map_height = img_height*real_map_width/img_width
    
path = path_find(map_source, robot_features['largura'], real_map_width/img_width)
pathx = []
pathy = []
for i in range(len(path)):
    path[i] = (path[i][0]*1.5/480,1.5-2*path[i][1]/640)
    pathx.append(path[i][0])
    pathy.append(path[i][1])

finish = (path[-1])

robot = DifferentialDrive(robot_features['largura'], \
    robot_features['comprimento'], \
    robot_features['raio_roda'], \
    pathx[0],pathy[0],yaw=0,maxrps=2.5,speed=0.1)

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
img = plt.imread(map_source)
init_time = time.time()
last_updated = init_time

ani = animation.FuncAnimation(fig, update, interval=50)
plt.show()