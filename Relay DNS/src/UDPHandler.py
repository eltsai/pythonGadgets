#!/usr/bin/python3
#coding=utf-8
#__author__ = 'E-Tsai'
#UDP handler

import socketserver
from dnsAnalyzer import *



local_cache = {}
# local cache
tasks = [] 
# threading

class UDPHandler(socketserver.BaseRequestHandler):
    """
    https://docs.python.org/3.4/library/socketserver.html
    a udp handler for relay dns
    """
    def handle(self):
        """
        :type local_cache: dict
        """
        data = self.request[0].strip()
        sock = self.request[1]
        analyzer = dnsAnalyzer(data)

        if analyzer.query.type == 1:
            # client ask for ip
            domain = analyzer.get_domain()
            print('::Requesting ip from local cache...')
            if domain in local_cache:
                ip = local_cache[domain]
                analyzer.set_ip(ip)
                if ip == "0.0.0.0":
                    # blacklisted website
                    analyzer.set_rcode(3)
                    print('::Error: domain does not exist.\n')
                else:
                    print('::Domain exists on local server..')
                    print('::Domain {}: ip {}\n'.format(domain, ip))
                
                sock.sendto(analyzer.response(), self.client_address)
                
            else:
                # relay
                print('::Requesting ip from public server...')
                tasks.append((sock, data.upper(), self.client_address))
        else:
            sock.sendto(data.upper(), self.client_address)

