# mindx_ipc
For the MindX coding challenge, this code is used to communicates messages between 2 processes running on the same pc.

In addition to a interprocess communication protocol, this code also includes a message protocol, random data generator, a data file storing system, and unit tests that can be used to evalute the system.

### Table of Contents
1. [File-Description](#file-description)
2. [How to Run](#how-to-run)
3. [Solution and Rationale](#solution-and-rationale)
---
### File-Description:

* [__ipc.py__](ipc.py)
	* Discerns the message protocol. 
	* Defines the random data generator, the data logging methods, and data reading methods. 
	* Lays down the common functionality to be used by transmission methods.

* [__ftp.py__](ftp.py)
	* Transmission methods for sending and receiving files using FTP. 

* [__test_ipc.py__](test_ipc.py)
	* Unit tests for ipc transmission. Tests standard use transmission, transmission latency, and maximum transmission speed. 
	* Should be used as a template to build unit tests for alternative transmission protocols.

* [__variables.json__](variables.json)
	* Defines the message variable names, format, and functions used to generate randomized data.
	* See ipc.py for formatting guidelines
---
### How to Run
To demonstrate functionality, code can be run in one of two ways:
* Run standard sender and standard receiver in separate terminal windows
	1. test_ipc.IPCTestCase().recv_ftp()
	2. test_ipc.IPCTestCase().send_ftp()
	* Note: Always run recv_ftp() first, as the sender will not wait for the receiver to join connection.
* Run standard case unit test file in a terminal window
	1. test_ipc.IPCTestCase.test_standard()
	* Note: This option does not work in a Windows machine due to a [documented issue](https://github.com/Axelrod-Python/Axelrod/issues/718) in parallel processing.

### Solution and Rationale

