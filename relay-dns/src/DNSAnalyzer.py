#!/usr/bin/python3
#coding=utf-8
#__author__ = 'E-Tsai'
#DNS analyzer

import struct

class DNSQuestion:
    def __init__(self, data):
        i = 1
        self.domain = ''
        self.ip = ''
        while True:
            d = data[i]
            if d == 0:
                break
            elif d < 32:
                self.domain += '.'
            else:
                self.domain += chr(d)
            i += 1
        self.package = data[0: i + 1]
        (self.qtype, self.qclass) = struct.unpack('!HH', data[i + 1: i + 5])
        self.len = i + 5

    def get_bytes(self):
        return self.package + struct.pack('!HH', self.qtype, self.qclass)

class DNSRRF:
    def __init__(self, ip):
        self.name = 49164
        self.qtype = 1
        self.qclass = 1
        self.ttl = 200
        self.datalength = 4
        self.ip = ip

    def get_bytes(self):
        pack = struct.pack('!HHHLH', self.name, self.qtype, self.qclass, self.ttl, self.datalength)
        iplist = self.ip.split('.')
        pack = pack + struct.pack('BBBB', int(iplist[0]), int(iplist[1]), int(iplist[2]), int(iplist[3]))
        return pack

class DNSAnalyzer:

    def __init__(self, data):
        (self.Id, self.Flags, self.QdCount, self.AnCount, self.NsCount, self.ArCount) = \
            struct.unpack('!HHHHHH', data[0: 12])
        
        # id: to match query to the corresponding reply received from a DNS server
        # qd: Question Count, specifies the number of questions
        # an: Answer Record Count: specifies the number of resource records
        # ar: Additional Record Count: specifies the number of resource records

        self.question = DNSQuestion(data[12:])

    def get_id(self):
        return self.Id

    def set_id(self, i):
        self.Id = i


    def get_domain(self):
        return self.question.domain

    def set_ip(self, ip):
        self.RRF = DNSRRF(ip)
        self.AnCount = 1
        self.Flags = 33152

    def get_ip(self, reply):
        ip = ''
        i = self.question.len + 12
        got = False
        while i < len(reply) and not got:

            if reply[i] == 0xc0 and i+3 < len(reply) and reply[i+3] == 0x01:
                got = True
                i += 12
            else:
                i += 1
        if i + 3 < len(reply):
            ip += str(reply[i])
            ip += '.'
            ip += str(reply[i+1])
            ip += '.'
            ip += str(reply[i+2])
            ip += '.'
            ip += str(reply[i+3])
        else:
            print(":: Error! Reply packet corrupted!")
        return ip

    def response(self):
        pack = struct.pack('!6H', self.Id, self.Flags, self.QdCount, self.AnCount, self.NsCount, self.ArCount)
        pack = pack + self.question.get_bytes()
        if self.AnCount != 0:
            pack += self.RRF.get_bytes()
        return pack

    def request(self, i):
        tmp = 0xff
        tmp = i & tmp
        self.set_id(tmp)
        pack = struct.pack('!6H', self.Id, self.Flags, self.QdCount, self.AnCount, self.NsCount, self.ArCount)
        pack = pack + self.question.get_bytes()
        return pack



