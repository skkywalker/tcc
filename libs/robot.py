import numpy as np
import math
import matplotlib.pyplot as plt
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

def plot_arrow(x, y, yaw, length=0.05, width=0.05, fc="r", ec="k"):
    if not isinstance(x, float):
        for (ix, iy, iyaw) in zip(x, y, yaw):
            plot_arrow(ix, iy, iyaw)
    else:
        plt.arrow(x, y, length * math.cos(yaw), length * math.sin(yaw),
                  fc=fc, ec=ec, head_width=width, head_length=width)
        plt.plot(x, y)

robot = DifferentialDrive(0.1,0.5,0.5,0.5,0,1.0,0.2)

i = 0
while(robot.yaw < 3.1415/2):
    now = time.time()
    plt.cla()
    plot_arrow(robot.x, robot.y, robot.yaw)
    plt.axis("equal")
    plt.grid(True)
    plt.title("Tempo (s):" + str(i))
    plt.pause(0.0001)
    passed = time.time()-now
    i += passed
    robot.update(passed)
#robot.pure_pursuit((0,0),[(1,1)],1,1)