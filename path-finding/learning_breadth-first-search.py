import queue
import numpy as np

class Map:
    def __init__(self,size,start,finish):
        self.graph = np.ones(shape=size, dtype=np.int)
        self.graph[start] = 2
        self.graph[finish] = 3
        print(self.graph)

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
        print(self.graph)

pos_start = (1,0)
finish = (0,2)
size = (3,4)
graph = Map(start=pos_start,size=size,finish=finish)
graph.make_wall([(0,1),(1,1),(1,2)])

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

current = finish
path = []
while current != pos_start:
    path.append(current)
    current = came_from[current]
path.append(pos_start)
path.reverse()

# End of Redblob algorithm

print(path)