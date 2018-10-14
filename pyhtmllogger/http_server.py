import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler
from .stoppableThread import StoppableThread
from .loggerException import LoggerException

__all__ = []


class Server(StoppableThread):
    def __init__(
        self, port=8080, bindingAddress="localhost", browserLock=None, stop_event=None
    ):
        StoppableThread.__init__(self, stop_event)
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

        logging.info("HTTP server ready")
        self.httpDeamon.serve_forever()
        logging.info("HTTP server off")

    def stop(self):
        if self.httpDeamon:
            self.httpDeamon.shutdown()
        else:
            raise LoggerException("Trying to stop HTTP server before starting it")
