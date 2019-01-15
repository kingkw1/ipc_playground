from test_ipc import IPCTestCase
import sys
import getopt
import os
import unittest
import importlib

"""Manage user inputs to code to enable easier switching between transfer protocols."""

def usage():
    print()
    print('usage: mindx_ipc [-m <run_mode>] [-t <transfer_protocol>]')
    print()
    print('   run_modes supported: \t\t test (default), sender, receiver')
    print('   transfer_protocols supportd: \t named_pipes (default), ftp')
    print()

def main(argv):
    # Defaults
    run_mode = 'test'
    transfer_protocol = 'named_pipes'

    # Get Inputs & deploy them to variables
    try:
        opts, args = getopt.getopt(argv,"hr:t:",["help","run_mode=","transfer_protocol="])
    except getopt.GetoptError as err:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        if opt == '-r':
            print('Received run_mode: ', arg)
            run_mode = arg
        if opt == '-t':
            print('Received transfer_protocol: ', arg)
            transfer_protocol = arg
        else:
            pass

    # Retreive the TransferProtocol
    try:
        modname = 'transfer_protocols.' + transfer_protocol
        tp = importlib.import_module(modname)
    except:
        raise FileNotFound('Could not find specified transfer protocol')

    # Complete the requested run
    try:
        # Step into main directory
        cwd = os.getcwd()
        os.chdir(os.path.join(cwd,'mindx_ipc'))

        # Operations based on input run_mode
        if run_mode == 'test':
            class TempTestCase(IPCTestCase):
                TransferProtocol = tp.TransferProtocol

            suite =  unittest.TestLoader().loadTestsFromTestCase(TempTestCase)
            unittest.TextTestRunner(verbosity=2).run(suite)
            print('Completed test of: ', transfer_protocol)

        # Standard sender
        elif run_mode == "sender":
            try:
                s = tp.TransferProtocol.sender()
                print('Completed run of: ', transfer_protocol)
            except:
                print("Remember to run receiver before sender")

        # Standard receiver
        elif run_mode == "receiver":
            r = tp.TransferProtocol.receiver()
            print('Completed run of: ', transfer_protocol)

        else:
            print('run_mode not implemented.')

    # Return to the original directory
    finally:
        os.chdir(cwd)

if __name__ == "__main__":
    # skip the 0 input, which is currently running script name.
    main(sys.argv[1:])
