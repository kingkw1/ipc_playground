import socket
import struct
import time
import eyemessage

UDP_IP = '192.168.0.1'
UDP_PORT = 1025

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

while True:
	# Generate message contents
	mssg = eyemessage.encbinmssg()

    # Pack the message
	MESSAGE = struct.pack('!dddddd', mssg)

    # Send the message
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
	print("Message sent")

    # Wait to send next message
	time.sleep(.1)
