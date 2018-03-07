#!/usr/bin/env python3

from http.server import *
import asyncio
from threading import Thread


class Server(Thread):

    def __init__(self, port=8080):
        Thread.__init__(self, daemon = True)
        self.port = 8080

    def run(self):

        server_address = ('localhost', self.port)

        SimpleHTTPRequestHandler.extensions_map[".mjs"] = "application/javascript"
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
        httpd.serve_forever()
