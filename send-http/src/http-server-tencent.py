#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
import random


PORT_NUMBER = 8080


sensitive = [b'Tian An Men', b'Xinjiang Concentration Camp', b'Panama Papers', b'FreeTibet']

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

        #Handler for the GET requests
        def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                # Send the html message
                self.wfile.write(b"freegate\n")
                self.wfile.write(b"falun\n")
                idx = random.randint(0, len(sensitive) - 1)
                self.wfile.write(sensitive[idx])
                return

try:
        #Create a web server and define the handler to manage the
        #incoming request
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        print('Started httpserver on port {}'.format(PORT_NUMBER))

        #Wait forever for incoming htto requests
        server.serve_forever()

except KeyboardInterrupt:
        print('^C received, shutting down the web server')
        server.socket.close()
