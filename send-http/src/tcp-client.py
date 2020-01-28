#!/usr/bin/python3

import socket

#host = socket.gethostname()
host='118.24.75.137'
port = 12345                   # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.sendall(b'freegate falun')
data = s.recv(1024)
s.close()
print('Received', repr(data))