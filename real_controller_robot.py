import pygame
import numpy as np
import socket
import time
import re

def send_wheel_speed(left_speed, right_speed, dest):
    max_rps = 1.5

    left_speed = int(100*round(max_rps*left_speed,2))
    right_speed = int(100*round(max_rps*right_speed,2))
    print("  left_speed:",left_speed, "\tright_speed:", right_speed)

    left_speed = bytes([left_speed])
    right_speed = bytes([right_speed])

    data = left_speed + right_speed
    
    try:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect(dest)
        tcp.send(data)
        time.sleep(0.01)
        tcp.close()
        print("Data sent!")
    except:
        print("Erro!")

pygame.init()

j = pygame.joystick.Joystick(0)
j.init()

last_speed = (0,0)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.JOYAXISMOTION:
            direita = -j.get_axis(3)
            if(direita < 0.15):
                direita = 0.0
            esquerda = -j.get_axis(1)
            if(esquerda < 0.15):
                esquerda = 0.0
            speed = (round(esquerda,2), round(direita,2)) # speed, omega
    if(last_speed != speed):
        last_speed = speed
        send_wheel_speed(speed[0],speed[1],('192.168.1.181', 8888))