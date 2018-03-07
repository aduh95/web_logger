#!/usr/bin/env python3

import asyncio
import websockets
import json
import time
from threading import Thread


class Websocket_server(Thread):
    def __init__(self, port=3000):
        Thread.__init__(self)
        self.port = port
        self.connected = set()
        self.showMustGoOn = True
        self.dataToSend = []

    def run(self):
        self.loop = asyncio.new_event_loop()

        start_server = websockets.serve(self.handler, 'localhost', self.port, loop=self.loop)

        self.loop.run_until_complete(start_server)
        self.loop.run_forever()

    async def handler(self, websocket, path):
        self.connected.add(websocket)
        try:
            await websocket.recv()
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connected.remove(websocket)

    def sendData(self, data):
        for websocket in self.connected.copy():
            print("Sending data: %s" % data)
            coro = websocket.send(data)
            future = asyncio.run_coroutine_threadsafe(coro, self.loop)


