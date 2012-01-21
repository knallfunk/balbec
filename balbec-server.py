#!/usr/bin/python
# -*- coding: utf-8 -*-

from balbec.xmlhandler import XmlHandler
from balbec.htmlhandler import HtmlHandler

import SimpleHTTPServer
import SocketServer
import os
import sys
import signal
import socket

PORT = 8100
CWD = os.getcwd()

class BalbecServer(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):

        pathElements = filter(None, self.path.split('/'))    
        accept = self.headers.getheader('Accept')

        try:
    
            if len(pathElements) == 1:
                
                requestedMap = pathElements[0]
            elif len(pathElements) > 1:

                raise Exception('"' + self.path + '" is not an allowed path.')
            else:
            
                requestedMap = None
    
            if accept.find('text/html') != -1:
    
                handler = HtmlHandler(CWD)
                
                if requestedMap == None:
                
                    self.send_response(301)
                    self.send_header("Location", "/" + handler.maps[0].name)
                    self.end_headers()                                
                    return
                
                output = handler.html(requestedMap)
    
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(output)
            else:
    
                handler = XmlHandler(CWD)
                output = handler.xml(requestedMap)  
    
                self.send_response(200)
                self.send_header('Content-type', 'text/xml')
                self.end_headers()
                self.wfile.write(output)
        except Exception, e:
            
            print e
            self.send_response(503, 'Service Unavailable')

try:

    if len(sys.argv) != 1:

        if len(sys.argv) != 3 or sys.argv[1] != '-p': raise Exception
        PORT = int(sys.argv[2])
except Exception:

    print 'syntax: '+sys.argv[0]+' [-p portnumber]'
    sys.exit(1) 


server = BalbecServer

#handler = XmlHandler(CWD)
#output = handler.xml() 

try:

    httpd = SocketServer.TCPServer(("", PORT), server)
    
    def signal_handler(signal, frame):

        httpd.socket.close()
        print "Balbec http server stopped."
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    httpd.serve_forever()
except socket.error, e:

    print "Error:", e[1]
    sys.exit(1)

