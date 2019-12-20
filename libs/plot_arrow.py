import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

def plot_arrow(robot,axis):
    '''
    Plota a posição do robô, em suas dimensões reais
    '''
    axis.arrow(robot.x, robot.y, robot.lenght * math.cos(robot.yaw), robot.lenght * math.sin(robot.yaw), fc='r', ec='k', head_width=0.05, head_length=0.05)
    axis.arrow(robot.x, robot.y, robot.width/2 * math.cos(robot.yaw+math.pi/2), robot.width/2 * math.sin(robot.yaw+math.pi/2), ec='k', head_width=2*robot.wheel_radius, head_length=0)
    axis.arrow(robot.x, robot.y, robot.width/2 * math.cos(robot.yaw-math.pi/2), robot.width/2 * math.sin(robot.yaw-math.pi/2), ec='k', head_width=2*robot.wheel_radius, head_length=0.)