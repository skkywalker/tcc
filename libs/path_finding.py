import queue
import math
import numpy as np
from .map import Map
from .get_center import get_center
import cv2
import time
import matplotlib.pyplot as plt

def path_find(img, rob_w, scale, walls_only = 0):
    print("Inicialiazando programa de path-finding...")
    now = time.time()

    im_map = cv2.imread(img, cv2.IMREAD_COLOR)

    scale = math.floor((rob_w/2)/scale) # (L/2+segurança)/(tamanho metros/tamanho pixels)
    dilation_kernel = np.ones((scale,scale), np.uint8) 

    pos_start = cv2.inRange(im_map, np.array([0,255,0]), np.array([0,255,0]))
    pos_start = get_center(pos_start)
    finish = cv2.inRange(im_map, np.array([255,0,0]), np.array([255,0,0]))  
    finish = get_center(finish)
    size = (len(im_map[0]),len(im_map))

    graph = Map(start=pos_start,size=size,finish=finish)

    walls = cv2.inRange(im_map, np.array([0,0,50]), np.array([0,0,255]))
    walls = cv2.dilate(walls, dilation_kernel, iterations=3)
    wall_img_backup = walls.copy()

    if(walls_only):
        print("Mostrando as paredes e saindo...")
        cv2.imshow('walls', walls)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        exit(1)

    walls = cv2.findNonZero(walls)

    for point in walls:
        point = (point[0][0],point[0][1])
        graph.make_wall([point])

    print("Mapa inicializado! Tempo:", round(time.time() - now, 2), "sec")
    print("Iniciando algoritmo...")
    now = time.time()

    # Start of Redblob algorithm

    frontier = queue.Queue()
    frontier.put(pos_start)
    came_from = {}
    came_from[pos_start] = None

    while not frontier.empty():
        current = frontier.get()
        
        if current == finish:
            break
        
        for next in graph.get_neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current
    try:
        tmp = came_from[finish]
    except KeyError:
        print("Nenhum caminho encontrado! Mostrando as paredes e saindo...")
        cv2.imshow('walls', wall_img_backup)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        exit(1)

    current = finish
    path = []
    while current != pos_start:
        path.append(current)
        current = came_from[current]
    path.append(pos_start)
    path.reverse()

    print("Caminho encontrado! Time:", round(time.time() - now, 2), "sec")

    print("Mostrando mapa...")
    for i in path:
        im_map[(i[1], i[0])] = [0,0,0]

    # End of Redblob algorithm

    #plt.imshow(im_map)
    #plt.show()

    return path
