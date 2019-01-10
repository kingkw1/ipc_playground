import time
import datetime
import random
import os
import pandas
import json
import functools
import struct
import socket
from abc import ABC, abstractmethod

class Variables:
    """Variable file structure unpacked from the json file.

    varfile -- string containing json file name including extension
    """
    def __init__(self, varfile = 'variables.json'):
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
    """ Writes data to files.
    """
    def __init__(self, fdir = 'test_data', file_len = 1000):
        super(Stenographer, self).__init__()
        self.file_len = file_len
        self.dataiter = 0
        self.fileiter = 0

        # Make the data folder
        if not os.path.exists(fdir):
            os.makedirs(fdir)

        # Make the session data folder
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
        os.makedirs(os.path.join(os.getcwd(),fdir, ts))
        self.filedir = os.path.join(os.getcwd(),fdir, ts)

        # Open the file for writing and add header
        self.newfile()

        # Create the write format
        ## ASSUME: Anything that isn't a float is an integer
        f_ind = [index for index, value in enumerate(self.mssgformat.lower()) if value == 'f']
        writeformat = list("d"*len(self.mssgformat))
        for ind in f_ind:
            writeformat[ind] = "f"

        self.writeformat = "%" + ",%".join(writeformat[1:]) + "\n" # skip message type

    def write(self, data):
        # TODO: Look into buffering
        # Check how many data points have been written
        if self.dataiter >= self.file_len:
            self.newfile()

        self.file.write(self.writeformat % tuple(data[1:]))
        self.dataiter += 1

    def newfile(self):
        self.dataiter = 0
        if hasattr(self,'file'):
            self.close()
            self.fileiter += 1

        filepath = os.path.join(self.filedir,str(self.fileiter)+'.csv')
        self.file = open(filepath,'w')
        self.file.write(','.join(self.varlist[1:])+'\n')

    def close(self):
        self.file.close()

def read_data(filepath):
    """Reads in all data to a data_frame, using pandas."""
    return pandas.read_csv(filepath, header = 0, delimiter=',')

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
