#!/usr/bin/python3
#coding=utf-8
#__author__ = 'E-Tsai'
#dns analyzer

from dnsQuery import *

local_cache_name = 'dnsrelay.txt'
BUFSIZE = 1024
id_map = {}

class dnsAnalyzer:
    ##    [dns Header structure]
    ##                                   1  1  1  1  1  1
    ##     0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    ##    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    ##    |                      ID                       |
    ##    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    ##    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
    ##    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    ##    |                    QDCOUNT                    |
    ##    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    ##    |                    ANCOUNT                    |
    ##    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    ##    |                    NSCOUNT                    |
    ##    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    ##    |                    ARCOUNT                    |
    ##    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    # DNS analyzer is used to unpack and analyse data in DNS requests
    # As be a frame, it need initialized by DnsQuery
    def __init__(self, data):
        (self.Id, self.Flags, self.QdCount, self.AnCount, self.NsCount, self.ArCount) = \
            struct.unpack('!6H', data[0: 12])
        self.query = DnsQuery(data[12:])
        # id: to match query to the corresponding reply received from a DNS server
        # qd: Question Count, specifies the number of questions
        # an: Answer Record Count: specifies the number of resource records
        # ar: Additional Record Count: specifies the number of resource records

    def get_id(self):
        return self.Id

    def set_id(self, i):
        self.Id = i

    def set_rcode(self, rcode):
        self.Flags = self.Flags//16 * 16 + rcode

    def get_qr(self):
        qr = (self.Flags >> 15) % 2
        #print('> QR is : %d' % qr)
        return qr

    def get_domain(self):
        #get the domain in Question part of DNS package
        return self.query.domain

    def set_ip(self, ip):
        #set ip of reply package
        self.Answer = DnsAnswer(ip)
        self.AnCount = 1
        self.Flags = 33152

    def get_ip(self, reply):
        #get IP from Answer part when the it is reply package
        ip = ''
        i = self.query.len + 12
        #according structure of Answer, RDATA starts from the 13th byte of Answer
        if_got = False
        while i < len(reply) and not if_got:
            if reply[i] == 0xc0 and i+3 < len(reply) and reply[i+3] == 0x01:
                if_got = True
                i += 12
            else:
                i += 1
        ip += str(reply[i])
        ip += '.'
        ip += str(reply[i+1])
        ip += '.'
        ip += str(reply[i+2])
        ip += '.'
        ip += str(reply[i+3])
        
        return ip

    def response(self):
        pack = struct.pack('!6H', self.Id, self.Flags, self.QdCount, self.AnCount, self.NsCount, self.ArCount)
        pack = pack + self.query.get_bytes()
        if self.AnCount != 0:
            pack += self.Answer.get_bytes()
        return pack

    def request(self, i):
        tmp = 0xff
        tmp = i & tmp
        self.set_id(tmp)
        pack = struct.pack('!6H', self.Id, self.Flags, self.QdCount, self.AnCount, self.NsCount, self.ArCount)
        pack = pack + self.query.get_bytes()
        return pack