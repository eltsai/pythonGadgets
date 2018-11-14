#!/usr/bin/python3
#coding=utf-8
#__author__ = 'E-Tsai'
#dns server

from UDPHandler import *

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


def loadCache():
        '''
        :type ip_list: str
        :rtype: dict
        '''
        try:
            print('::Scanning local ip cache')
            ip_file = open(local_cache_name, 'r')
        except:
            print('::Error: can not find local cache')
            return
    
        for line in ip_file.readlines():
            if line == '\n':
                continue
            ip = line.split(' ')[0]
            name = line.split(' ')[1][:-1]
            local_cache[name] = ip
        print('::Local dns table has been successfully loaded')


class Server:
    def __init__(self, ip = '127.0.0.1', port = 53):
        '''
        initialization
        '''
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.public_server = ('202.46.36.116', 53)
        # https://public-dns.info/nameserver/cn.html, using UDP
        loadCache()

    

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
                # local_cache[index] = analyzer.get_id()
                self.sock.sendto(analyzer.request(index), self.public_server)

                self.sock.setblocking(0)
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

    def runServer(self):
        '''
        set up dns relay server
        '''
        threading.Thread(target=self.relay_thread).start()
        print('::Server starting up on ip: {}, port: {}...\n'.format(self.ip, self.port))
        server = socketserver.UDPServer((self.ip, self.port), UDPHandler)
        server.serve_forever()


        

    
