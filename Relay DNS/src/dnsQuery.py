#!/usr/bin/python3
#coding=utf-8
#__author__ = 'E-Tsai'
#dns query

import threading
import time
import struct
import socketserver
import socket

class DnsQuery:
    # from question part, get domain address which need to be queried
    def __init__(self, data):
        i = 1
        self.domain = ''
        self.ip = ''
        while True:
            d = data[i]
            if d == 0:
                #ASCII = 0, then end up the deal
                break
            elif d < 32:
                #Add '.' between domain address
                self.domain += '.'
            else:
                self.domain += chr(d)
            i += 1
        self.package = data[0: i + 1]
        (self.type, self.classify) = struct.unpack('!HH', data[i + 1: i + 5])
        self.len = i + 5

    def get_bytes(self):
        return self.package + struct.pack('!HH', self.type, self.classify)

class DnsAnswer:
    # write the answer part in dns package if needs
    def __init__(self, ip):
        self.name = 49164
        self.type = 1
        self.classify = 1
        self.ttl = 190
        self.datalength = 4
        self.ip = ip

    def get_bytes(self):
        pack = struct.pack('!HHHLH', self.name, self.type, self.classify, self.ttl, self.datalength)
        iplist = self.ip.split('.')
        pack = pack + struct.pack('BBBB', int(iplist[0]), int(iplist[1]), int(iplist[2]), int(iplist[3]))
        return pack