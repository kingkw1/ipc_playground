import time

class eyemessage():
    def __init__(self, eyed, conf, x, y, d):
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
            self.eyed = 1
            self.conf = 1
            self.xpos = 1
            self.ypos = 1
            self.dia = 1

    def encmssg(self):
        mssg = format(self.timestamp_s,'064b') \
        + format(self.timestamp_ns,'032b') \
        + format(self.eyed,'01b') \
        + format(self.conf,'032b') \
        + format(self.xpos,'032b') \
        + format(self.ypos,'032b') \
        + format(self.dia,'032b')
        return mssg

    def decmssg(mssg):
        timestamp_s = mssg[1:64]
