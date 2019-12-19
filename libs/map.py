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
        for i,j in ([0,1],[-1,0],[0,-1],[1,0], [1,1], [1,-1], [-1,1], [-1,-1]):
            if (position[0]+i >= 0 and position[0]+i < self.graph.shape[0] and 
                position[1]+j >= 0 and position[1]+j < self.graph.shape[1] and
                self.graph[position[0]+i][position[1]+j] != 0):
                neighbors.append((position[0]+i,position[1]+j))
        return neighbors

    def make_wall(self,position):
        for pos in position:
            self.graph[pos] = 0
