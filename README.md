# mindx_ipc
For the MindX coding challenge, this code sets up a transmission protocol to communicates messages between 2 processes running on the same pc.

---
### CORE FILES FUNCTIONALITY:

* __ipc.py__
	* Discerns the message protocol. 
	* Defines the random data generator, the data logging methods, and data reading methods. 
	* Lays down the common functionality to be used by transmission methods.

* __ftp.py__
	* Transmission methods for sending and receiving files using FTP. 

* __test_ftp.py__
	* Unit tests for ftp transmission. Tests standard use transmission, transmission latency, and maximum transmission speed. 
	* Should be used as a template to build unit tests for alternative transmission protocols.

* __variables.json__
	* Defines the message variable names, format, and functions used to generate randomized data.
	* See ipc.py for formatting guidelines

---
### Implementing
Code can be tested using the "test_ftp.py" file. Code should be run within a terminal in the mindx_ipc directory. Code was developed in a linux machine, and hasn't been tested in windows. 

