"""
Author: Jamal Alhariri
Assignment: #2
Description: Port Scanner — A tool that scans a target machine for open network ports
"""

import socket
import threading
import sqlite3
import os
import platform
import datetime

print("Python version:", platform.python_version())
print("OS name:", os.name)

# Stores common port numbers and their usual service names
common_ports = {
    20: "FTP-Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP",
    68: "DHCP",
    69: "TFTP",
    80: "HTTP",
    110: "POP3",
    123: "NTP",
    143: "IMAP",
    161: "SNMP",
    179: "BGP",
    443: "HTTPS",
    587: "SMTP Secure",
    993: "IMAP Secure",
    995: "POP3 Secure"
}


class NetworkTool:
    def __init__(self, target):
        self.__target = target

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, value):
        if value != "":
            self.__target = value

    def __del__(self):
        print("NetworkTool instance destroyed")


# Q3: What is the benefit of using @property and @target.setter?
# They help control how the target value is accessed and changed.
# Instead of letting any value be assigned directly, the setter can check the input first.
# This makes the program safer and helps protect the data inside the object.


# Q1: How does PortScanner reuse code from NetworkTool?
# PortScanner inherits from NetworkTool, so it reuses the target attribute and its getter and setter.
# This avoids writing the same code again in the child class.
# It also makes the design cleaner by keeping shared behavior in one parent class.