from enum import IntEnum

class MessageSource(IntEnum):
    UNKNOWN = 0
    TEST_PROCESS = 1 # Used in testing modules
    SOURCE2 = 2 # Example of an additional source. Change name appropriately

class MessageCommand(IntEnum):
    CLOSE_COM = 0
    XMIT_DATA = 1
    ERROR = 2
