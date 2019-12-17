from libs.path_finding import path_find
from libs.robot import DifferentialDrive
from libs.plot_arrow import plot_arrow
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import math
import numpy as np

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

def calculate_angle(current, nex, desired):
    n = (nex[0]-current[0], nex[1]-current[1])
    d = (desired[0]-current[0], desired[1]-current[1])
    sin_theta = (n[0]*d[1]-d[0]*n[1])/(absolute(n)*absolute(d))
    return np.arcsin(sin_theta)

def update(frame):
    global last_updated, init_time
    global robot
    global path,pathx,pathy, finish
    
    # Desenha as coisas que precisa
    ax1.clear()
    ax1.imshow(img,extent=[0, 2, 0, 1.5])
    ax1.set_ylim([0, 1.5])
    ax1.set_xlim([0, 2])
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

    robot.w = calculate_angle(current_pos,next_pos,desired) * robot.k

    # Update das posições do robo
    robot.update(time.time()-last_updated)
    last_updated = time.time()
    
    
path = path_find('map-pics/test2.png')
pathx = []
pathy = []
for i in range(len(path)):
    path[i] = (path[i][0]*1.5/480,1.5-2*path[i][1]/640)
    pathx.append(path[i][0])
    pathy.append(path[i][1])

finish = (path[-1])

robot = DifferentialDrive(0.1,0.1,0.06,pathx[0],pathy[0],2*math.pi-0.5,1,0.1,0)

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
img = plt.imread('map-pics/test2.png')
init_time = time.time()
last_updated = init_time

ani = animation.FuncAnimation(fig, update, interval=50)
plt.show()
    
#robot.pure_pursuit((0,0),[(1,1)],1,1)