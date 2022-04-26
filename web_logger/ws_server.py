import asyncio
import json
import logging
from websockets.server import serve
from websockets.exceptions import ConnectionClosed
from threading import Event, Lock
from typing import Callable
from .stoppableThread import StoppableThread
from .loggerException import LoggerException

__all__ = []


class Websocket_server(StoppableThread):
    def __init__(
        self,
        port: int = 3000,
        handlerCallback: Callable = None,
        browserLock: Lock = None,
        bindingAddress: str = "localhost",
        jsModulePath: str = "./webSocketPort.mjs",
        start_event: Event = None,
        stop_event: Event = None,
    ):
        StoppableThread.__init__(self, stop_event)
        self.port = port
        self.connected = set()
        self.showMustGoOn = True
        self.threadOnConnection = []
        self.handlerCallback = handlerCallback
        self.server = None
        self.loop = None
        self.browserLock = browserLock
        self.start_event = start_event
        self.bindingAddress = bindingAddress
        if browserLock:
            browserLock.acquire()
        # Communicating WS port to the client (browser)
        with open(jsModulePath, "w") as f:
            f.write("export default {}".format(port))

    def run(self):
        try:
            self.loop = asyncio.get_event_loop()
        except:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            logging.debug("Loop created")

        start_server = serve(
            self.handler, self.bindingAddress, self.port, loop=self.loop
        )

        self.server = self.loop.run_until_complete(start_server)
        logging.info("WS server ready")
        if self.browserLock:
            self.browserLock.release()
        try:
            self.loop.run_forever()
        finally:
            self.loop.run_until_complete(self.server.wait_closed())
            logging.info("WS server off")

    async def handler(self, websocket, path):
        self.connected.add(websocket)
        self.start_event.set()
        try:
            while True:
                logging.debug("waiting for a socket...")
                data = await websocket.recv()
                logging.debug("socket received: {}".format(data))
                if self.handlerCallback:
                    self.handlerCallback(data)
        except ConnectionClosed:
            logging.debug("connection closed")
            pass
        except asyncio.CancelledError:
            logging.debug("connection cancelled")
            pass
        finally:
            self.connected.remove(websocket)

    def send(self, data):
        if self.loop.is_closed():
            raise LoggerException(
                "Cannot send messages with a closed instance")
        for websocket in self.connected.copy():
            logging.info("Sending data: %s" % data)
            asyncio.run_coroutine_threadsafe(
                websocket.send(json.dumps(data)), self.loop
            )

    def stop(self):
        if self.server:
            self.server.close()
        else:
            logging.warning("Ignoring stop signal on a closed WS server")

    def stop_loop(self):
        if self.loop and self.loop.is_running():
            self.loop.call_soon_threadsafe(self.loop.stop)
        else:
            logging.warning("Ignoring stop signal on a closed loop")
