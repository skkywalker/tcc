import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

class DifferentialDrive():
    def __init__(self,L,R,x,y,yaw,v=0.0,w=0.0):
        self.L = L
        self.R = R

        self.x = x
        self.y = y
        self.yaw = yaw

        self.v = v
        self.w = w
    
    def update(self, dt):
        self.x += self.v * math.cos(self.yaw) * dt
        self.y += self.v * math.sin(self.yaw) * dt
        self.yaw += self.w * dt

    def get_wheel_speed(self):
        '''
        Returns right & left wheels in m/s
        '''
        left = self.v - self.w*self.L/2
        right = self.v + self.w*self.L/2
        return (left,right)

    def pure_pursuit(self,finish,path,la,t):
        while not (finish[0]+t > self.x and finish[0]-t < self.x and finish[1]+t > self.y and finish[1]-t < self.y):
            # Run algorithm
            print('a')

def norm(p1,p2):
    return(math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 ))

def find_closest(robot, path):
    x = robot.x
    y = robot.y
    least = norm((x,y),path[0])
    position = 0
    for i,pos in enumerate(path):
        if(norm((x,y),pos) < least):
            least = norm((x,y),pos)
            position = i
    return position

def lookahead(path,la,i):
    x = path[i][0]
    y = path[i][1]
    for i,pos in enumerate(path[i:]):
        if(norm((x,y),pos) < la):
            continue
        else:
            return pos

def plot_arrow(robot):
    # Main arrow
    ax1.arrow(robot.x, robot.y, 0.1 * math.cos(robot.yaw), 0.1 * math.sin(robot.yaw),
                 fc='r', ec='k', head_width=0.05, head_length=0.05)
    # Sides
    ax1.arrow(robot.x, robot.y, robot.L/2 * math.cos(robot.yaw+math.pi/2), robot.L/2 * math.sin(robot.yaw+math.pi/2),
                 ec='k', head_width=2*robot.R, head_length=0)
    ax1.arrow(robot.x, robot.y, robot.L/2 * math.cos(robot.yaw-math.pi/2), robot.L/2 * math.sin(robot.yaw-math.pi/2),
                 ec='k', head_width=2*robot.R, head_length=0.)


def update(frame):
    global last_updated
    global robot
    ax1.clear()
    ax1.imshow(img,extent=[0, 2, 0, 1.5])
    ax1.set_ylim([0, 1.5])
    ax1.set_xlim([0, 2])
    ax1.set_title(str(round(time.time()-init_time,1)) + " segundos")
    plot_arrow(robot)
    
    robot.update(time.time()-last_updated)
    last_updated = time.time()
    if(robot.x > 0.9):
        ani.event_source.stop()
    

robot = DifferentialDrive(0.1,0.06,0.5,0.5,0,0,3.1415/4)

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
img = plt.imread('../map-pics/test2.png') # CONSERTAR ISSO
init_time = time.time()
last_updated = init_time

ani = animation.FuncAnimation(fig, update, interval=100)
plt.show()
    
#robot.pure_pursuit((0,0),[(1,1)],1,1)