import time
import random
import os
import json
import functools
import struct
from abc import ABC, abstractmethod

"""
TODO: Use following code to monitor ram usage and timings:
import ipython_memory_usage.ipython_memory_usage as imu
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
        self.packer = struct.Struct(mssgformat)
        self.funlist = funlist

class MessageGenerator(MessageVariables):
    def generate_timestamp(self):
        now = time.time()
        timestamp_s = int(now)
        timestamp_ns = int((now-int(now))*1e9)
        return timestamp_s, timestamp_ns

    def generate_random_data(self, sourceid = 1):
        # Generate header & timestamps (header = 1 for datamssg)
        mssgtype = 1
        timestamp_s, timestamp_ns = self.generate_timestamp()
        headerlist = [mssgtype, sourceid, timestamp_s, timestamp_ns]

        # Generate vals from funlist
        datalist = [f() for f in self.funlist]
        return headerlist + datalist

    def generate_com_messg(self , sourceid = 1, mssg_type = 0):
        # Generate header & timestamps (header = 1 for mssg)
        timestamp_s, timestamp_ns = self.generate_timestamp()
        headerlist = [mssgtype, sourceid, timestamp_s, timestamp_ns]

        # Generate vals from funlist
        datalist = [0 for f in self.funlist]
        return headerlist + datalist

class Packer(MessageVariables):
    def encode(self, data):
        mssg = self.packer.pack(data)
        return mssg

    def decode(self, mssg):
        data = self.packer.unpack(mssg)
        return data

class Transmsission(ABC): # should this inherit packer also?
    def __init__(self):
        pass

    @abstractmethod
    def send(self):
        pass

    @abstractmethod
    def recv(self):
        pass

class FTProtocol(Transmission):
    def __init__(self):
        a = 0
