import asyncio
import websockets
from threading import Thread, Semaphore
import json


class Websocket_server(Thread):
    def __init__(self, port=3000, apex=None, browserLock=None):
        Thread.__init__(self)
        self.port = port
        self.connected = set()
        self.showMustGoOn = True
        self.threadOnConnection = []
        self.apex = apex
        self.browserLock = browserLock
        if browserLock:
            browserLock.acquire()
        with open('./webSocketPort.mjs', 'w') as f:
            f.write('export default '+str(port))

    def attach(self, thread):
        self.threadOnConnection.append(thread)

    def run(self):
        self.loop = asyncio.new_event_loop()

        start_server = websockets.serve(
            self.handler, 'localhost', self.port, loop=self.loop)

        self.loop.run_until_complete(start_server)
        if self.browserLock:
            self.browserLock.release()
        print("WebSockets server ready")
        self.loop.run_forever()

    async def handler(self, websocket, path):
        self.connected.add(websocket)
        for thread in self.threadOnConnection:
            if not thread.is_alive():
                thread.ws_server = self
                thread.start()
        try:
            while True:
                print("WS: waiting socket...")
                data = await websocket.recv()
                print("WS: socket received")
                if self.apex:
                    self.apex.executeMenuAction(data)
        except websockets.exceptions.ConnectionClosed:
            print("WS: connection closed")
            pass
        finally:
            self.connected.remove(websocket)

    def send(self, data):
        for websocket in self.connected.copy():
            print("Sending data: %s" % data)
            coro = websocket.send(json.dumps(data))
            future = asyncio.run_coroutine_threadsafe(coro, self.loop)
