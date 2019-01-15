from core.messageprotocol import MessageProtocol
from MessageRegister import MessageCommand
import random
import time

class Generator:
    """"Generator used to make pseudo data used in unittests, as well as stop message to end termination.

    sourceid    int     used as a signature for the data source. For use when multiple data sources are implemented
    """
    def __init__(self, sourceid):
        self.sourceid = sourceid
        self.message_protocol = MessageProtocol()

    def generate_timestamp(self):
        """Generate a timestamp for messages using the current time.
        """
        now = time.time()
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

        # Generate data values from funlist
        data = [f() for f in self.message_protocol.funlist]
        return header + data

    def generate_stop_message(self):
        """Generate a stop message that instructs receiver to terminate transmission.
        """
        # Generate header
        mssgtype = MessageCommand.CLOSE_COM.value
        header = self.generate_header(mssgtype)

        # Use 0s for variables
        data = [0 for f in self.message_protocol.funlist]
        return header + data
