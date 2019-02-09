from core.messageprotocol import MessageProtocol
import struct
from abc import ABC, abstractmethod

class SendingProtocol(ABC):
    """Defines the structure of sending protocols and provides the message encoding method.
    """
    def __init__(self):
        super(SendingProtocol, self).__init__()
        self.message_protocol = MessageProtocol()
        self.packer = struct.Struct(self.message_protocol.mssgformat)

    @abstractmethod
    def send(self):
        pass

    def encode(self, data):
        """Encodes a message into the message format defined by the MessageProtocol.

        data    tuple   Data following the format designated MessageProtocol
        """
        self.packer = struct.Struct(self.message_protocol.mssgformat)
        mssg = self.packer.pack(*data)
        return mssg

class ReceivingProtocol(ABC): # should this inherit packer also?
    """Defines the structure of receiving protocols and provides the message decoding method.
    """
    def __init__(self):
        super(ReceivingProtocol, self).__init__()
        self.message_protocol = MessageProtocol()
        self.packer = struct.Struct(self.message_protocol.mssgformat)

    @abstractmethod
    def recv(self):
        pass

    def decode(self, mssg):
        """Decodes a message using the  message format defined by the MessageProtocol.

        mssg    bytes   Message following the format designated MessageProtocol
        """
        data = self.packer.unpack(mssg)
        return data

class TransferProtocol(ABC): # should this inherit packer also?
    """Defines the structure of transfer protocols. Transfer protocols must have a sender and a receiver.
    """
    def __init__(self):
        super(TransferProtocol, self).__init__()

    @abstractmethod
    def sender(self):
        pass

    @abstractmethod
    def receiver(self):
        pass
