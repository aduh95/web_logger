#!/usr/bin/env python3


from threading import Thread
from http.server import *
import asyncio
import websockets
import asyncio
import json

PORT = 8080


class Server(Thread):

    def __init__(self):
        Thread.__init__(self, daemon = True)

    def run(self):

        server_address = ('localhost', PORT)

        SimpleHTTPRequestHandler.extensions_map[".mjs"] = "application/javascript"
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
        httpd.serve_forever()


class Websocket_server(Thread):

    def __init__(self):
        Thread.__init__(self, daemon = True)
        

    async def hello(self, websocket, path):
        with open("./menu.json") as f:
            await websocket.send(f.read())
        with open("./example.json") as f:
            data = json.load(f)
            for message in data:
                await websocket.send(json.dumps({"message": message}))
                await asyncio.sleep(1)

        command = None
        while(command != "quit"):
            command = await websocket.recv()
            print("Receive: {}".format(command))
        websocket.close()
        exit()

    def run(self):
        self.loop = asyncio.new_event_loop()

        start_server = websockets.serve(self.hello, 'localhost', 3000, loop=self.loop)

        self.loop.run_until_complete(start_server)
        self.loop.run_forever()


server = Server()
websocket_server = Websocket_server()

server.start()
websocket_server.start()

server.join()
websocket_server.join()
