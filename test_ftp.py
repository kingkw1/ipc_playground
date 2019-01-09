import ftp
import time
from multiprocessing import Process
from numpy import diff, sign
import sys
import unittest

class FTPTestCase(unittest.TestCase):
    """Unit tests for ftp.py"""
    inter_test_pause_dur = 0.2 # Time to close the socket between tests and avoid errors.

    def send_ftp(self, send_freq = 60, dur = 2):
        """
        For no sleep mode, send_freq = 0
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

    def recv_ftp(self, fname='test_ftp.csv'):
        receiver = ftp.FTPReceiver()
        writer = ftp.Stenographer(fname)

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
        writer.close()
        print("Messages recieved:  ", mssgcount)

    def test_standard(self):
        """
        Checks standard use case -- running code at designated speed and checking timestamps for increment.
        """
        filename = 'test_ftp.csv'

        sender = Process(target=self.send_ftp, args=(60,2))
        receiver = Process(target=self.recv_ftp, args=(filename,))

        receiver.start()
        time.sleep(0.1) # Necessary to ensure that receiver starts before sender
        sender.start()

        receiver.join()
        sender.join()
        time.sleep(self.inter_test_pause_dur)

        data = ftp.read_data(filename)
        ts = data.timestamp_s + data.timestamp_ns*(10**-9)
        self.assertTrue(all(sign(diff(ts))==1))

    def test_speed(self):
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
