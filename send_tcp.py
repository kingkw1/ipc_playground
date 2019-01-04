import socket
import eyemessage
import time

# Variables
send_freq = 60 # message send frequency (hz)
nmssgs = 200

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.connect(server_address)

# Send the process signature

# Load the packing methodology
packs = eyemessage.packing()
packer = packs.packorg

sleeptime = 1/send_freq
mssgcount = 0
try:
    while True:
        # TODO: implement selectable timing
        # TODO: implement an additional bit for mssg type (i.e. signature/start, stop, message)
        mssg = eyemessage.eyedata()
        packed_data = packs.encode(mssg)
        print('Sending mssg', mssg.timestamp_s)
        sock.sendall(packed_data)
        mssgcount += 1
        time.sleep(sleeptime)
except KeyboardInterrupt:
    pass

print('Closing socket')
print("Messages recieved:  ", mssgcount)
sock.close()
