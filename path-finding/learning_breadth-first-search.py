import queue
import numpy as np

class Map:
    def __init__(self,size,start):
        self.size = size
        self.graph = np.ones(shape=(self.size[0],self.size[1]), dtype=np.int)
        self.graph[start[0]][start[1]] = 0
        print(self.graph)

    def get_neighbors(self,position):
        neighbors = list()
        for i,j in ([0,1],[-1,0],[0,-1],[1,0]):
            if ((position[0]+i >= 0 and position[0]+i < self.graph.shape[0]) and 
                (position[1]+j >= 0 and position[1]+j < self.graph.shape[1])):
                neighbors.append((position[0]+i,position[1]+j))
        return neighbors              

pos_start = (1,1)
size = (5,3)
graph = Map(start=pos_start,size=size)