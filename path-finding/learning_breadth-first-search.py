import queue
import numpy as np

class Map:
    def __init__(self,size,start):
        self.graph = np.ones(shape=size, dtype=np.int)
        self.graph[start] = 2
        print(self.graph)

    def get_neighbors(self,position):
        neighbors = list()
        for i,j in ([0,1],[-1,0],[0,-1],[1,0]):
            if ((position[0]+i >= 0 and position[0]+i < self.graph.shape[0]) and 
                (position[1]+j >= 0 and position[1]+j < self.graph.shape[1])):
                neighbors.append((position[0]+i,position[1]+j))
        return neighbors

    def make_wall(self,position):
        for pos in position:
            self.graph[pos] = 0

pos_start = (1,0)
size = (3,4)
graph = Map(start=pos_start,size=size)
graph.make_wall([(0,1),(1,1),(1,2)])
print(graph.graph)
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