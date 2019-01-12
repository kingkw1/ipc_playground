from ipc import *

class FTP(ABC):
    """Designates the server address and socket properties needed for FTP.
    """
    def __init__(self):
        self.server_address = ('localhost', 10000)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class FTPSender(SendingProtocol, FTP):
    """Establishes the sending end of the FTP communication.
    """
    def __init__(self):
        FTP.__init__(self)
        SendingProtocol.__init__(self)
        print('Attempting to connect...')
        self.sock.connect(self.server_address)
        print('Sender Connected!')

    def send(self, data):
        """Sends given message through the socket

        data    tuple   Variables following the format designated in the variables json file
        """
        if data[0] == 0:
            print('Terminal mssg with timestamp: ', data[self.varlist.index('timestamp_s')], ' ', data[self.varlist.index('timestamp_ns')])
        else:
            print('Sending data with timestamp: ', data[self.varlist.index('timestamp_s')], ' ', data[self.varlist.index('timestamp_ns')])
        packed_data = self.encode(data)
        self.sock.sendall(packed_data)

    def close(self):
        """Closes the communication on the senders end.
        """
        print('Ending Transmission...')
        self.sock.close()

class FTPReceiver(ReceivingProtocol, FTP):
    """Establishes the receiving end of the FTP communications.
    """
    def __init__(self):
        FTP.__init__(self)
        ReceivingProtocol.__init__(self)
        self.sock.bind(self.server_address)
        self.sock.listen(1)
        print('Awaiting connection...')
        self.connection, client_address = self.sock.accept()
        print('Receiver Connected!')

    def recv(self):
        """Receives a message from the sender and unpacks it into a tuple.
        """
        data = self.connection.recv(self.packer.size)
        unpacked_data = self.decode(data)
        if unpacked_data[0] == 0:
            print('Terminal mssg with timestamp: ', unpacked_data[self.varlist.index('timestamp_s')], ' ', unpacked_data[self.varlist.index('timestamp_ns')])
        else:
            print('Received data with timestamp: ', unpacked_data[self.varlist.index('timestamp_s')], ' ', unpacked_data[self.varlist.index('timestamp_ns')])
        return unpacked_data

    def close(self):
        """Closes the communication on the receiver end.
        """
        print("Ending Transmission...")
        self.connection.close()
        self.sock.close()
