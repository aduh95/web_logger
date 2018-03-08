#!/usr/bin/env python3

from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread


class Server(Thread):

    def __init__(self, port=8080, browser=None):
        Thread.__init__(self)
        self.port = 8080
        self.browser = browser

    def run(self):

        server_address = ('localhost', self.port)

        SimpleHTTPRequestHandler.extensions_map[".mjs"] = "application/javascript"
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

        if self.browser:
            self.browser.appAddress = "http://localhost:"+str(self.port)
            self.browser.start()

        httpd.serve_forever()
