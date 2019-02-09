from transfer_protocols.ftp import TransferProtocol as tp
from core.stenographer import _data_dir
import time
from multiprocessing import Process
from numpy import diff, sign
import pandas
import unittest
import os

""" Provides the test cases to be used for all transfer protocols.
UnitTests is best demonstrated in either of 2 ways.

    1) cmd terminal: python ipc_playground
        - Use when in the ipc_playground outer directory
        - Use inputs to select the Transfer Protocol desired
    2) cmd terminal: python test_ipc.py
        - Use while in the ipc_playground inner directory (ipc_playground/ipc_playground)
        - manually modify the imported transfer_protocol above to make selection
"""

_testfname = "unittestresults.temp"
_inter_test_pause_dur = 1 # Time to close the socket and file between tests and avoid errors.
_sender_receiver_latency = 0.1 # Time between start of receiver and start of sender.
_throughput_dur = 1 # How long the sender will transmit messages to the receiver.

class IPCTestCase(unittest.TestCase):
    """Unit tests for inter process communication"""

    TransferProtocol = tp

    def test_standard(self):
        """
        Tests the IPC system by running the system at 60Hz and reading data from the first saved data file. Timestamps from the data are checked for incremental increase.
        """
        # Prepare the sender and receiver processes
        receiver = Process(target=self.TransferProtocol.receiver)
        sender = Process(target=self.TransferProtocol.sender, args=(60,2,))

        # Start the processes
        receiver.start()
        time.sleep(_sender_receiver_latency) # Necessary to ensure that receiver starts before sender
        sender.start()

        # Wait until processes complete and join together to primary thread
        receiver.join()
        sender.join()

        # Check the data directory for newest file
        fname = '0.csv'
        data_dir_list= os.listdir(_data_dir)
        data_dir_list.sort()
        filepath = os.path.join(os.getcwd(),_data_dir,data_dir_list[0],fname)

        # Read newest file data and evaluate timestamps
        data = pandas.read_csv(filepath, header = 0, delimiter=',')
        ts = data.timestamp_s + data.timestamp_ns*(10**-9)
        self.assertTrue(all(sign(diff(ts))==1))

        # Pause to ensure sockets and files closed successfully
        time.sleep(_inter_test_pause_dur)

    def test_throughput(self):
        """Tests the IPC system in no sleep mode for 1 second to determine the maximum rate of transmission.
        """
        receiver = Process(target=self.TransferProtocol.receiver, args=('throughput',_testfname,))
        sender = Process(target=self.TransferProtocol.sender, args=(0,_throughput_dur,))

        receiver.start()
        time.sleep(_sender_receiver_latency) # Necessary to ensure that receiver starts before sender
        sender.start()

        receiver.join()
        sender.join()
        time.sleep(_inter_test_pause_dur)

    def test_latency(self):
        """Sends a single message through the defined protocol, and times it. Specifically, it evaluates the time to complete the following steps:
            1. packing & sending a messages
            2. receiving & unpacking a message
            3. generating a timestamp for comparison
        """
        # Prepare the sender and receiver processes
        receiver = Process(target=self.TransferProtocol.receiver, args=('latency',_testfname,))
        sender = Process(target=self.TransferProtocol.sender, args=(0,0,))

        # Start the processes
        receiver.start()
        time.sleep(_sender_receiver_latency) # Necessary to ensure that receiver starts before sender
        start_time = time.time() # Start timer to evaluate message sending latency
        sender.start()

        # Wait until processes complete and join together to primary thread
        receiver.join()
        sender.join()
        time.sleep(_inter_test_pause_dur)

    @classmethod
    def setUpClass(cls):
        """Deletes the temporary file used to store test results, if one somehow was left over.
        """
        if os.path.exists(_testfname):
            os.remove(_testfname)

    @classmethod
    def tearDownClass(cls):
        """Prints out the test results stored in the temporary file and then deletes the file.
        """
        print()
        print('---------------------------------------------------------------------')
        print('UNIT TEST SUMMARY:')
        print()
        print()

        with open(_testfname, 'r') as fin:
            print(fin.read())
        if os.path.exists(_testfname):
            os.remove(_testfname)

if __name__ == "__main__":
    unittest.main()
