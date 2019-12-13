import numpy as np
import math

class DifferentialDrive():
    def __init__(self,L,SIZE,R,x,y,yaw,k,v=0.0,w=0.0):
        self.L = L
        self.R = R
        self.SIZE = SIZE
        self.k = k

        self.x = x
        self.y = y
        self.yaw = yaw

        self.v = v
        self.w = w

        self.x_hist = [x]
        self.y_hist = [y]
    
    def update(self, dt):

        self.x += self.v * math.cos(self.yaw) * dt
        self.y += self.v * math.sin(self.yaw) * dt
        self.yaw += self.w * dt
        self.x_hist.append(self.x)
        self.y_hist.append(self.y)

    def get_wheel_speed(self):
        '''
        Returns right & left wheels in m/s
        '''
        left = self.v - self.w*self.L/2
        right = self.v + self.w*self.L/2
        return (left,right)

    def find_closest(self, path, kp):
        x = self.x + self.v*math.cos(self.yaw) * kp
        y = self.y + self.v*math.sin(self.yaw) * kp
        least = math.sqrt( (x-path[0][0])**2 + (y-path[0][1])**2 )
        position = 0
        for i,pos in enumerate(path):
            tmp = math.sqrt( (x-pos[0])**2 + (y-pos[1])**2 )
            if(tmp < least):
                least = tmp
                position = i
        return position

    def next_position(self):
        return((self.x + self.v*math.cos(self.yaw),self.y + self.v*math.sin(self.yaw)))