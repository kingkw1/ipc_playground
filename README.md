# mindx_ipc
For the MindX coding challenge, this code is used to communicates messages between 2 processes running on the same pc.

[COREFUNCTIONALITY](#corefunctionality)
---
### COREFUNCTIONALITY:

* [__ipc.py__](ipc.py)
	* Discerns the message protocol. 
	* Defines the random data generator, the data logging methods, and data reading methods. 
	* Lays down the common functionality to be used by transmission methods.

* [__ftp.py__](ftp.py)
	* Transmission methods for sending and receiving files using FTP. 

* [__test_ftp.py__](test_ftp.py)
	* Unit tests for ftp transmission. Tests standard use transmission, transmission latency, and maximum transmission speed. 
	* Should be used as a template to build unit tests for alternative transmission protocols.

* [__variables.json__](variables.json)
	* Defines the message variable names, format, and functions used to generate randomized data.
	* See ipc.py for formatting guidelines
---
### How to Run
To demonstrate functionality, code can be run in one of two ways:
* Run sender and receiver in separate terminal windows
	1. test_ftp.recv_ftp()
	2. test_ftp.send_ftp()
	* Note: Always run recv_ftp() first, as the sender will not wait for the receiver to join connection.
* Run unit test file in aterminal window
	1. test_ftp
	* Note: This option does not work in a Windows machine due to a [documented issue](https://github.com/Axelrod-Python/Axelrod/issues/718) in parallel processing
	
Code can be tested using the "test_ftp.py" file. Code should be run within a terminal in the mindx_ipc directory. Code was developed and tested on on a linux machine. On a windows machine, unittests must be run individually in order to 
