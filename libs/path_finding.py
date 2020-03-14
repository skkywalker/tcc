import queue
import math
import numpy as np
from .map import Map
from .get_center import get_center
import cv2
import time
import matplotlib.pyplot as plt

def path_find(img, rob_w, scale, iters, walls_only = 0):
    '''
    Algoritmo Breadth First Search, para encontrar o melhor caminho
    '''
    print("Inicialiazando programa de path-finding...")
    now = time.time()

    # Inicializa o mapa a partir de uma imagem
    im_map = cv2.imread(img, cv2.IMREAD_COLOR)

    # Seta o tamanho da dilatação das parede, para levar em conta
    # a largura do carrinho. 'scale' equivale a relação metro/pixel
    scale = int((rob_w/2)/scale)
    if (scale % 2 == 0): scale += 1
    dilation_kernel = np.ones((scale,scale), np.uint8) 

    # Encontra as posições iniciais e finais
    pos_start = cv2.inRange(im_map, np.array([0,255,0]), np.array([0,255,0]))
    pos_start = get_center(pos_start)
    finish = cv2.inRange(im_map, np.array([255,0,0]), np.array([255,0,0]))  
    finish = get_center(finish)
    size = (len(im_map[0]),len(im_map))

    # Define um objeto mapa, que contém as funções para encontrar o caminho
    graph = Map(start=pos_start,size=size,finish=finish)

    # Cria uma máscara com as paredes (vermelho) e faz a dilatação
    walls = cv2.inRange(im_map, np.array([0,0,50]), np.array([0,0,255]))
    walls = cv2.dilate(walls, dilation_kernel, iterations=iters)
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
