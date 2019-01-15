from core.messageprotocol import MessageProtocol
import os
from time import time
from datetime import datetime

_data_dir = 'DataStore'

class Stenographer:
    """ Writes data to files. Data are stored in a series of numbered files. The starting data iteration for each file is listed in an index file.

    Files are stored within a timestamped directory which is in the given file directory. An index file lists

    fdir        str     the directory for storing files relative to the current directory
    file_len    int     maximum number of data points per file
    """
    def __init__(self, fdir = _data_dir, file_len = 1000):
        super(Stenographer, self).__init__()
        self.file_len = file_len
        self.__fileiter = 0
        self.__alldataiter = 0
        self.message_protocol = MessageProtocol()

        # Make the datastore folder
        if not os.path.exists(fdir):
            os.makedirs(fdir)

        # Make the session data folder
        ts = datetime.fromtimestamp(time()).strftime('%Y%m%d_%H%M%S')
        os.makedirs(os.path.join(os.getcwd(),fdir, ts))
        self.filedir = os.path.join(os.getcwd(),fdir, ts)

        # Make the index file
        indexpath = os.path.join(self.filedir,'index.txt')
        self.index = open(indexpath,'w')

        # Open a new file for writing
        self.newfile()

        # Create the write format to inform write command
        ## ASSUME: Anything that isn't a float is an integer. No strings allowed
        f_ind = [index for index, value in enumerate(self.message_protocol.mssgformat.lower()) if value == 'f']
        writeformat = list("d"*len(self.message_protocol.mssgformat))
        for ind in f_ind:
            writeformat[ind] = "f"

        self.writeformat = "%" + ",%".join(writeformat) + "\n"

    def write(self, data):
        """Adds data point to numbered data file.

        data    tuple   Data following the format designated MessageProtocol
        """
        # Check how many data points have been written
        if self.__filedataiter >= self.file_len:
            self.newfile()

        self.file.write(self.writeformat % tuple(data))
        self.__filedataiter += 1
        self.__alldataiter += 1

    def newfile(self):
        """Creates a new data file and updates the index file.
        """
        # Reset current file data iteration and increment the file iteration
        self.__filedataiter = 0
        if hasattr(self,'file'):
            self.close()
            self.__fileiter += 1

        # Create the new file
        filepath = os.path.join(self.filedir,str(self.__fileiter)+'.csv')
        self.file = open(filepath,'w')
        self.file.write(','.join(self.message_protocol.headerlist + self.message_protocol.varlist)+'\n')

        # Update the index file
        self.index.write(str(self.__alldataiter)+'\n')

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
