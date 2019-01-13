from message_regs import *
from time import time
from datetime import datetime
import random
import os
import json
import functools
import struct
import socket
from abc import ABC, abstractmethod

# TODO: generator functions & Message protocol comment update
# TODO: underscore variables
# TODO: jupyter notebook documentation
# TODO: Readme file updates
# TODO: Scrub the challenge description
class MessageProtocol:
    """Variable file structure unpacked from the designated json file.

    varfile         str     json file name including extension

    ------------
    Variable file should have the following structure:
        {
        header:[headerdict1,headerdict2,...],
        data: [datadict1,datadict2,...]
        }
    Header dicts* should have the following key-value pairs:
        varname     str     name of variable
        varformat   str     "I" or "f" to indicate integer or float when writing to data file
    Data dicts should have the following key-value pairs:
        varname     str     name of variable
        varformat   str     "I" or "f" to indicate integer or float when writing to data file
        genrand     str     stored, uncalled function (no parantheses). Used in generator for unit tests
        randargin   dict    key-value pairs of the argument inputs to the function given in "genrand"

    * Note: The header should have a command type, a sourceid, and a timestamp. Modifications to the header will require additional modifications to the Genearator class for unit tests.
    """
    def __init__(self, varfile = 'variables.json'):
        with open(varfile, 'r') as f:
                all_vars = json.load(f)

        headerlist = []
        varlist = []
        mssgformat = ''
        funlist = []
        for iheadvar in all_vars['headers']:
            headerlist.append(iheadvar['varname'])
            mssgformat += iheadvar['varformat']
        for idatavar in all_vars['data']:
            varlist.append(idatavar['varname'])
            mssgformat += idatavar['varformat']
            if 'randargin' in idatavar:
                funlist.append(functools.partial(eval(idatavar['genrand']),**idatavar['randargin']))
            else:
                funlist.append(eval(idatavar['genrand']))
        self.headerlist = headerlist
        self.varlist = varlist
        self.mssgformat = mssgformat
        self.funlist = funlist

class Generator:
    """"Generator used to make pseudo data used in unittests, as well as stop message to end termination.

    sourceid    int     used as a signature for the data source. For use when multiple data sources are implemented
    """
    def __init__(self, sourceid):
        super(Generator, self).__init__()
        self.sourceid = sourceid
        self.message_protocol = MessageProtocol()

    def generate_timestamp(self):
        """Generate a timestamp for messages using the current time.
        """
        now = time()
        timestamp_s = int(now)
        timestamp_ns = int((now-int(now))*1e9)
        return timestamp_s, timestamp_ns

    def generate_header(self, mssgtype):
        """Generates a header using the format specified in MessageProtocol.
        """
        timestamp_s, timestamp_ns = self.generate_timestamp()
        header = [0]*len(self.message_protocol.headerlist)
        header[self.message_protocol.headerlist.index('timestamp_s')] = timestamp_s
        header[self.message_protocol.headerlist.index('timestamp_ns')] = timestamp_ns
        header[self.message_protocol.headerlist.index('mssgtype')] = mssgtype
        header[self.message_protocol.headerlist.index('mssgsource')] = self.sourceid
        return header

    def generate_data_message(self):
        """Generate a pseudo data message using the given randomization functions designated by "MessageProtocol"
        """
        # Generate header
        mssgtype = MessageCommand.XMIT_DATA.value
        header = self.generate_header(mssgtype)

        # Generate vals from funlist
        data = [f() for f in self.message_protocol.funlist]
        return header + data

    def generate_stop_message(self):
        """Generate a stop message that instructs receiver to terminate transmission.
        """
        # Generate header
        mssgtype = MessageCommand.CLOSE_COM.value
        header = self.generate_header(mssgtype)

        # Generate vals from funlist
        data = [0 for f in self.message_protocol.funlist]
        return header + data

class Stenographer:
    """ Writes data to files. Data are stored in a series of numbered files. The starting data iteration for each file is listed in an index file.

    Files are stored within a timestamped directory which is in the given file directory. An index file lists

    fdir        str     the directory for storing files relative to the current directory
    file_len    int     maximum number of data points per file
    """
    def __init__(self, fdir = 'test_data', file_len = 1000):
        """Opens up the index file and the first data file. Indicates the write format.
        """
        super(Stenographer, self).__init__()
        self.file_len = file_len
        self.filedataiter = 0
        self.fileiter = 0
        self.alldataiter = 0
        self.message_protocol = MessageProtocol()

        # Make the datastore folder
        if not os.path.exists(fdir):
            os.makedirs(fdir)

        # Make the session data folder
        ts = datetime.fromtimestamp(time()).strftime('%Y%m%d_%H%M%S')
        os.makedirs(os.path.join(os.getcwd(),fdir, ts))
        self.filedir = os.path.join(os.getcwd(),fdir, ts)

        # Write the index file
        indexpath = os.path.join(self.filedir,'index.txt')
        self.index = open(indexpath,'w')

        # Open the file for writing and add header
        self.newfile()

        # Create the write format to inform write command
        ## ASSUME: Anything that isn't a float is an integer
        f_ind = [index for index, value in enumerate(self.message_protocol.mssgformat.lower()) if value == 'f']
        writeformat = list("d"*len(self.message_protocol.mssgformat))
        for ind in f_ind:
            writeformat[ind] = "f"

        self.writeformat = "%" + ",%".join(writeformat) + "\n" # skip message type

    def write(self, data):
        """Adds data point to numbered data file.

        data    tuple   MessageProtocol following the format designated in the variables json file
        """
        # Check how many data points have been written
        if self.dataiter >= self.file_len:
            self.newfile()

        self.file.write(self.writeformat % tuple(data))
        self.dataiter += 1
        self.alldataiter += 1

    def newfile(self):
        """Creates a new data file and updates the index file.
        """
        self.dataiter = 0
        if hasattr(self,'file'):
            self.close()
            self.fileiter += 1

        filepath = os.path.join(self.filedir,str(self.fileiter)+'.csv')
        self.file = open(filepath,'w')
        self.file.write(','.join(self.message_protocol.headerlist + self.message_protocol.varlist)+'\n')
        self.index.write(str(self.alldataiter)+'\n')

    def close(self):
        """Closes the current data file.
        """
        self.file.close()

    def end(self):
        """Closes the current data file and index.
        """
        if hasattr(self,'file'):
            self.close()

        self.index.close()

class SendingProtocol(ABC):
    """Defines the structure of sending protocols and provides the message encoding method.
    """
    def __init__(self):
        self.message_protocol = MessageProtocol()
        self.packer = struct.Struct(self.message_protocol.mssgformat)

    @abstractmethod
    def send(self):
        pass

    def encode(self, data):
        """Encodes a message into the message format defined by the variables json file.

        data    tuple   MessageProtocol following the format designated in the variables json file
        """
        self.packer = struct.Struct(self.message_protocol.mssgformat)
        mssg = self.packer.pack(*data)
        return mssg

class ReceivingProtocol(ABC): # should this inherit packer also?
    """Defines the structure of receiving protocols and provides the message unpacking method.
    """
    def __init__(self):
        self.message_protocol = MessageProtocol()
        self.packer = struct.Struct(self.message_protocol.mssgformat)

    @abstractmethod
    def recv(self):
        pass

    def decode(self, mssg):
        """Decodes a message using the  message format defined by the variables json file.

        mssg    bytes   message in the mssgformat defined by the variables json file.
        """
        data = self.packer.unpack(mssg)
        return data
