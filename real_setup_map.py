from libs.real.get_map import get_map_clicking
import cv2

map_img, rotate_angle, tl, br = get_map_clicking()

cv2.imwrite('map_setup/map.png', map_img)
f = open('map_setup/rotate_angle', 'w')
f.write(str(rotate_angle))
f.close()
f = open('map_setup/tl', 'w')
f.write(str(tl))
f.close()
f = open('map_setup/br', 'w')
f.write(str(br))
f.close()