import time
import random
import os
import json
import functools

varfile = 'data_vars.json'

with open(varfile, 'r') as f:
        data_vars = json.load(f)

class mssgvar:
    def __init__(self, vardict):
        self.varname = vardict['varname']
        self.varformat =  vardict['varformat']
        self.genrand = functools.partial(eval(vardict['genrand']),**vardict['randargin'])

class mssgstruct:
    def __init__(self,data_vars):
        self.packorg =[]
        for ivar in data_vars:
            mssgvar[vardict]

class AccelerometerData(Icm20689Data):
    def __init__(self, x_val, y_val, z_val):
        self.x_val = x_val

    def serialize(self):
        return struct.pack('!ddd', self.x_val, self.y_val, self.z_val)

    def __repr__(self):
        return "%lf %lf %lf" % (self.x_val, self.y_val, self.z_val)

class datamssg:
    def __init__(self):
        now = time.time()
        self.timestamp_s = int(now)
        self.timestamp_ns = int((now-int(now))*1e9)
