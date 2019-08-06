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
size = (2,3)
graph = Map(start=pos_start,size=size)

# Start of Redblob algorithm

frontier = queue.Queue()
frontier.put(pos_start)
came_from = {}
came_from[pos_start] = None

while not frontier.empty():
    current = frontier.get()
    for next in graph.get_neighbors(current):
        if next not in came_from:
            frontier.put(next)
            came_from[next] = current

# End of Redblob algorithm

print(came_from)