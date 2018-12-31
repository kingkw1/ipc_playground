import time
import random
import struct

"""
Conversions from: https://stackoverflow.com/questions/8751653/how-to-convert-a-binary-string-into-a-float-value
"""
def bin_to_float(b):
    """ Convert 32bit binary string to a float. """
    bf = int_to_bytes(int(b, 2), 4)  # 8 bytes needed for IEEE 754 binary64.
    return struct.unpack('>f', bf)[0]

def int_to_bytes(n, minlen=0):  # Helper function
    """ Int/long to byte string. """
    nbits = n.bit_length() + (1 if n < 0 else 0)  # +1 for any sign bit.
    nbytes = (nbits+7) // 8  # Number of whole bytes.
    b = bytearray()
    for _ in range(nbytes):
        b.append(n & 0xff)
        n >>= 8
    if minlen and len(b) < minlen:  # Zero padding needed?
        b.extend([0] * (minlen-len(b)))
    return bytearray(reversed(b))  # High bytes first.

def float_to_bin(value):  # For testing.
    """ Convert float to 32-bit binary string. """
    [d] = struct.unpack(">l", struct.pack(">f", value))
    return '{:032b}'.format(d)

#def bin2float32(bin32):
#    return struct.unpack('f', struct.pack('I', bin32))[0]
#
#def float2bin32(f32):
#    return ''.join(bin(ord(c)).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', f32))
#
class eyemessage():
    def __init__(self, eyed=None, conf=None, x=None, y=None, d=None):
        """
        Timestamp : Seconds: Int64U, Nanoseconds: Int32U
	       Timestamp of message received
        ID : Boolean
        	0 – left eye, 1 – right eye
        Confidence : Float32
        	0 – no confidence, 1 – perfect confidence
        NormalizedPosX : Float32
        	Normalized x-coordinate of the pupil location, 0 – left, 1 – right
        NormalizedPosY : Float32
        	Normalized y-coordinate of the pupil location, 0 – bottom, 1 – top
        PupilDiameter : Int32U
        	Diameter of the pupil in image pixels
        """
        now = time.time()
        self.timestamp_s = int(now)
        self.timestamp_ns = int((now-int(now))*1e9)

        if eyed and conf and x and y and d:
            self.eyed = eyed
            self.conf = conf
            self.xpos = x
            self.ypos = y
            self.dia = d
        else:
            self.eyed = random.randint(0,1)
            self.conf = random.random()
            self.xpos = random.random()
            self.ypos = random.random()
            self.dia = random.randrange(1,500)

    def encbinmssg(self):
        mssg = format(self.timestamp_s,'064b') \
        + format(self.timestamp_ns,'032b') \
        + format(self.eyed,'01b') \
        + float_to_bin(self.conf) \
        + float_to_bin(self.xpos) \
        + float_to_bin(self.ypos) \
        + format(self.dia,'032b')
        return mssg

def decmssg(mssg):
    # a = [0,64,32,1,32,32,32,32]
    timestamp_s = int(mssg[0:64],2)
    timestamp_ns = int(mssg[64:96],2)
    eyed = mssg[96:97]
    conf = bin_to_float(mssg[97:129])
    xpos = bin_to_float(mssg[129:161])
    ypos = bin_to_float(mssg[161:193])
    dia = int(mssg[193:225],2)
    return timestamp_s, timestamp_ns, eyed, conf, xpos, ypos, dia

#a = eyemessage().encbinmssg()
