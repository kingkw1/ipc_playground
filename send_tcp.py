import socket
import eyemessage
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.connect(server_address)

packs = eyemessage.packing()
packer = packs.packorg

try:
    while True:
        mssg = eyemessage.eyedata()
        packed_data = packs.encode(mssg)
        print('Sending mssg', mssg.timestamp_s)
        sock.sendall(packed_data)
        time.sleep(0.02)
except KeyboardInterrupt:
    pass

print('Closing socket')
sock.close()
