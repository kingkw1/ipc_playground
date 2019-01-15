import sys, getopt
from test_ipc import IPCTestCase
import os
import unittest
import importlib

def main(argv):
    run_mode = None
    transfer_protocol = None
    try:
        opts, args = getopt.getopt(argv,"i:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('BAD INPUT')
        print('mindx_ipc -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-help':
            sys.exit()
        else:
            print("Argument input pair not recognized")

# Get the TransferProtocol
try:
    modname = 'transfer_protocols.' + transfer_protocol
    tp = importlib.import_module(modname)
except:
    raise FileNotFound('Could not find specified transfer protocol')

if __name__ == "__main__":
    # Step into main directory
    cwd = os.getcwd()
    os.chdir(os.path.join(cwd,'mindx_ipc'))

    # Operations based on input run_mode
    if run_mode == 'test':
        class TempTestCase(IPCTestCase):
            TransferProtocol = tp.TransferProtocol

        suite =  unittest.TestLoader().loadTestsFromTestCase(TempTestCase)
        unittest.TextTestRunner(verbosity=2).run(suite)

    elif run_mode == "sender":
        s = tp.TransferProtocol.sender()

    elif run_mode == "receiver":
        r = tp.TransferProtocol.receiver()

    else:
        print('run_mode not implemented.')

    os.chdir(cwd)
