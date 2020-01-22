import queue
import math
import numpy as np
from ..map import Map
from ..get_center import get_center
from .color import color
import cv2
import time
import matplotlib.pyplot as plt

def read_filter(name, mapa, lower, upper):
    ret = cv2.inRange(mapa, lower, upper)
    ret = cv2.morphologyEx(ret, cv2.MORPH_CLOSE, np.ones([4,4]))
    ret = cv2.morphologyEx(ret, cv2.MORPH_OPEN, np.ones([4,4]))
    cv2.imshow(name, ret)
    ret = get_center(ret)
    return ret

def path_find(im_map, rob_w, scale, iters, walls_only = 0):
    '''
    Algoritmo Breadth First Search, para encontrar o melhor caminho
    '''
    print("Inicialiazando programa de path-finding...")
    now = time.time()

    # Seta o tamanho da dilatação das parede, para levar em conta
    # a largura do carrinho. 'scale' equivale a relação metro/pixel
    scale = math.floor((rob_w/2)/scale)
    dilation_kernel = np.ones((scale,scale), np.uint8) 

    verm, am, verd = color('vermelho'),color('amarelo'),color('verde')
    # Encontra as posições iniciais e finais
    pos_start = read_filter('pos_start', im_map, verm[0], verm[1])
    finish = read_filter('finish', im_map, am[0], am[1])
    size = (len(im_map[0]),len(im_map))

    # Define um objeto mapa, que contém as funções para encontrar o caminho
    graph = Map(start=pos_start,size=size,finish=finish)

    # Cria uma máscara com as paredes (verde) e faz a dilatação
    walls = cv2.inRange(im_map, verd[0], verd[1])
    walls = cv2.morphologyEx(walls, cv2.MORPH_OPEN, np.ones([5,5]))
    walls = cv2.morphologyEx(walls, cv2.MORPH_CLOSE, np.ones([5,5]))
    walls = cv2.dilate(walls, dilation_kernel, iterations=iters)
    cv2.imshow('walls',walls)

    wall_img_backup = walls.copy()

    # Se quiser observar apenas as paredes dilatadas, passe
    # wall_only para a função
    if(walls_only):
        print("Mostrando as paredes e saindo...")
        cv2.imshow('walls', walls)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        exit(1)

    # Define as paredes no objeto mapa (como graph)
    walls = cv2.findNonZero(walls)

    for point in walls:
        point = (point[0][0],point[0][1])
        graph.make_wall([point])

    print("Mapa inicializado! Tempo:", round(time.time() - now, 2), "sec")
    print("Iniciando algoritmo...")
    now = time.time()

    '''
    Início do algorítmo Breadth First Search
    (Obrigado Redblob!)
    https://www.redblobgames.com/pathfinding/a-star/introduction.html
    '''

    frontier = queue.Queue()
    frontier.put(pos_start)
    came_from = {}
    came_from[pos_start] = None

    while not frontier.empty():
        current = frontier.get()
        
        if current == finish:
            break
        
        for n in graph.get_neighbors(current):
            if n not in came_from:
                frontier.put(n)
                came_from[n] = current

    # Se não encontrar nenhum caminho disponivel, 'finish' não estará
    # no dicionário, então saímos do programa antes do erro.
    try:
        tmp = came_from[finish]
        print("Algoritmo encerrado!")
        print("Preparando a lista 'path'...")
    except KeyError:
        print("Nenhum caminho encontrado! Mostrando as paredes e saindo...")
        cv2.imshow('walls', wall_img_backup)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        exit(1)

    # Para encontrar o menor caminho, vamos andando para trás no dicionário
    # e anotando por onde passamos.
    current = finish
    path = []
    while current != pos_start:
        path.append(current)
        current = came_from[current]
    
    # Coloque o início no path e inverte a ordem do vetor 
    path.append(pos_start)
    path.reverse()

    print("Caminho encontrado! Time:", round(time.time() - now, 2), "sec")

    return path
