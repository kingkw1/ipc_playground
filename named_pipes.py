import ipc
from message_regs import MessageSource, MessageCommand
import time
import os
import struct

"""Methods used for inter-process communications using Named Pipes.
"""

_pipename = 'fifo'

class SendingProtocol(ipc.SendingProtocol):
    """Establishes the sending end of the FTP communication.
    """
    def __init__(self):
        super(SendingProtocol, self).__init__()
        print('Attempting to connect...')
        self.pipe = os.fdopen(os.open(_pipename, os.O_NONBLOCK|os.O_WRONLY), 'wb', buffering=0, closefd=False)
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
        self.pipe.write(packed_data)

    def closing_message(self, data):
        """Indicates communication termination.
        """
        print('Sending TERMINATION message with timestamp: ', data[self.message_protocol.headerlist.index('timestamp_s')], ' ', data[self.message_protocol.headerlist.index('timestamp_ns')])

class ReceivingProtocol(ipc.ReceivingProtocol):
    """Establishes the receiving end of the FTP communications.
    """
    def __init__(self):
        super(ReceivingProtocol, self).__init__()

        if os.path.exists(_pipename):
            os.remove(_pipename)
        os.mkfifo(_pipename)

        print('Awaiting connection...')
        self.pipe = os.fdopen(os.open(_pipename, os.O_NONBLOCK|os.O_RDONLY), 'rb', buffering=0)
        print('Receiver Connected!')

    def recv(self):
        """Receives a message from the sender and unpacks it into a tuple.
        """
        # data = self.connection.recv(self.packer.size)
        data = self.pipe.read(self.packer.size)
        unpacked_data = self.decode(data)
        if unpacked_data[self.message_protocol.headerlist.index('mssgtype')] == 0:
            self.closing_message(unpacked_data)
        else:
            print('Received data with timestamp: ', unpacked_data[self.message_protocol.headerlist.index('timestamp_s')], ' ', unpacked_data[self.message_protocol.headerlist.index('timestamp_ns')])
        return unpacked_data

    def close(self):
        self.pipe.close()
        os.remove(_pipename)

    def closing_message(self, data):
        """Indicates communication termination.
        """
        print('Received TERMINATION message with timestamp: ', data[self.message_protocol.headerlist.index('timestamp_s')], ' ', data[self.message_protocol.headerlist.index('timestamp_ns')])

class TransferProtocol(ipc.TransferProtocol):
    def __init__(self):
            super(TransferProtocol, self).__init__()

    def receiver(test_mode = None, testfname = None):
        # Interpret the inputs
        if test_mode:
            print('Testing ', test_mode)

        # Initializations
        receiver = ReceivingProtocol()
        writer = ipc.Stenographer()
        mssgcount = 0

        # Communications
        try:
            if test_mode == 'latency':
                data = None
                while data == None:
                    try:
                        data = receiver.recv()
                    except KeyboardInterrupt:
                        break
                    except:
                        pass
                ts_data = ipc.Generator(MessageSource.TEST_PROCESS.value).generate_timestamp()
                dt = ts_data[0]-data[receiver.message_protocol.headerlist.index('timestamp_s')] + (ts_data[1]-data[receiver.message_protocol.headerlist.index('timestamp_ns')])*(10**-9)*1000
                print("Message Latency: \t", dt,"\t(ms)")
                if testfname:
                    with open(testfname, "a+") as temp_file:
                        temp_file.write("Latency: \t\t%f\t(ms) \n" % dt)
            else:
                # Stream mode
                while True:
                    try:
                        data = receiver.recv()
                        writer.write(data)
                        mssgcount += 1
                        if data[receiver.message_protocol.headerlist.index('mssgtype')] == MessageCommand.CLOSE_COM.value:
                            break
                    except KeyboardInterrupt:
                        print() # line break cuz I'm being overly anal about that stuff
                        break
                    except:
                        # Didn't catch a message. Try again.
                        pass
        finally:
            receiver.close()
            writer.end()

        if test_mode == 'throughput':
            ## ASSUME: Throughput involves a test duration of 1 second.
            print("Maximum Throughput: \t", mssgcount, "\t\t(mssg/sec) \n")
            if testfname:
                with open(testfname, "a+") as temp_file:
                    temp_file.write("Max Throughput: \t%d\t\t(mssg/sec) \n" % mssgcount)

    def sender(send_freq = 60, dur = 2):
        # Interpret the inputs
        sleeptime = 1/send_freq if send_freq!=0 else 0
        singlemode = True if dur == 0 else False

        # Initializations
        sender = SendingProtocol()
        generator = ipc.Generator(MessageSource.TEST_PROCESS.value)
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

        print("Messages sent:  ", mssgcount)
