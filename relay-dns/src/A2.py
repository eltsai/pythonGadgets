


import socketserver
import struct
import socket
import threading
import sys
import time




class DNSQuestion:
    #from question part, get domain address which need to be queried
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


class DNSRRF:
    #write the RRF part in DNS package if needs
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


class DNSAnalyzer:
    #DNS analyzer is used to unpack and analyse data in DNS requests
    #As be a frame, it need initialized by DNSQuestion
    def __init__(self, data):
        (self.Id, self.Flags, self.QdCount, self.AnCount, self.NsCount, self.ArCount) = \
            struct.unpack('!6H', data[0: 12])
        self.question = DNSQuestion(data[12:])

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
        return self.question.domain

    def set_ip(self, ip):
        #set ip of reply package
        self.RRF = DNSRRF(ip)
        self.AnCount = 1
        self.Flags = 33152

    def get_ip(self, reply):
        #get IP from RRF part when the it is reply package
        ip = ''
        i = self.question.len + 12
        #according structure of RRF, RDATA starts from the 13th byte of RRF
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
        #print('%d.%d.%d.%d' % (reply[i], reply[i+1], reply[i+2], reply[i+3]))
        return ip

    def response(self):
        pack = struct.pack('!6H', self.Id, self.Flags, self.QdCount, self.AnCount, self.NsCount, self.ArCount)
        pack = pack + self.Question.get_bytes()
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



