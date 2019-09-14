import numpy as np
from matplotlib import pyplot

class Map:
    def __init__(self,size,start,finish):
        self.size = size
        self.start = start
        self.finish = finish
        self.graph = np.ones(shape=size, dtype=np.int)
        self.graph[start] = 2
        self.graph[finish] = 3

    def get_neighbors(self,position):
        neighbors = list()
        for i,j in ([0,1],[-1,0],[0,-1],[1,0]):
            if (position[0]+i >= 0 and position[0]+i < self.graph.shape[0] and 
                position[1]+j >= 0 and position[1]+j < self.graph.shape[1] and
                self.graph[position[0]+i][position[1]+j] != 0):
                neighbors.append((position[0]+i,position[1]+j))
        return neighbors

    def make_wall(self,position):
        for pos in position:
            self.graph[pos] = 0

    def mk_image(self,path):
        img = self.graph

        for tup in path:
            img[tup] = 4
        img[self.start] = 2
        img[self.finish] = 3

        scale_factor = 1
        img = np.kron(img, np.ones((scale_factor,scale_factor)))
        for i in range(self.size[0]*scale_factor):
            for j in range(self.size[1]*scale_factor):
                if(img[i][j] == 1):
                    img[i][j] = 255
                elif(img[i][j] == 2 or img[i][j] == 3):
                    img[i][j] = 130
                elif(img[i][j] == 4):
                    img[i][j] = 180
                else:
                    img[i][j] = 0
        pyplot.imshow(img, cmap='gray')
        pyplot.show()
