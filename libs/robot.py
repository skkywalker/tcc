import numpy as np
import math
from .custom_math import norm

class DifferentialDrive():
    def __init__(self,width,lenght,wheel_radius,x,y,yaw,max_rps,kp):
        # Características gerais
        self.width = width
        self.wheel_radius = wheel_radius
        self.lenght = lenght

        self.kp = kp
        self.max_rps = max_rps

        # Posição inicial
        self.x = x
        self.y = y
        self.yaw = yaw

        # Velocidades iniciais
        self.omega = 0.0
        self.speed = max_rps*wheel_radius*2*np.pi/10

        # Variáveis para registrar histórico
        self.x_hist = [x]
        self.y_hist = [y]
        self.left_wheel_rps_hist = []
        self.right_wheel_rps_hist = []
        self.speed_hist = [self.speed]
        self.omega_hist = [self.omega]
        self.dist_hist = []

        # Chama a função para registrar as velocidades das rodas
        self.register_wheel_speed()

    def register_wheel_speed(self):
        '''
        Registra as velocidades em cada roda (RPS). Tem fução meramente
        registradora, não entra no algoritmo PP.
        '''
        # Da modelagem de um Robô Diferencial
        self.left_speed = self.speed - self.omega*self.width/2
        self.right_speed = self.speed + self.omega*self.width/2

        # V = (RPS*2*pi)*R
        self.left_rps = self.left_speed/(self.wheel_radius*2*np.pi)
        self.right_rps = self.right_speed/(self.wheel_radius*2*np.pi)

        self.left_wheel_rps_hist.append(self.left_rps)
        self.right_wheel_rps_hist.append(self.right_rps)
    
    def update_pos(self, dt):
        '''
        Calcula e atualiza a posição do robô, com base nas velocidade
        e posições x, y e yaw.
        '''
        self.yaw += self.omega * dt
        self.x += self.speed * math.cos(self.yaw) * dt
        self.y += self.speed * math.sin(self.yaw) * dt
        
        self.x_hist.append(self.x)
        self.y_hist.append(self.y)

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

        self.register_wheel_speed()
        self.speed_hist.append(self.speed)
        self.omega_hist.append(self.omega)

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