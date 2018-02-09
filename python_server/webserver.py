#!/usr/bin/env python3

from http.server import *
import asyncio
import websockets

PORT = 8080
server_address = ('localhost', PORT)

SimpleHTTPRequestHandler.extensions_map[".mjs"] = "application/javascript"
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
httpd.serve_forever()
