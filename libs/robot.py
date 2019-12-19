import numpy as np
import math

class DifferentialDrive():
    def __init__(self,width,lenght,wheel_radius,x,y,yaw,max_rps):
        self.width = width
        self.wheel_radius = wheel_radius
        self.lenght = lenght

        self.x = x
        self.y = y
        self.yaw = yaw

        self.max_rps = max_rps
        self.omega = 0.0

        self.speed = max_rps*wheel_radius*2*np.pi

        self.update_wheel_speed()

        self.x_hist = [x]
        self.y_hist = [y]

    def update_wheel_speed(self):
        self.left_speed = self.speed - self.omega*self.width/2
        self.right_speed = self.speed + self.omega*self.width/2

        self.left_rps = self.left_speed/(self.wheel_radius*2*np.pi)
        self.right_rps = self.right_speed/(self.wheel_radius*2*np.pi)
    
    def update_pos(self, dt):
        self.x += self.speed * math.cos(self.yaw) * dt
        self.y += self.speed * math.sin(self.yaw) * dt
        self.yaw += self.omega * dt

        self.x_hist.append(self.x)
        self.y_hist.append(self.y)

    def update_speed(self, omega, kp):
        omega = omega * kp
        if(omega < 0):
            sig = -1
        else:
            sig = 1

        if(abs(omega) > self.max_rps*2*np.pi*self.wheel_radius/self.width):
            self.omega = sig*self.max_rps*2*np.pi*self.wheel_radius/self.width
        else:
            self.omega = omega

        self.speed = self.max_rps*2*math.pi*self.wheel_radius-abs(self.omega)*self.width/2
        self.update_wheel_speed()

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
        return position, least

    def next_position(self):
        return((self.x + self.speed*math.cos(self.yaw),self.y + self.speed*math.sin(self.yaw)))