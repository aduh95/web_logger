from threading import Thread
from time import strftime

import sys
import traceback

from .http_server import Server
from .ws_server import Websocket_server
from .browser import Browser

__all__ = ["Logger"]


class Logger(Thread):
    DEBUG_ENABLED = False

    def __init__(
        self,
        browser_path,
        http_port=3000,
        ws_port=3001,
        onReady=lambda _: None,
        onClosing=lambda _: None,
        closeOnBrowserClose=True,
    ):
        Thread.__init__(self)
        browser = Browser(browser_path, appAddress="http://localhost:" + str(http_port))

        self.should_terminate = False
        self.executeOnReady = onReady
        self.ws_server = Websocket_server(ws_port, browserLock=browser.getLock())
        self.ws_server.apex = self
        self.ws_server.attach(self)
        http_server = Server(http_port, browserLock=browser.getLock())

        http_server.start()
        self.ws_server.start()
        browser.start()

        # Wait for browser thread to end (I.E. the user closes it)
        browser.join()

        if not closeOnBrowserClose:
            self.should_terminate = True
            input("Browser has closed, press enter to terminate")

        print("Stopping servers...")
        http_server.stop()
        self.ws_server.stop()

        # Wait for the servers to stop
        http_server.join()
        self.ws_server.join()

        onClosing(self)

    def run(self):
        self.executeOnReady(self)

    def stop(self):
        # Stopping WS server should close the browser
        # Which then will terminate the other threads
        try:
            self.ws_server.close()
        except:
            # Wait for the client to be ready
            self.executeOnReady = self.stop
        self.should_terminate = True

    def defineNewMenu(self, menus):
        self.serializedFunctions = []
        self.__serializeFunctions(menus)
        self.ws_server.send({"menu": menus})

    def __serializeFunctions(self, menuContainer):
        for menuItem in menuContainer:
            if "click" in menuItem and callable(menuItem["click"]):
                self.serializedFunctions.append(menuItem["click"])
                menuItem["click"] = len(self.serializedFunctions)
            if "submenu" in menuItem:
                self.__serializeFunctions(menuItem["submenu"])

    def clean(self):
        self.ws_server.send({"command": "clean"})

    def executeMenuAction(self, id):
        try:
            self.serializedFunctions[int(id) - 1]()
        except:
            print("Menu: Invalid action")
            traceback.print_exc(file=sys.stderr)

    def printMessage(
        self, *message, className="message", keyboardInput=None, audioFile=None
    ):
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
