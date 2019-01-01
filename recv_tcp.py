import socket
import eyemessage

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.bind(server_address)
sock.listen(1)
packs = eyemessage.packing()
unpacker = packs.packorg

print('\nwaiting for a connection')
connection, client_address = sock.accept()

try:
    while True:
        data = connection.recv(unpacker.size)
        unpacked_data = packs.decode(data)
        print('Recieved mssg:', unpacked_data[0])
except KeyboardInterrupt:
    pass

connection.close()
