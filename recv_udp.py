import socket
import time
import eyemessage

UDP_IP = '192.168.0.1'
host = ''
UDP_PORT = 1025
bufsize = 1024;

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP,UDP_PORT))

while True:
	data, addr = sock.recv(bufsize)
	print("Message received")
	time.sleep(.01)
