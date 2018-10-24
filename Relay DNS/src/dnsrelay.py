#!/usr/bin/python3
#coding=utf-8
#__author__ = 'E-Tsai'
#dns server

import threading
import time
import socket

def localTable(ip_list):
    '''
    :type ip_list: str
    :rtype: dict
    '''
    try:
        print('::Scanning local ip cache')
        ip_file = open(ip_list, 'r')
    except:
        print('::Error: can not open file:', ip_list)
        return
    ip_table = {}
    for line in ip_file.readlines():
        if line == '\n':
            continue
        ip = line.split(' ')[0]
        name = line.split(' ')[1][:-1]
        ip_table[name] = ip
    return ip_table

class DNSServer:
    def __init__(self, ip = '127.0.0.1', port = 53):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #using UDP

    def runServer(self):
        print('::starting up on {} port {}'.format(self.ip, self.port))
        self.sock.bind((self.ip, self.port))
        while 1:
            data, addr = self.sock.recvfrom(512)
            print('::data:',data)
        #thread.Thread(target=self.relay_thread).start()
