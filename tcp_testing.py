import socket
import time

def playSound(dest, tone, beats):
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect(dest)
    tcp.send(tone.encode())
    data = tcp.recv(1)
    tcp.close()
    time.sleep(beats/bps)

DO = '065065'
RE = '075075'
MI = '083083'
FA = '090090'
SOL = '100100'
DO2 = '130130'

notes = [DO, SOL, FA, MI, RE, DO2, SOL, FA, MI, RE, DO2, SOL, FA, MI, FA, RE]
beats = [2,2,1/3,1/3,1/3,2,1,1/3,1/3,1/3,2,1,1/3,1/3,1/3,2]


dest = ('192.168.1.172', 8888)
bps = 108/60

for i,note in enumerate(notes):
    playSound(dest, note, beats[i])

playSound(dest,'000000', 1)