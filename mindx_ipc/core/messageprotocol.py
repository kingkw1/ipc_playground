import json
import functools
import random

_varfile = 'Variables.json'

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
    def __init__(self, varfile = _varfile):
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
