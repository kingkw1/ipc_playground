import time
import random
import os
import json
import functools

"""
Use following code to monitor ram usage and timings:
import ipython_memory_usage.ipython_memory_usage as imu
"""
varfile = 'variables.json'

with open(varfile, 'r') as f:
        all_vars = json.load(f)

varlist = []
packlist = ''
funlist = []
for iheadvar in all_vars['headers']:
    varlist.append(iheadvar['varname'])
    packlist += iheadvar['varformat']

for idatavar in all_vars['data']:
    varlist.append(idatavar['varname'])
    packlist += idatavar['varformat']
    if 'randargin' in idatavar:
        funlist.append(functools.partial(eval(idatavar['genrand']),**idatavar['randargin']))
    else:
        funlist.append(eval(idatavar['genrand']))

def genmssgvals():
    # Generate timestamps
    # Generate vals from funlist
    return mssg

class mssgvar:
    def __init__(self, vardict):
        self.varname = vardict['varname']
        self.varformat =  vardict['varformat']
        self.genrand = functools.partial(eval(vardict['genrand']),**vardict['randargin'])

class datamssg:
    __slots__ = ('x','y')
    def __init__(self, x, y):
        self.x = 0
        self.y = 0
    def genrand(self):
        self.x = 1
        self.y = 1
