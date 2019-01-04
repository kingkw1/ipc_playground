import socket
import eyemessage

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.bind(server_address)
sock.listen(1)

packs = eyemessage.packing()
unpacker = packs.packorg
agg = eyemessage.aggregator('test_tcp.txt')
mssgcount = 0

print('\nwaiting for a connection')
connection, client_address = sock.accept()

# signature

# Data transmission body
try:
    while True:
        data = connection.recv(unpacker.size)
        # TODO: implement "Terminate" message

        unpacked_data = packs.decode(data)
        agg.write(eyemessage.eyedata(unpacked_data))
        print('Recieved mssg:', unpacked_data[0])
        mssgcount += 1
except KeyboardInterrupt:
    pass

connection.close()
print("Messages recieved:  ", mssgcount)
