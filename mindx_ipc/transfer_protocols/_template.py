import ipc
from MessageDescriptors.MessageRegister import MessageSource, MessageCommand
import time
# IMPORT ALL THE REST OF THE THINGS

"""Template for inter-process communications.
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
        packed_data = self.encode(data)
        # Send

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
        unpacked_data = self.decode(data)
        if unpacked_data[self.message_protocol.headerlist.index('mssgtype')] == 0:
            self.closing_message(unpacked_data)
        else:
            print('Received data with timestamp: ', unpacked_data[self.message_protocol.headerlist.index('timestamp_s')], ' ', unpacked_data[self.message_protocol.headerlist.index('timestamp_ns')])
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

                        if test_mode == 'throughput' and mssgcount == 0:
                            first_data_pt = data

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
            ts_data = ipc.Generator(MessageSource.TEST_PROCESS.value).generate_timestamp()
            dur = ts_data[0]-first_data_pt[receiver.message_protocol.headerlist.index('timestamp_s')] + (ts_data[1]-first_data_pt[receiver.message_protocol.headerlist.index('timestamp_ns')])*(10**-9)
            throughput = round(mssgcount/dur)
            print("Messages Transmitted: \t\t", mssgcount, "\t\tmssg")
            print("Communication Duration: \t", dur, "\tsec")
            print("Resulting Throughput: \t\t", throughput, "\t\t(mssg/sec)")
            if testfname:
                with open(testfname, "a+") as temp_file:
                    temp_file.write("Throughput: \t%d\t\t(mssg/sec) \n" % throughput)

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
