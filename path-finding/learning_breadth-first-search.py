import queue
import numpy as np
from map import Map

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

graph.mk_image(path)
