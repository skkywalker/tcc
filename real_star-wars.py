import socket
import time

def playSound(dest, tone, beats):
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect(dest)
    print(tone)
    tcp.send(tone)
    time.sleep(0.01)
    tcp.close()
    time.sleep(beats/bps)

DO = 2*bytes([65])
RE = 2*bytes([75])
MI = 2*bytes([83])
FA = 2*bytes([90])
SOL = 2*bytes([100])
DO2 = 2*bytes([130])

notes = [DO, SOL, FA, MI, RE, DO2, SOL, FA, MI, RE, DO2, SOL, FA, MI, FA, RE]
beats = [2,2,1/3,1/3,1/3,2,1,1/3,1/3,1/3,2,1,1/3,1/3,1/3,2]


dest = ('192.168.1.181', 8888)
bps = 108/60

for i,note in enumerate(notes):
    playSound(dest, note, beats[i])

playSound(dest,2*bytes([0]), 1)