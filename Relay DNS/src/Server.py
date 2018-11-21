#!/usr/bin/python3
#coding=utf-8
#__author__ = 'E-Tsai'
#dns server

# from UDPHandler import *
from loadCache import *
import socketserver
from dnsAnalyzer import *


##    [dns package structure]
##     0 1 2    ...       31
##    +---------------------+
##    |         Header      | package head including port and address, includes 3 lines
##    +---------------------+
##    |       Question      | the question for the name server
##    +---------------------+
##    |        Answer       | RRs answering the question
##    +---------------------+
##    |      Authority      | RRs pointing toward an authority
##    +---------------------+
##    |      Additional     | RRs holding additional information
##    +---------------------+


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
            if domain in local_cache:
                ip = local_cache[domain]
                analyzer.set_ip(ip)
                print('::Requesting ip from local cache...')
                if ip == "0.0.0.0":
                    # blacklisted website
                    analyzer.set_rcode(3)
                    print('::Error: domain {} does not exist.\n'.format(domain))
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


class Server:
    def __init__(self, public_server = ('202.46.36.116', 53)):
        '''
        initialization
        '''
        self.ip = '127.0.0.1'
        self.port = 53
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.public_server = public_server
        # https://public-dns.info/nameserver/cn.html, using UDP
        

    @staticmethod
    def loadCache(filename = local_cache_name):
        """
        load local cache
        """
        global local_cache
        local_cache = loadCache_(filename)
        if local_cache:
            print('::Local dns table has been successfully loaded')

    
    """
    def renewCache(self, domain, ip):
        try:
            f = open(local_cache_name, 'a')
        except IOError:
            print("::Fail to renew local cache {}...".format(local_cache_name))
            return None
        else:
            line = ip + " " + domain + "\n"
            f.write(line)
            f.close()
    """

    def relay_thread(self):
        #start a loop to deal with task queue
        index = 0
        while True:
            if len(tasks) > 0:
                #when there exists tasks
                if index < 1024:
                    index += 1
                else:
                    index = 0

                sock, data, client_address = tasks[0]
                analyzer = dnsAnalyzer(data)
                id_map[index] = analyzer.get_id()
                self.sock.sendto(analyzer.request(index), self.public_server)

                self.sock.setblocking(1)
                time.sleep(2)
                reply, addr = self.sock.recvfrom(BUFSIZE)
                if len(reply) == 0:
                    print('::Fail to receive ip from public dns.\n')
                else:
                    reply_analyzer = dnsAnalyzer(reply)
                    domain = reply_analyzer.get_domain()
                    ip = reply_analyzer.get_ip(reply)
                    print('::Getting reply from public dns...')
                    print('::Domain {}: ip {}\n'.format(domain.lower(), ip))
                    # domainmap[domain] = reply_ip
                    # save_table(file_name, domain, reply_ip)

                    rest = reply[2:]
                    Id = id_map[index]
                    reply = struct.pack('!H', Id) + rest
                    sock.sendto(reply, client_address)
                    #print(reply)
                tasks.pop(0)

    def run(self):
        '''
        set up dns relay server
        '''
        threading.Thread(target=self.relay_thread).start()
        print('::Server starting up on ip: {}, port: {}...\n'.format(self.ip, self.port))
        server = socketserver.UDPServer((self.ip, self.port), UDPHandler)
        server.serve_forever()


        

    
