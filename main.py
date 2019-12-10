from libs.path_finding import path_find
from libs.robot import DifferentialDrive
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import math

def norm(p1,p2):
    return(math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 ))

def lookahead(path,la,i):
    x = path[i][0]
    y = path[i][1]
    for j,pos in enumerate(path[i:]):
        if(norm((x,y),pos) < la):
            continue
        else:
            return i+j,pos

def plot_arrow(robot):
    ax1.arrow(robot.x, robot.y, 0.1 * math.cos(robot.yaw), 0.1 * math.sin(robot.yaw), fc='r', ec='k', head_width=0.05, head_length=0.05)
    ax1.arrow(robot.x, robot.y, robot.L/2 * math.cos(robot.yaw+math.pi/2), robot.L/2 * math.sin(robot.yaw+math.pi/2), ec='k', head_width=2*robot.R, head_length=0)
    ax1.arrow(robot.x, robot.y, robot.L/2 * math.cos(robot.yaw-math.pi/2), robot.L/2 * math.sin(robot.yaw-math.pi/2), ec='k', head_width=2*robot.R, head_length=0.)


def update(frame):
    global last_updated
    global robot
    global path,pathx,pathy
    ax1.clear()
    ax1.imshow(img,extent=[0, 2, 0, 1.5])
    ax1.set_ylim([0, 1.5])
    ax1.set_xlim([0, 2])
    ax1.set_title(str(round(time.time()-init_time,1)) + " segundos")
    ax1.plot(pathx,pathy, "-k", label="path")
    ax1.plot(robot.x_hist, robot.y_hist, "-b", label="trajectory")
    plot_arrow(robot)

    robot.update(time.time()-last_updated)
    last_updated = time.time()
    if(robot.x > 0.9):
        ani.event_source.stop()
    
path = path_find('map-pics/test2.png')
pathx = []
pathy = []
for i in range(0,len(path),10):
    #path[i] = (path[i][0]*1.5/480,2*path[i][1]/640)
    path[i] = (path[i][0]*1.5/480,2*path[i][1]/640)
    pathx.append(path[i][0])
    pathy.append(1.5-path[i][1])


robot = DifferentialDrive(0.1,0.06,pathx[0],pathy[0],3*3.1415/2,0.1,0)

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
img = plt.imread('map-pics/test2.png')
init_time = time.time()
last_updated = init_time

ani = animation.FuncAnimation(fig, update, interval=100)
plt.show()
    
#robot.pure_pursuit((0,0),[(1,1)],1,1)