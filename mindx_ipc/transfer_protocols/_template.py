from core import ipcprotocols as ipc
from MessageDescriptors.MessageRegister import MessageSource, MessageCommand
import time

"""Template for inter-process communications.
NOTE: This file is not meant to be used as an IPC itself.
"""

class SendingProtocol(ipc.SendingProtocol):
    """Establishes the sending end of the IPC communication.
    """
    def __init__(self):
        super(SendingProtocol, self).__init__()
        print('Attempting to connect...')
        # Connect
        print('Sender Connected!')

    def send(self, data):
        """Sends given message through the socket

        data    tuple   MessageProtocol following the format designated in the variables json file
        """
        if data[self.message_protocol.headerlist.index('mssgtype')] ==  MessageCommand.CLOSE_COM.value:
            self.closing_message(data)
        else:
            print('Sending data with timestamp: ', data[self.message_protocol.headerlist.index('timestamp_s')], ' ', data[self.message_protocol.headerlist.index('timestamp_ns')])

        # Pack data
        # Send data

    def closing_message(self, data):
        """Indicates communication termination.
        """
        print('Sending TERMINATION message with timestamp: ', data[self.message_protocol.headerlist.index('timestamp_s')], ' ', data[self.message_protocol.headerlist.index('timestamp_ns')])

class ReceivingProtocol(ipc.ReceivingProtocol):
    """Establishes the receiving end of the IPC communication.
    """
    def __init__(self):
        super(ReceivingProtocol, self).__init__()

        # Setup
        print('Awaiting connection...')
        # Connect
        print('Receiver Connected!')

    def recv(self):
        """Receives a message from the sender and unpacks it into a tuple.
        """
        # Receive Data
        # Interpret Data
        if unpacked_data[self.message_protocol.headerlist.index('mssgtype')] == 0:
            self.closing_message(unpacked_data)
        else:
            print('Received data with timestamp: ', unpacked_data[self.message_protocol.headerlist.index('timestamp_s')], ' ', unpacked_data[self.message_protocol.headerlist.index('timestamp_ns')])

        # Return Data
        return unpacked_data

    def closing_message(self, data):
        """Indicates communication termination.
        """
        print('Received TERMINATION message with timestamp: ', data[self.message_protocol.headerlist.index('timestamp_s')], ' ', data[self.message_protocol.headerlist.index('timestamp_ns')])

class TransferProtocol(ipc.TransferProtocol):
    """Protocol for transferring messages using IPC.
    """
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
        ## Include cases for latency and throughput test_mode's

    def sender(send_freq = 60, dur = 2):
        # Interpret the inputs
        sleeptime = 1/send_freq if send_freq!=0 else 0
        singlemode = True if dur == 0 else False

        # Initializations
        sender = SendingProtocol()
        generator = ipc.Generator(MessageSource.TEST_PROCESS.value)
        mssgcount = 0

        # Communications

        print("Messages sent:  ", mssgcount)
