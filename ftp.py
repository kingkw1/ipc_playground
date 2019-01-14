from ipc import MessageProtocol, SendingProtocol, ReceivingProtocol, socket
from abc import ABC, abstractmethod

class FTP(ABC):
    """Designates the server address and socket properties needed for FTP.
    """
    def __init__(self):
        super(FTP, self).__init__()
        self.server_address = ('localhost', 10000)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_protocol = MessageProtocol()

    def closing_message(self, data):
        """Indicates communication termination.
        """
        print('Closing mssg with timestamp: ', data[self.message_protocol.headerlist.index('timestamp_s')], ' ', data[self.message_protocol.headerlist.index('timestamp_ns')])

    def close(self):
        """Closes the FTP transmission socket.
        """
        print("Ending Transmission...")
        self.sock.close()

class FTPSender(SendingProtocol, FTP):
    """Establishes the sending end of the FTP communication.
    """
    def __init__(self):
        super(FTPSender, self).__init__()
        print('Attempting to connect...')
        self.sock.connect(self.server_address)
        print('Sender Connected!')

    def send(self, data):
        """Sends given message through the socket

        data    tuple   MessageProtocol following the format designated in the variables json file
        """
        if data[self.message_protocol.headerlist.index('mssgtype')] == 0:
            self.closing_message(data)
        else:
            print('Sending data with timestamp: ', data[self.message_protocol.headerlist.index('timestamp_s')], ' ', data[self.message_protocol.headerlist.index('timestamp_ns')])
        packed_data = self.encode(data)
        self.sock.sendall(packed_data)

class FTPReceiver(ReceivingProtocol, FTP):
    """Establishes the receiving end of the FTP communications.
    """
    def __init__(self):
        super(FTPReceiver, self).__init__()
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
        if unpacked_data[self.message_protocol.headerlist.index('mssgtype')] == 0:
            self.closing_message(unpacked_data)
        else:
            print('Received data with timestamp: ', unpacked_data[self.message_protocol.headerlist.index('timestamp_s')], ' ', unpacked_data[self.message_protocol.headerlist.index('timestamp_ns')])
        return unpacked_data

    def close(self):
        """Closes the FTP connection.
        """
        super(FTPReceiver, self).close()
        self.connection.close()
