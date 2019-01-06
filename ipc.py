import time
import random
import os
import csv # this is used by reader
import json
import functools
import struct
import socket
from message_regs import *
from abc import ABC, abstractmethod

"""
TODO: Use following code to monitor ram usage and timings:
import ipython_memory_usage.ipython_memory_usage as imu

TODO: Implement the message_regs
"""

class Variables:
    def __init__(self, varfile = 'variables.json'):
        """Unpack the variable file structure"""
        with open(varfile, 'r') as f:
                all_vars = json.load(f)

        varlist = []
        mssgformat = ''
        funlist = []
        for iheadvar in all_vars['headers']:
            varlist.append(iheadvar['varname'])
            mssgformat += iheadvar['varformat']
        for idatavar in all_vars['data']:
            varlist.append(idatavar['varname'])
            mssgformat += idatavar['varformat']
            if 'randargin' in idatavar:
                funlist.append(functools.partial(eval(idatavar['genrand']),**idatavar['randargin']))
            else:
                funlist.append(eval(idatavar['genrand']))
        self.varlist = varlist
        self.mssgformat = mssgformat
        self.funlist = funlist

class Generator(Variables):
    def __init__(self, sourceid = 1):
        super(Generator, self).__init__()
        self.sourceid = sourceid

    def generate_timestamp(self):
        now = time.time()
        timestamp_s = int(now)
        timestamp_ns = int((now-int(now))*1e9)
        return timestamp_s, timestamp_ns

    def generate_data_message(self):
        # Generate header
        mssgtype = 1
        timestamp_s, timestamp_ns = self.generate_timestamp()
        headerlist = [mssgtype, self.sourceid, timestamp_s, timestamp_ns]

        # Generate vals from funlist
        datalist = [f() for f in self.funlist]
        return headerlist + datalist

    def generate_stop_message(self):
        # Generate header
        mssgtype = 0
        timestamp_s, timestamp_ns = self.generate_timestamp()
        headerlist = [mssgtype, self.sourceid, timestamp_s, timestamp_ns]

        # Generate vals from funlist
        datalist = [0 for f in self.funlist]
        return headerlist + datalist

class Stenographer(Variables):
    def __init__(self, fname, fdir = 'test_datastore'):
        super(Stenographer, self).__init__()

        # Open the file for writing and add header
        self.file = open(os.path.join(os.getcwd(),fdir,fname),'w')

        # Write the header, listing variables
        self.file.write(', '.join(self.varlist[1:])+'\n')

        # Create the write format
        ## ASSUME: Anything that isn't a float is an integer
        f_ind = [index for index, value in enumerate(self.mssgformat.lower()) if value == 'f']
        writeformat = list("d"*len(self.mssgformat))
        for ind in f_ind:
            writeformat[ind] = "f"

        self.writeformat = "%" + ", %".join(writeformat[1:]) + "\n" # skip message type

    def write(self, data):
        # TODO: Look into buffering
        self.file.write(self.writeformat % tuple(data[1:]))

    def close(self):
        self.file.close()

class Reader(Variables):
    # TODO: implement reader
    def __init__(self, fname, fdir = 'test_datastore'):
        super(Reader, self).__init__()
        self.file = open(os.path.join(os.getcwd(),fdir,fname),"r")
        # Gather data as list. Store as variables to self

class SendingProtocol(ABC, Variables): # should this inherit packer also?
    def __init__(self):
        Variables.__init__(self)
        self.packer = struct.Struct(self.mssgformat)

    @abstractmethod
    def send(self):
        pass

    def encode(self, data):
        self.packer = struct.Struct(self.mssgformat)
        mssg = self.packer.pack(*data)
        return mssg

    # TODO: implement "Terminate" message

class ReceivingProtocol(ABC, Variables): # should this inherit packer also?
    def __init__(self):
        Variables.__init__(self)
        self.packer = struct.Struct(self.mssgformat)

    @abstractmethod
    def recv(self):
        pass

    def decode(self, mssg):
        data = self.packer.unpack(mssg)
        return data

class FTP(ABC):
    def __init__(self):
        self.server_address = ('localhost', 10000)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class FTPSender(SendingProtocol, FTP):
    def __init__(self):
        FTP.__init__(self)
        SendingProtocol.__init__(self)
        print('\nAttempting to connect...')
        self.sock.connect(self.server_address)
        print('Connected!')

    def send(self, data):
        if data[0] == 0:
            print('Terminal mssg with timestamp: ', data[self.varlist.index('timestamp_s')])
        else:
            print('Sending data with timestamp: ', data[self.varlist.index('timestamp_s')])
        packed_data = self.encode(data)
        self.sock.sendall(packed_data)

    def close(self):
        print('Ending Transmission...')
        self.sock.close()

class FTPReceiver(ReceivingProtocol, FTP):
    def __init__(self):
        FTP.__init__(self)
        ReceivingProtocol.__init__(self)
        self.sock.bind(self.server_address)
        self.sock.listen(1)
        print('\nAwaiting connection...')
        self.connection, client_address = self.sock.accept()
        print('Connected!')

    def recv(self):
        data = self.connection.recv(self.packer.size)
        unpacked_data = self.decode(data)
        if unpacked_data[0] == 0:
            print('Terminal mssg with timestamp: ', unpacked_data[self.varlist.index('timestamp_s')])
        else:
            print('Received data with timestamp: ', unpacked_data[self.varlist.index('timestamp_s')])
        return unpacked_data

    def close(self):
        print("Ending Transmission...")
        self.connection.close()
