from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread


class Server(Thread):

    def __init__(self, port=8080, browserLock=None):
        Thread.__init__(self)
        self.port = 8080
        self.browserLock = browserLock
        if browserLock:
            browserLock.acquire()

    def run(self):
        server_address = ('localhost', self.port)

        SimpleHTTPRequestHandler.extensions_map[".mjs"] = "application/javascript"
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

        if self.browserLock:
            self.browserLock.release()

        print("HTTP server ready")
        httpd.serve_forever()
