from threading import Thread, Event
from time import strftime

import sys
import logging
import traceback

from .http_server import Server
from .ws_server import Websocket_server
from .browser import Browser

__all__ = ["Logger"]


class Logger(Thread):
    def __init__(
        self, browser_path, http_port=3000, ws_port=3001, onReady=lambda _: None
    ):
        Thread.__init__(self)
        self.start_event = Event()
        self.stop_event = Event()

        browser = Browser(
            browser_path,
            appAddress="http://localhost:" + str(http_port),
            stop_event=self.stop_event,
        )

        self.executeOnReady = onReady
        self.ws_server = Websocket_server(
            ws_port,
            handlerCallback=self.executeMenuAction,
            browserLock=browser.getLock(),
            start_event=self.start_event,
            stop_event=self.stop_event,
        )
        http_server = Server(
            http_port, browserLock=browser.getLock(), stop_event=self.stop_event
        )

        http_server.start()
        self.ws_server.start()
        browser.start()
        self.start()

        # Wait for browser thread to end (I.E. the user closes it)
        browser.join()
        logging.debug("Browser thread has ended")

        # stopping the event loop
        self.ws_server.stop_loop()

        # Wait for the servers to stop
        http_server.join()
        self.ws_server.join()

        # logger has now terminated
        logging.debug("Logger has terminated")
        logging.debug("onReady thread status: {}".format(self.is_alive()))

    def run(self):
        self.start_event.wait()  # start event will be set when a client connects
        self.executeOnReady(self)

    def stop(self):
        logging.debug("Sending stop event")
        self.stop_event.set()

    def defineNewMenu(self, menus):
        self.__serializedFunctions = []
        self.__serializeFunctions(menus)
        self.ws_server.send({"menu": menus})

    def __serializeFunctions(self, menuContainer):
        for menuItem in menuContainer:
            if "click" in menuItem and callable(menuItem["click"]):
                self.__serializedFunctions.append(menuItem["click"])
                menuItem["click"] = len(self.__serializedFunctions)
            if "submenu" in menuItem:
                self.__serializeFunctions(menuItem["submenu"])

    def clean(self):
        self.ws_server.send({"command": "clean"})

    def executeMenuAction(self, id):
        try:
            self.__serializedFunctions[int(id) - 1]()
            logging.debug("Menu: action has ran")
        except:
            logging.warning("Menu: Invalid action")
            traceback.print_exc(file=sys.stderr)

    def log(self, *message, className="message", keyboardInput=None, audioFile=None):
        """
        Logs a message. If the message cannot be logged, will raise a LoggerException
        """
        self.ws_server.send(
            {
                "message": [
                    className,
                    strftime("%x"),
                    strftime("%X"),
                    *message,
                    keyboardInput,
                    audioFile,
                ]
            }
        )
