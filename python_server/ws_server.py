import json
import asyncio
import websockets
from threading import Thread, Semaphore


class Websocket_server(Thread):
    def __init__(
        self,
        port=3000,
        apex=None,
        browserLock=None,
        bindingAddress="localhost",
        jsModulePath="./webSocketPort.mjs",
    ):
        Thread.__init__(self)
        self.port = port
        self.connected = set()
        self.showMustGoOn = True
        self.threadOnConnection = []
        self.apex = apex
        self.browserLock = browserLock
        self.bindingAddress = bindingAddress
        if browserLock:
            browserLock.acquire()
        # Communicating WS port to the client (browser)
        with open(jsModulePath, "w") as f:
            f.write("export default {}".format(port))

    def attach(self, thread):
        self.threadOnConnection.append(thread)

    def run(self):
        self.loop = asyncio.new_event_loop()

        start_server = websockets.serve(
            self.handler, self.bindingAddress, self.port, loop=self.loop
        )

        self.loop.run_until_complete(start_server)
        print("WS server ready")
        if self.browserLock:
            self.browserLock.release()
        self.loop.run_forever()
        self.loop.close()
        print("WS server off")

    async def handler(self, websocket, path):
        self.connected.add(websocket)
        for thread in self.threadOnConnection:
            try:
                thread.ws_server = self
                thread.start()
            except:
                pass
        try:
            while True:
                self.verbosePrint("waiting socket...")
                data = await websocket.recv()
                self.verbosePrint("socket received")
                if self.apex:
                    self.apex.executeMenuAction(data)
        except websockets.exceptions.ConnectionClosed:
            self.verbosePrint("connection closed")
            pass
        finally:
            self.connected.remove(websocket)

    def send(self, data):
        for websocket in self.connected.copy():
            self.verbosePrint("Sending data: %s" % data)
            asyncio.run_coroutine_threadsafe(
                websocket.send(json.dumps(data)), self.loop
            )

    def stop(self):
        self.loop.call_soon_threadsafe(self.stopLoop)

    def stopLoop(self):
        if callable(asyncio.all_tasks):
            # Python 3.7+
            tasks = asyncio.all_tasks(self.loop)
        elif callable(asyncio.Task.all_tasks):
            # Python 3.5 - 3.6
            tasks = asyncio.Task.all_tasks(self.loop)
        else:
            tasks = set()

        for task in tasks:
            task.cancel()
        self.loop.stop()

    def verbosePrint(self, message):
        if self.apex and self.apex.DEBUG_ENABLED:
            print("WS: {}".format(message))
