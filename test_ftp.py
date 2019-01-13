import ftp
import time
from multiprocessing import Process
from numpy import diff, sign
import pandas
import unittest
import os

inter_test_pause_dur = 1 # Time to close the socket and file between tests and avoid errors.
sender_receiver_latency = 0.1 # Time between start of receiver and start of sender.

class FTPTestCase(unittest.TestCase):
    """Unit tests for ftp.py"""
    def send_ftp(self, send_freq = 60, dur = 2):
        """
        Generates messages and sends them through the FTP communication system.

        send_freq   float/int   used to determine how long to pause in between sending messages. For no sleep mode use send_freq = 0
        dur         float/int   duration of time to run sender before closing communication. For singlemode (send 1 message) use dur = 0.
        """
        # Initializations
        sleeptime = 1/send_freq if send_freq!=0 else 0
        singlemode = True if dur == 0 else False

        sender = ftp.FTPSender()
        generator = ftp.Generator(ftp.MessageSource.TEST_PROCESS.value)
        mssgcount = 0

        # Main function loop
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

    def recv_ftp(self, singlemode = False):
        """Receives messages through the FTP communication system, and writes them to a file.

        singlemode  Bool    Receives a single message and calculates the transmission latency. Sender should also be set to singlemode.
        """
        # Initializations
        receiver = ftp.FTPReceiver()
        writer = ftp.Stenographer()
        mssgcount = 0

        # Main function loop
        if singlemode:
            data = receiver.recv()
            ts_data = ftp.Generator(ftp.MessageSource.TEST_PROCESS.value).generate_timestamp()
            dt = ts_data[0]-data[receiver.message_protocol.headerlist.index('timestamp_s')] + (ts_data[1]-data[receiver.message_protocol.headerlist.index('timestamp_ns')])*(10**-9)
            print("Message latency: ", dt)
        else:
            try:
                while True:
                    data = receiver.recv()
                    writer.write(data)
                    mssgcount += 1
                    if data[receiver.message_protocol.headerlist.index('mssgtype')] == ftp.MessageCommand.CLOSE_COM.value:
                        break
            except KeyboardInterrupt:
                pass
        receiver.close()
        writer.end()

        print("Messages recieved:  ", mssgcount)

    def test_standard(self):
        """
        Tests the FTP system by running the system at 60Hz and reading data from the first saved data file. Timestamps from the data are checked for incremental increase.
        """
        # Prepare the sender and receiver processes
        sender = Process(target=self.send_ftp, args=(60,2,))
        receiver = Process(target=self.recv_ftp)

        # Start the processes
        receiver.start()
        time.sleep(sender_receiver_latency) # Necessary to ensure that receiver starts before sender
        sender.start()

        # Wait until processes complete and join together to primary thread
        receiver.join()
        sender.join()

        # Check the data directory for newest file
        data_dir = 'test_data'
        fname = '0.csv'
        data_dir_list= os.listdir(data_dir)
        data_dir_list.sort()
        filepath = os.path.join(os.getcwd(),data_dir,data_dir_list[0],fname)

        # Read newest file data and evaluate timestamps
        data = pandas.read_csv(filepath, header = 0, delimiter=',')
        ts = data.timestamp_s + data.timestamp_ns*(10**-9)
        self.assertTrue(all(sign(diff(ts))==1))

        # Pause to ensure sockets and files closed successfully
        time.sleep(inter_test_pause_dur)

    def test_throughput(self):
        """Tests the FTP communication system in no sleep mode to determine the maximum rate of transmission.
        """
        sender = Process(target=self.send_ftp, args=(0,1,))
        receiver = Process(target=self.recv_ftp)

        receiver.start()
        time.sleep(sender_receiver_latency) # Necessary to ensure that receiver starts before sender
        sender.start()

        receiver.join()
        sender.join()
        time.sleep(inter_test_pause_dur)

    def test_latency(self):
        """Sends a single message through the defined protocol, and times it. Specifically, it evaluates the time to complete the following steps:
            1. packing & sending a messages
            2. receiving & unpacking a message
            3. generating a timestamp for comparison
        """
        # Prepare the sender and receiver processes
        sender = Process(target=self.send_ftp, args=(0,0,))
        receiver = Process(target=self.recv_ftp, args=(True,))

        # Start the processes
        receiver.start()
        time.sleep(sender_receiver_latency) # Necessary to ensure that receiver starts before sender
        start_time = time.time() # Start timer to evaluate message sending latency
        sender.start()

        # Wait until processes complete and join together to primary thread
        receiver.join()
        sender.join()

        time.sleep(inter_test_pause_dur)

if __name__ == "__main__":
    unittest.main()
