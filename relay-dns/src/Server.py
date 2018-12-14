#!/usr/bin/python3
#coding=utf-8
#__author__ = "E-Tsai"
#DNS server

# from UDPHandler import *
import socketserver
import socket
from DNSAnalyzer import *
from threading import Thread 
from time import ctime

local_addr = "dnsrelay.txt"
BUFSIZE = 1024
MAXQUEUE = 512 # support max threading of 512
id = {}
local_cache = {}
server_114 = "114.114.114.114"
public_request = [] 
cur = 0


class UDPHandler(socketserver.BaseRequestHandler):
    """
    https://docs.python.org/3.4/library/socketserver.html
    a udp handler for relay DNS
    """
    def handle(self):
        """
        :type local_cache: dict
        """
        
        data = self.request[0].strip()
        sock = self.request[1]

        analyzer = DNSAnalyzer(data)
        #print(analyzer.get_domain())
        if analyzer.question.qtype == 1:
            # client ask for ip
            domain = analyzer.get_domain()
            if domain in local_cache:
                ip = local_cache[domain]
                analyzer.set_ip(ip)
                #print(":: Requesting ip from local cache...")
                if ip == "0.0.0.0":
                    # blacklisted website
                    print("----------------------------------------------------\n")
                    print(":: Error: domain {} does not exist.\n".format(domain.upper()))
                    print("----------------------------------------------------\n")
                else:
                    #print(":: Domain exists on local server..")
                    print("----------------------------------------------------\n")
                    print(":: ANSWER SECTION:\n\n   {}.   {}".format(domain.upper(), ip))
                    if testLev == 2:
                        localID = analyzer.get_id()
                        socTime = time.ctime()
                        print("\n:: WHEN: {}".format(socTime))
                        print(":: ID: {}".format(localID))
                    elif testLev == 3:
                        print(":: SERVER: {}#{}({})".format("127.0.0.1", 53, "127.0.0.1"))
                        #print(type(data))
                        print(":: RAW DATA:\n{}".format(data))

                    print("\n----------------------------------------------------\n")
                sock.sendto(analyzer.response(), self.client_address)
                
            else:
                # relay
                
                public_request.append((sock, data.upper(), self.client_address))
        else:
            sock.sendto(data.upper(), self.client_address)


class Server:
    def __init__(self, public_server = (server_114, 53), testLevel = 1, local_addr_ = local_addr ):
        """
        initialization
        """
        self.ip = "127.0.0.1"
        self.port = 53
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.public_server = public_server
        self.local_addr = local_addr_
        global testLev
        testLev = testLevel
        self.loadCache()
        # https://public-dns.info/nameserver/cn.html, using UDP    
  
    def loadCache(self):
        """
        :type ip_list: str
        :rtype: dict
        """
        local_cache_ = {}
        try:
            
            ip_file = open(self.local_addr, "r")
        except:
            print(':: Error: can not find local cache file at {}'.format(self.local_addr))
            return
    
        for line in ip_file.readlines():
            if line == '\n':
                continue
            ip = line.split(' ')[0]
            name = line.split(' ')[1][:-1]
            local_cache[name] = ip
            

    def UDPThreading(self):
        # start a loop to deal with task queue
        while True:
            if len(public_request) > 0:
                global cur
                if cur < MAXQUEUE:
                    cur += 1
                else:
                    cur = 0
                
                sock, data, client_address = public_request[0]
                #print("request: ", data)
                analyzer = DNSAnalyzer(data)
                id[cur] = analyzer.get_id()
                
                
                self.sock.sendto(analyzer.request(cur), self.public_server)
                #self.sock.setblocking(1)
                #print("reley")
                try:
                    reply, addr = self.sock.recvfrom(BUFSIZE)
                    #print("reply:", reply)
                    
                except socket.timeout:
                    print(":: DNS timeout for 2 sec.\n")
                    continue
                
                else:
                    reply_analyzer = DNSAnalyzer(reply)
                    domain = reply_analyzer.get_domain()
                    #print("reply:", reply)
                    ip = reply_analyzer.get_ip(reply)
                    print("----------------------------------------------------\n")
                    print(":: ANSWER SECTION:\n\n   {}.   {}".format(domain.upper(), ip))
                    if testLev == 2:
                        socTime = time.ctime()
                        print("\n:: WHEN: {}".format(socTime))
                        print(":: ID: {}".format(id[cur]))
                    elif testLev == 3:
                        print("\n:: SERVER: {}#{}({})".format("127.0.0.1", 53, "127.0.0.1"))
                        print(":: DATA:\n{}".format(data))
                    print("\n----------------------------------------------------\n")
                    rest = reply[2:]
                    Id = id[cur]
                    reply = struct.pack("!H", Id) + rest
                    sock.sendto(reply, client_address)
                    
                public_request.pop(0)
                # FIFO

    def run(self):
        """
        set up DNS relay server
        """
        # https://docs.python.org/3/library/threading.html
        Thread(target=self.UDPThreading).start()
        server = socketserver.UDPServer((self.ip, self.port), UDPHandler)
        server.serve_forever()
    
