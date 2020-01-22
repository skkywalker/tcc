from libs.real.get_map import get_map_clicking,rotateImage
from libs.real.path_finding import path_find
from libs.real.robot import RealDifferentialDrive
from libs.real.get_robot_xy import get_robot_xyyaw
from libs.plot_arrow import plot_arrow
from libs.custom_math import norm, absolute, calculate_angle, real_get_image_dims
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import math
import numpy as np
import cv2

def load_map_setup():
    map_img = cv2.imread('map_setup/map.png')
    f = open('map_setup/rotate_angle', 'r')
    map_angle = float(f.read())
    f.close()
    f = open('map_setup/br', 'r')
    map_br = f.read()
    map_br = tuple(map(int, map_br[1:-1].split(',')))
    f.close()
    f = open('map_setup/tl', 'r')
    map_tl = f.read()
    map_tl = tuple(map(int, map_tl[1:-1].split(',')))
    f.close()
    return map_img, map_angle, map_tl, map_br

def get_frame():
    global camera, map_angle, map_tl, map_br
    ret, frame = camera.read()
    if not ret:
        return 1
    frame = cv2.resize(frame,(640,480))
    frame = rotateImage(frame,map_angle, map_tl)
    frame = frame[map_tl[1]:map_br[1],map_tl[0]:map_br[0]]
    return frame

def update():
    global robot, map_img
    global init_time, last_updated
    global path,pathx,pathy
    global real_map_width, real_map_height

    im = get_frame()
    robot.update_info(time.time()-last_updated,get_robot_xyyaw(im,real_map_height))
    last_updated = time.time()

    # Operações de desenho no plot
    for i in path:
        im[(i[1], i[0])] = [0,0,0]

    pos_im = (int(robot.x*im.shape[1]/real_map_width),im.shape[0]-int(robot.y*im.shape[0]/real_map_height))
    fin_im = (int(pos_im[0]+30*np.cos(robot.yaw)),int(pos_im[1]-30*np.sin(robot.yaw)))
    cv2.arrowedLine(im, pos_im, fin_im,[50,50,50],3)
    cv2.imshow('robot', im)
    if cv2.waitKey(30) & 0xff == 27:
        return 1


    '''
    # Se chegar no ponto final, parar a animação e mostrar infos relevantes
    if(norm((robot.x, robot.y), path[-1]) < 0.02):
        camera.release()
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
            axs[i].grid(True, axis='both')

        plt.show()
    
    '''
    #Algoritmo Pure Pursuit
    '''
    # Encontra a distância lookahead >= 'la', a partir da posição mais próxima
    # 'closest' é a i-ésima posição em path mais próxima (ponto vermelho)
    # 'lookahead_i' é a i-ésima posição do lookahead
    # 'lookahead' é a coordenada da lookahead
    closest, lookahead_i, lookahead = robot.lookahead(path, la=0.1)

    # Plota os pontos lookahead e mais próximo
    ax1.plot([pathx[closest]],[pathy[closest]], marker='o', markersize=3, color="red")
    ax1.plot([pathx[lookahead_i]],[pathy[lookahead_i]], marker='x', markersize=3, color="green")

    # Calcula o novo omega, a partir das informações adquiridas
    current_pos = (robot.x, robot.y)
    next_pos = robot.next_position()
    robot.update_speed(calculate_angle(current_pos,next_pos,lookahead),gain=3)
    '''
    return 0
if __name__ == '__main__':
    _, map_angle, map_tl, map_br = load_map_setup()
    camera = cv2.VideoCapture(0)
    map_img = 1
    while(isinstance(map_img,int)):
        map_img = get_frame()

    robot_features = {
        'width' : 0.18,
        'lenght' : 0.19,
        'wheel_radius' : 0.0315,
        'max_rps' : 1.5
    }
    real_map_width = 2.5 # em metros

    # Conta da altura, em metros, da imagem
    img_height, img_width = real_get_image_dims(map_img)
    real_map_height = img_height*real_map_width/img_width

    # Operações de transformação com o path
    # 1- Transformar em metros
    # 2- Criar pathy e pathx, zipando a lista
    path = path_find(map_img, robot_features['width'], real_map_width/img_width, iters=3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #pathx = []
    #pathy = []
    #for i in range(len(path)):
    #    path[i] = (path[i][0]*real_map_width/img_width, \
    #        real_map_height - real_map_height*path[i][1]/img_height)
    #    pathx.append(path[i][0])
    #    pathy.append(path[i][1])

    # Criação do robô diferencial
    ret,frame = camera.read()
    frame = cv2.resize(frame,(640,480))
    frame = rotateImage(frame,map_angle, map_tl)
    frame = frame[map_tl[1]:map_br[1],map_tl[0]:map_br[0]]
    robot = RealDifferentialDrive(get_robot_xyyaw(frame,real_map_height), \
        robot_features['width'], \
        robot_features['lenght'], \
        robot_features['wheel_radius'], \
        max_rps=robot_features['max_rps'], kp=0.2)

    init_time = time.time()
    last_updated = init_time

    check_ended = 0
    while(check_ended == 0):
        check_ended = update()