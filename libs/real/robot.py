import numpy as np
import math
from ..custom_math import norm
from .get_robot_xy import get_robot_xy
import socket

class RealDifferentialDrive():
    def __init__(self,width,lenght,wheel_radius,max_rps,kp):
        # Características gerais
        self.width = width
        self.wheel_radius = wheel_radius
        self.lenght = lenght

        self.kp = kp
        self.max_rps = max_rps

        # Posição inicial
        self.x = 0
        self.previous_x = 0
        self.y = 0
        self.previous_y = 0
        self.yaw = 0
        self.previous_yaw = 0

        # Velocidades iniciais
        self.omega = 0.0
        self.speed = max_rps*wheel_radius*2*np.pi/10

        self.update_info()

        # Variáveis para registrar histórico
        self.x_hist = [x]
        self.y_hist = [y]
        self.left_wheel_rps_hist = []
        self.right_wheel_rps_hist = []
        self.speed_hist = [self.speed]
        self.omega_hist = [self.omega]
        self.dist_hist = []

    def send_wheel_speed(self, dest):
        # Da modelagem de um Robô Diferencial
        self.left_speed = self.speed - self.omega*self.width/2
        self.right_speed = self.speed + self.omega*self.width/2

        # V = (RPS*2*pi)*R
        self.left_rps = self.left_speed/(self.wheel_radius*2*np.pi)
        self.right_rps = self.right_speed/(self.wheel_radius*2*np.pi)

        self.left_wheel_rps_hist.append(self.left_rps)
        self.right_wheel_rps_hist.append(self.right_rps)

        data = str(100*int(round(self.left_rps,2))) + str(100*int(round(self.right_rps,2)))
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect(dest)
        tcp.send(data.encode())
        _ = tcp.recv(1)
        tcp.close()

    def get_cam_info(self, mp):
        camera = cv2.VideoCapture(cam)
        ret, frame = camera.read()
        camera.release()
        x,y,yaw = get_robot_xyyaw(frame, mp)
        return x,y,yaw
    
    def update_info(self, dt, map_height):
        '''
        Pega pela camera o x, y e yaw do robo
        '''
        self.previous_x = x - 0.001
        self.previous_y = y - 0.001
        self.previous_yaw = yaw
        self.x,self.y,self.yaw = self.get_cam_info(map_height)

        self.x_hist.append(self.x)
        self.y_hist.append(self.y)

        self.speed = norm((self.previous_x,self.previous_y),(self.x, self.y))/dt
        self.omega = (self.yaw-self.previous_yaw)/dt

        self.speed_hist.append(self.speed)
        self.omega_hist.append(self.omega)
        

    def update_speed(self, omega, gain):
        '''
        Calcula e atualiza as velocidades, de acordo com o omega
        desejado (pelo algoritmo PP).
        '''
        omega *= gain
        if(omega < 0):
            sig = -1
        else:
            sig = 1

        # Verifica se o omega não extrapola a velocidade máxima do motor
        if(abs(omega) > self.max_rps*2*np.pi*self.wheel_radius/self.width):
            self.omega = sig*self.max_rps*2*np.pi*self.wheel_radius/self.width
        else:
            self.omega = omega

        # Calcula a velocidade a partir do que "sobra" de rps para o motor
        self.speed = self.max_rps*2*math.pi*self.wheel_radius-abs(self.omega)*self.width/2

        self.send_wheel_speed(dest=('192.168.1.172', 8888))

    def lookahead(self, path, la):
        '''
        Função principal no algoritmo Pure Pursuit
        '''
        # 1) Encontrar o ponto no path mais próximo do carrinho
        x, y = self.next_position()
        least = norm((x,y), path[0])
        position = 0

        for i,pos in enumerate(path):
            tmp = norm((x,y), pos)
            if(tmp < least):
                least = tmp
                position = i
        # 'least' é o valor da menor distância
        # 'position' é a posição i no vetor path, da menor distância
        self.dist_hist.append(100*least)

        # 2) Encontrar o ponto de 'lookahead'
        x, y = path[position]
        for j,pos in enumerate(path[position:]):
            if(norm((x,y),pos) < la):
                continue
            else:
                return position, position+j, pos
        return position, len(path)-1, path[-1]

    def next_position(self):
        return((self.x + self.speed*math.cos(self.yaw)*self.kp, self.y + self.speed*math.sin(self.yaw)*self.kp))