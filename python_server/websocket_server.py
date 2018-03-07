#!/usr/bin/env python3

import asyncio
import websockets
import json
from threading import Thread


class Websocket_server(Thread):

    def __init__(self, port=3000):
        Thread.__init__(self, daemon = True)
        self.port = port
        

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

        start_server = websockets.serve(self.hello, 'localhost', self.port, loop=self.loop)

        self.loop.run_until_complete(start_server)
        self.loop.run_forever()

