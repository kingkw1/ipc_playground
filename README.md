# mindx_ipc
For the MindX coding challenge, this code sets up a transmission protocol to communicates messages between 2 processes running on the same pc.

Code can be tested using the "test_ftp.py" file. Code should be run within a terminal in the code directory. Code was developed in a linux machine, and hasn't been tested in windows (but socket based ipc should work on windows also). 


Core files breakdown:

BCICodeChallenge.docx
	Describes the challenge goals and evaluation criteria

ipc.py
	Discerns the message variables. Defines the random data generator, the data logging methods, and data reading methods. Lays down the common core functionality to be used by transmission methods.

ftp.py
	Modular transmission method for sending and receiving files using FTP. Alternative transmission methods can be written and used to replace this.

test_ftp.py
	Unit tests for ftp transmission. Tests standard use transmission, transmission latency, and maximum transmission speed. Should be used as a template to build unit tests for alternative transmission protocols.

variables.json
	Defines the message variable names, format, and functions used to generate randomized data.
	
