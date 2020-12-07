#!/usr/bin/python3

import logging
import time

import time, threading, socket
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path != '/':
            self.send_error(404, "Object not found")
            return
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        ## serve up an infinite stream
        #i = 0
        #while True:
        #    self.wfile.write("%i " % i)
        #    time.sleep(0.1)
        #    i += 1
        self.wfile.write(bytes("Hello caller", "utf-8"))
        #for i in range(50):
        #    logging.warning("Danger Will Robinson %d!" % (i+1))
            

# Create ONE socket.
addr = ('', 8080)
sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(addr)
sock.listen(5)

# Launch 4 listener threads.
class Thread(threading.Thread):
    def __init__(self, i):
        threading.Thread.__init__(self)
        self.i = i
        self.daemon = True
        self.start()
    def run(self):
        httpd = HTTPServer(addr, Handler, False)

        # Prevent the HTTP server from re-binding every handler.
        # https://stackoverflow.com/questions/46210672/
        httpd.socket = sock
        httpd.server_bind = self.server_close = lambda self: None

        httpd.serve_forever()
[Thread(i) for i in range(4)]

# Log a lot!
while True:
    logging.warning("Danger Will Robinson!")
    time.sleep(1)
