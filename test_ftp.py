import ftp
import time
from multiprocessing import Process
from numpy import diff, sign
import unittest
import os

class FTPTestCase(unittest.TestCase):
    """Unit tests for ftp.py"""
    inter_test_pause_dur = 0.2 # Time to close the socket between tests and avoid errors.

    def send_ftp(self, send_freq = 60, dur = 2):
        """
        Generates messages and sends them through the FTP communication system.

        send_freq   float/int   used to determine how long to pause in between sending messages. For no sleep mode use send_freq = 0
        dur         float/int   duration of time to run sender before closing communication
        """
        # Initializations
        sleeptime = 1/send_freq if send_freq!=0 else 0
        mssgcount = 0
        nmssgs = send_freq*dur
        sender = ftp.FTPSender()
        generator = ftp.Generator()

        try:
            start = time.time()
            while time.time()-start < dur:
                data = generator.generate_data_message()
                sender.send(data)
                mssgcount += 1
                time.sleep(sleeptime)
        except KeyboardInterrupt:
            pass

        sender.send(generator.generate_stop_message())
        sender.close()

        print("Messages sent:  ", mssgcount)

    def recv_ftp(self):
        """Receives messages through the FTP communication system, and writes them to a file.
        """
        receiver = ftp.FTPReceiver()
        writer = ftp.Stenographer()

        mssgcount = 0
        try:
            while True:
                data = receiver.recv()
                if data[0] == 0:
                    break
                else:
                    writer.write(data)
                    mssgcount += 1
        except KeyboardInterrupt:
            pass

        receiver.close()
        writer.end()

        print("Messages recieved:  ", mssgcount)

    def test_standard(self):
        """
        Tests the FTP system by running the system at 60Hz and reading data from the first saved data file. Timestamps from the data are checked for incremental increase.
        """
        filename = '0.csv'

        sender = Process(target=self.send_ftp, args=(60,2))
        receiver = Process(target=self.recv_ftp)

        receiver.start()
        time.sleep(0.1) # Necessary to ensure that receiver starts before sender
        sender.start()

        receiver.join()
        sender.join()
        time.sleep(self.inter_test_pause_dur)

        data_dir = 'test_data'
        fname = '0.csv'
        data_dir_list= os.listdir(data_dir)
        data_dir_list.sort()
        filepath = os.path.join(os.getcwd(),data_dir,data_dir_list[0],fname)

        data = ftp.read_data(filepath)
        ts = data.timestamp_s + data.timestamp_ns*(10**-9)
        self.assertTrue(all(sign(diff(ts))==1))

    def test_speed(self):
        """Tests the FTP communication system in no sleep mode to determine the maximum rate of transmission.
        """
        sender = Process(target=self.send_ftp, args=(0,1))
        receiver = Process(target=self.recv_ftp)

        receiver.start()
        time.sleep(0.1) # Necessary to ensure that receiver starts before sender
        sender.start()

        receiver.join()
        sender.join()
        time.sleep(self.inter_test_pause_dur)

if __name__ == "__main__":
    unittest.main()
