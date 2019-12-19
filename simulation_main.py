from libs.path_finding import path_find
from libs.robot import DifferentialDrive
from libs.plot_arrow import plot_arrow
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import math
import numpy as np
import cv2

def get_image_dims(im_path):
    im = cv2.imread(im_path)
    h, w, c = im.shape
    return h,w

def norm(p1,p2):
    return(math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 ))

def absolute(point):
    return(math.sqrt(point[0]**2+point[1]**2))

def lookahead(path,la,i, finish):
    x = path[i][0]
    y = path[i][1]
    for j,pos in enumerate(path[i:]):
        if(norm((x,y),pos) < la):
            continue
        else:
            return i+j,pos
    return len(path)-1, finish

def calculate_angle(current, nex, desired):
    n = (nex[0]-current[0], nex[1]-current[1])
    d = (desired[0]-current[0], desired[1]-current[1])
    sin_theta = (n[0]*d[1]-d[0]*n[1])/(absolute(n)*absolute(d))
    return np.arcsin(sin_theta)

def update(frame):
    '''
    Função chamada a cada frame para atualizar o plot
    '''

    # Definições das variáveis globais
    global last_updated, init_time
    global robot
    global path,pathx,pathy, finish
    global real_map_width, real_map_height
    global left_wheel_rps, right_wheel_rps, speed, omega
    global deviation
    
    # Operações de desenho no plot
    ax1.clear()
    ax1.imshow(img,extent=[0, real_map_width, 0, real_map_height])
    ax1.set_ylim([0, real_map_height])
    ax1.set_xlim([0, real_map_width])
    ax1.set_title(str(round(time.time()-init_time,1)) + " segundos")
    ax1.plot(pathx,pathy, "-k", label="path")
    ax1.plot(robot.x_hist, robot.y_hist, "-b", label="trajetória")
    plot_arrow(robot,ax1)

    # Se chegar no ponto final, parar a animação e mostrar infos relevantes
    if(norm((robot.x, robot.y), finish) < 0.02):
        ani.event_source.stop()
        fig, axs = plt.subplots(5, 1, constrained_layout=True)
        fig.suptitle('Resultados', fontsize=16)

        plot_vars = [right_wheel_rps, left_wheel_rps, speed, omega, deviation]
        plot_titles = ["Roda Direita", "Roda Esquerda", "Velocidade", "Omega", "Desvio"]
        plot_yaxis = ['rps', 'rps', 'm/s', 'rad/s', 'cm']

        for i in range(5):
            axs[i].plot(plot_vars[i])
            axs[i].set_title(plot_titles[i])
            axs[i].set_ylabel(plot_yaxis[i])
            axs[i].grid(True, axis='y')

        plt.show()

    '''
    Algoritmo Pure Pursuit
    '''
    # Encontra o ponto no path mais perto do carrinho numa próxima posição
    # 'dist' tem função de debug
    # 'closest' é a i-ésima posição do path
    closest, dist = robot.find_closest(path)

    # Encontra a distância lookahead >= 'la', a partir da i-ésima posição
    # 'desired' é a coordenada da lookahead
    # 'pos' é a i-ésima posição de desired no path
    pos, desired = lookahead(path, la=0.1, i=closest, finish=finish)

    # Plota os pontos lookahead e mais próximo
    ax1.plot([pathx[closest]],[pathy[closest]], marker='o', markersize=3, color="red")
    ax1.plot([pathx[pos]],[pathy[pos]], marker='x', markersize=3, color="green")

    # Calcula o novo omega, a partir das informações adquiridas
    current_pos = (robot.x, robot.y)
    next_pos = robot.next_position()
    robot.update_speed(calculate_angle(current_pos,next_pos,desired),gain=3)

    # Update das listas de controle
    right_wheel_rps.append(robot.right_rps)
    left_wheel_rps.append(robot.left_rps)
    omega.append(robot.omega)
    speed.append(robot.speed)
    deviation.append(dist*100)

    # Update da posição do carrinho e passagem de tempo
    robot.update_pos(time.time()-last_updated)
    last_updated = time.time()
    
'''
Programa principal
'''

# Listas de controle das variáveis
left_wheel_rps = []
right_wheel_rps = []
speed = []
omega = []
deviation = []

# Definições básicas
map_source = 'map-pics/test2.png'
robot_features = {
    'width' : 0.1,
    'lenght' : 0.1,
    'wheel_radius' : 0.032,
    'max_rps' : 1.5
}
real_map_width = 2 # em metros

# Conta da altura, em metros, da imagem
img_height, img_width = get_image_dims(map_source)
real_map_height = img_height*real_map_width/img_width

# Operações de transformação com o path
# 1- Transformar em metros
# 2- Criar pathy e pathx, zipando a lista
path = path_find(map_source, robot_features['width'], real_map_width/img_width)
pathx = []
pathy = []
for i in range(len(path)):
    path[i] = (path[i][0]*real_map_width/img_width, \
        real_map_height - real_map_height*path[i][1]/img_height)
    pathx.append(path[i][0])
    pathy.append(path[i][1])
finish = (path[-1])

# Criação do robô diferencial
robot = DifferentialDrive(robot_features['width'], \
    robot_features['lenght'], \
    robot_features['wheel_radius'], \
    pathx[0],pathy[0],yaw=-math.pi/4,max_rps=robot_features['max_rps'], kp=0.2)

# Início da animação
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
img = plt.imread(map_source)
init_time = time.time()
last_updated = init_time

ani = animation.FuncAnimation(fig, update, interval=50)
plt.show()