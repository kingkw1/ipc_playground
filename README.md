# mindx_ipc
For the MindX coding challenge, this code is used to communicates messages between 2 processes running on the same pc.

In addition to a interprocess communication protocol, this code also includes a message protocol, random data generator, a data file storing system, and unit tests that can be used to evalute the system.

### Table of Contents
1. [File-Description](#file-description)
2. [Set Up](#set-up)
3. [How to Run](#how-to-run)
4. [Solution and Rationale](#solution-and-rationale)
---
### File-Description:

* [__core.messageprotocol.py__](/mindx_ipc/core/messageprotocol.py)
	* Discerns the message protocol from Variables.json file. 
	
* [__core.generator.py__](/mindx_ipc/core/generator.py)
	* Defines the random data generator using inputs from from Variables.json file. 

* [__core.stenographer.py__](/mindx_ipc/core/stenographer.py)
	* Defines the data logging methods. 
	* Each session is saved with an index file, and increasing numbered files.
	* Amount of data saved per numbered file is set in this submodule

* [__core.ipcprotocols.py__](/mindx_ipc/core/ipcprotocols.py)
	* Lays down the common functionality to be used by transfer protocols.

* [__transfer_protocols__](mindx_ipc/transfer_protocols/)
	* Transmission methods for sending and receiving files. 
	* Currently supporting ftp and named_pipes.
	* [template.py](mindx_ipc/transfer_protocols/_template.py) is provided to give core functionality and structure for newly added transfer protocols.
	* Note: all files here inherit from core.ipcprotocols.py, and I've attempted to standardize their usage. Thus, there is some reptition the code within these files. I felt that this was acceptable given the inconsistencies in the transfer protocols main loops -- particularly with respect to the "try" commands.

* [__test_ipc.py__](test_ipc.py)
	* Unit tests for ipc transmission. 
	* Tests standard use transmission (as defined by code challenge guidelines), transmission latency, and maximum transmission speed. 

* [__Variables.json__](Variables.json)
	* Defines the message variable names, format, and functions used to generate randomized data.
	* json format was selected for readability, and ease of modification.
	* See ipc.py for formatting guidelines

* [__MessageRegister.py__](MessageRegister.py)
	* Provides a space for providing definitions to message variables
	* MessageCommands: indicates transmission commands. Currently only "continue" and "stop" are used
	* MessageSource: indicates sender signature. Currently only TEST_PROCESS is being used.
	
* [__main.py__](__main__.py)
	* Enables parsing of command line options. I felt this was much easier to use to demonstrate functionality.
	
---
### Set Up
Easily done with following command from terminal in base directory:
	
	sudo python setup.py install
	
### How to Run
To quickly demonstrate functionality, code can be run in one of two ways:
* Run standard sender and standard receiver in separate terminal windows (in mindx_ipc directory)
	1. python mindx_ipc -r receiver -t named_pipes
	2. python mindx_ipc -r sender -t named_pipes
	* Note: Always run recv_ftp() first, as the sender will not wait for the receiver to join connection.
* Run standard case unit test file in a terminal window (in mindx_ipc directory)
	1. python mindx_ipc
	* Note: This uses parallel processing to run both from the same terminal simultaneously. This option does not work in a Windows machine due to a [documented issue](https://github.com/Axelrod-Python/Axelrod/issues/718) in parallel processing.

### Solution and Rationale
