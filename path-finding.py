import queue
import numpy as np
from libs.map import Map
import libs.tools as tools
import cv2
import time

print("Starting program...")
print("Setting up map from image...")
now = time.time()

im_map = cv2.imread('src/test-map.png', cv2.IMREAD_COLOR)

dilation_kernel = np.ones((11,11), np.uint8) 

pos_start = cv2.inRange(im_map, np.array([0,255,0]), np.array([0,255,0]))
pos_start = tools.get_center(pos_start)
finish = cv2.inRange(im_map, np.array([255,0,0]), np.array([255,0,0]))  
finish = tools.get_center(finish)
size = (len(im_map[0]),len(im_map))

graph = Map(start=pos_start,size=size,finish=finish)

walls = cv2.inRange(im_map, np.array([0,0,50]), np.array([0,0,255]))
walls = cv2.dilate(walls, dilation_kernel, iterations=3)
cv2.imshow('walls', walls)
walls = cv2.findNonZero(walls)

for point in walls:
    point = (point[0][0],point[0][1])
    graph.make_wall([point])

print("Map setup! Time:", round(time.time() - now, 2), "sec")
print("Initializing path-finding algorithm...")
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

current = finish
path = []
while current != pos_start:
    path.append(current)
    current = came_from[current]
path.append(pos_start)
path.reverse()

print("Path found! Time:", round(time.time() - now, 2), "sec")

print("Preparing to show map...")
for i in path:
    im_map[(i[1], i[0])] = [0,0,0]

# End of Redblob algorithm

cv2.imshow('path chosen', im_map)

print("Done!")
cv2.waitKey(0)
cv2.destroyAllWindows()
