import numpy as np
import math

class DifferentialDrive():
    def __init__(self,width,lenght,wheel_radius,x,y,yaw,max_rps,speed=0.1):
        self.width = width
        self.wheel_radius = wheel_radius
        self.lenght = lenght

        self.x = x
        self.y = y
        self.yaw = yaw

        self.speed = speed
        self.max_rps = max_rps
        self.omega = 0.0

        self.x_hist = [x]
        self.y_hist = [y]
    
    def update(self, dt):

        self.x += self.speed * math.cos(self.yaw) * dt
        self.y += self.speed * math.sin(self.yaw) * dt
        self.yaw += self.omega * dt
        self.x_hist.append(self.x)
        self.y_hist.append(self.y)

    def get_wheel_speed(self):
        left = (self.speed - self.omega*self.lenght/2)/self.wheel_radius
        right = (self.speed + self.omega*self.lenght/2)/self.wheel_radius
        return (left,right)

    def find_closest(self, path, kp):
        x = self.x + self.speed*math.cos(self.yaw) * kp
        y = self.y + self.speed*math.sin(self.yaw) * kp
        least = math.sqrt( (x-path[0][0])**2 + (y-path[0][1])**2 )
        position = 0
        for i,pos in enumerate(path):
            tmp = math.sqrt( (x-pos[0])**2 + (y-pos[1])**2 )
            if(tmp < least):
                least = tmp
                position = i
        return position

    def next_position(self):
        return((self.x + self.speed*math.cos(self.yaw),self.y + self.speed*math.sin(self.yaw)))

    def apply_max_motor(self):
        return 0