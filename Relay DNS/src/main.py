#!/usr/bin/python3
#coding=utf-8
#__author__ = 'E-Tsai'
#read command
from tests import *
from dnsrelay import *

if __name__ == '__main__':
    server = DNSServer()
    server.runServer()
    # debug()
