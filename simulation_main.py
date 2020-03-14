from libs.path_finding import path_find
from libs.robot import DifferentialDrive
from libs.plot_arrow import plot_arrow
from libs.custom_math import norm, calculate_angle, get_image_dims
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import math
import cv2

def update(frame):
    '''
    Função chamada a cada frame para atualizar o plot
    '''

    # Definições das variáveis globais
    global robot, ax1
    global last_updated, init_time
    global path,pathx,pathy,img
    global real_map_width, real_map_height
    
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
    if(norm((robot.x, robot.y), path[-1]) < 0.02):
        ani.event_source.stop()
        fig, axs = plt.subplots(5, 1, constrained_layout=True)
        fig.suptitle('Resultados', fontsize=16)

        plot_vars = [robot.right_wheel_rps_hist, robot.left_wheel_rps_hist, \
            robot.speed_hist, robot.omega_hist, robot.dist_hist]
        plot_titles = ["Roda Direita", "Roda Esquerda", "Velocidade", "Omega", "Desvio"]
        plot_yaxis = ['rps', 'rps', 'm/s', 'rad/s', 'cm']

        for i in range(5):
            axs[i].plot(plot_vars[i])
            axs[i].set_title(plot_titles[i])
            axs[i].set_ylabel(plot_yaxis[i])
            axs[i].set_xlabel('frame')
            axs[i].grid(True, axis='both')

        plt.show()

    '''
    Algoritmo Pure Pursuit
    '''
    # Encontra a distância lookahead >= 'la', a partir da posição mais próxima
    # 'closest' é a i-ésima posição em path mais próxima (ponto vermelho)
    # 'lookahead_i' é a i-ésima posição do lookahead
    # 'lookahead' é a coordenada da lookahead
    closest, lookahead_i, lookahead = robot.lookahead(path, la=0.1)

    # Plota os pontos lookahead e mais próximo
    ax1.plot([pathx[closest]],[pathy[closest]], marker='o', markersize=5, color="red")
    ax1.plot([pathx[lookahead_i]],[pathy[lookahead_i]], marker='x', markersize=5, color="green")

    # Calcula o novo omega, a partir das informações adquiridas
    current_pos = (robot.x, robot.y)
    next_pos = robot.next_position()
    robot.update_speed(calculate_angle(current_pos,next_pos,lookahead),gain=3)

    # Update da posição do carrinho e passagem de tempo
    robot.update_pos(time.time()-last_updated)
    last_updated = time.time()
    
'''
Programa principal
''' 

if __name__ == '__main__':
    # Definições básicas
    map_source = 'map-pics/test2.png'
    robot_features = {
        'width' : 0.12,
        'lenght' : 0.18,
        'wheel_radius' : 0.0315,
        'max_rps' : 1.5
    }
    real_map_width = 2.5 # em metros

    # Conta da altura, em metros, da imagem
    img_height, img_width = get_image_dims(map_source)
    real_map_height = img_height*real_map_width/img_width

    # Operações de transformação com o path
    # 1- Transformar em metros
    # 2- Criar pathy e pathx, zipando a lista
    path = path_find(map_source, robot_features['width'], real_map_width/img_width, iters=3, walls_only = 0)
    pathx = []
    pathy = []
    for i in range(len(path)):
        path[i] = (path[i][0]*real_map_width/img_width, \
            real_map_height - real_map_height*path[i][1]/img_height)
        pathx.append(path[i][0])
        pathy.append(path[i][1])

    # Criação do robô diferencial
    yaw = math.atan2(path[1][1]-path[0][1],path[1][0]-path[0][0])
    robot = DifferentialDrive(robot_features['width'], \
        robot_features['lenght'], \
        robot_features['wheel_radius'], \
        pathx[0],pathy[0],yaw=yaw,max_rps=robot_features['max_rps'], kp=0.2)

    # Início da animação
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    img = plt.imread(map_source)
    init_time = time.time()
    last_updated = init_time

    ani = animation.FuncAnimation(fig, update, interval=50)
    plt.show()