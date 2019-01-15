from enum import IntEnum, unique

"""Stores the unique values for interpretting message signatures and command types.

Extra key-value pairs have been added to simply to demonstrate how to modify this file. Not all key-value pairs have not implemented.
"""

@unique
class MessageSource(IntEnum):
    UNKNOWN = 0
    TEST_PROCESS = 1 # Used in testing modules
    SOURCE2 = 2 # Example of an additional source. Change name appropriately

@unique
class MessageCommand(IntEnum):
    CLOSE_COM = 0
    XMIT_DATA = 1
    ERROR = 2
