from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from .loggerException import LoggerException


class Server(Thread):
    def __init__(self, port=8080, bindingAddress="localhost", browserLock=None):
        Thread.__init__(self)
        self.port = port
        self.browserLock = browserLock
        self.httpDeamon = None
        self.bindingAddress = bindingAddress
        if browserLock:
            browserLock.acquire()

    def run(self):
        server_address = (self.bindingAddress, self.port)

        SimpleHTTPRequestHandler.extensions_map[".mjs"] = "application/javascript"
        self.httpDeamon = HTTPServer(server_address, SimpleHTTPRequestHandler)

        if self.browserLock:
            self.browserLock.release()

        print("HTTP server ready")
        self.httpDeamon.serve_forever()
        print("HTTP server off")

    def stop(self):
        if self.httpDeamon:
            self.httpDeamon.shutdown()
        else:
            raise LoggerException("Trying to stop HTTP server before starting it")
