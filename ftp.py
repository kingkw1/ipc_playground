from ipc import MessageProtocol, SendingProtocol, ReceivingProtocol, TransferProtocol, Generator, Stenographer
from message_regs import MessageSource, MessageCommand
from abc import ABC, abstractmethod
import socket
import time

"""Methods used for inter-process communications using a file transfer protocol (FTP).
"""

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

class FTPSendingProtocol(SendingProtocol, FTP):
    """Establishes the sending end of the FTP communication.
    """
    def __init__(self):
        super(FTPSendingProtocol, self).__init__()
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

class FTPReceivingProtocol(ReceivingProtocol, FTP):
    """Establishes the receiving end of the FTP communications.
    """
    def __init__(self):
        super(FTPReceivingProtocol, self).__init__()
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
        super(FTPReceivingProtocol, self).close()
        self.connection.close()

class TransferProtocolTest(TransferProtocol):
    def sender(send_freq = 60, dur = 2):
        """
        Generates messages and sends them through the FTP communication system.

        send_freq   float/int   used to determine how long to pause in between sending messages. For no sleep mode use send_freq = 0
        dur         float/int   duration of time to run sender before closing communication. For singlemode (send 1 message) use dur = 0.
        """
        # Interpret the inputs
        sleeptime = 1/send_freq if send_freq!=0 else 0
        singlemode = True if dur == 0 else False

        # Initializations
        sender = FTPSendingProtocol()
        generator = Generator(MessageSource.TEST_PROCESS.value)
        mssgcount = 0

        # Main functionality
        if singlemode:
            data = generator.generate_data_message()
            sender.send(data)
        else:
            start = time.time()
            while time.time()-start < dur:
                data = generator.generate_data_message()
                sender.send(data)
                mssgcount += 1
                time.sleep(sleeptime)
        sender.send(generator.generate_stop_message())
        mssgcount += 1
        sender.close()

        print("Messages sent:  ", mssgcount)

    def receiver(test_mode = None, testfname = None):
        """Receives messages through the FTP communication system, and writes them to a file.

        test_mode           str     identifies the test to be run and the outcome to be reported.
        test_file_name      str     identifies the temporary file to write outcome to.
        """
        # Interpret the inputs
        if test_mode:
            print('Testing ', test_mode)

        # Initializations
        receiver = FTPReceivingProtocol()
        writer = Stenographer()
        mssgcount = 0

        # Communications
        if test_mode == 'latency':

            data = receiver.recv()
            ts_data = Generator(MessageSource.TEST_PROCESS.value).generate_timestamp()
            dt = ts_data[0]-data[receiver.message_protocol.headerlist.index('timestamp_s')] + (ts_data[1]-data[receiver.message_protocol.headerlist.index('timestamp_ns')])*(10**-9)*1000
            print("Message Latency: \t", dt,"\t(ms)")
            if testfname:
                with open(testfname, "a+") as temp_file:
                    temp_file.write("Latency: \t\t%f\t(ms) \n" % dt)
        else:
            try:
                while True:
                    data = receiver.recv()
                    writer.write(data)
                    mssgcount += 1
                    if data[receiver.message_protocol.headerlist.index('mssgtype')] == MessageCommand.CLOSE_COM.value:
                        break
            except KeyboardInterrupt:
                pass

        if test_mode == 'throughput':
            ## ASSUME: Throughput involves a test duration of 1 second.
            print("Maximum Throughput: \t", mssgcount, "\t\t(mssg/sec) \n")
            if testfname:
                with open(testfname, "a+") as temp_file:
                    temp_file.write("Max Throughput: \t%d\t\t(mssg/sec) \n" % mssgcount)

        receiver.close()
        writer.end()

        print("Messages recieved:  ", mssgcount)
