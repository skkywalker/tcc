import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

def plot_arrow(robot,axis):
    axis.arrow(robot.x, robot.y, robot.SIZE * math.cos(robot.yaw), robot.SIZE * math.sin(robot.yaw), fc='r', ec='k', head_width=0.05, head_length=0.05)
    axis.arrow(robot.x, robot.y, robot.L/2 * math.cos(robot.yaw+math.pi/2), robot.L/2 * math.sin(robot.yaw+math.pi/2), ec='k', head_width=2*robot.R, head_length=0)
    axis.arrow(robot.x, robot.y, robot.L/2 * math.cos(robot.yaw-math.pi/2), robot.L/2 * math.sin(robot.yaw-math.pi/2), ec='k', head_width=2*robot.R, head_length=0.)