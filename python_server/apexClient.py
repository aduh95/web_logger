from threading import Thread
from time import strftime

from .http_server import Server
from .ws_server import Websocket_server
from .browser import Browser


class ApexClient(Thread):
    def __init__(self, browser_name, http_port, ws_port, onReady=lambda _: None):
        Thread.__init__(self)
        browser = Browser(browser_name, appAddress="http://localhost:" + str(http_port))

        self.executeOnReady = onReady
        self.ws_server = Websocket_server(ws_port, browserLock=browser.getLock())
        self.ws_server.apex = self
        self.ws_server.attach(self)
        http_server = Server(http_port, browserLock=browser.getLock())

        http_server.start()
        self.ws_server.start()
        browser.start()

        http_server.join()
        self.ws_server.join()
        browser.join()

    def run(self):
        self.executeOnReady(self)

    def defineNewMenu(self, menus):
        self.serializedFunctions = []
        self.serializeFunctions(menus)
        self.ws_server.send({"menu": menus})

    def serializeFunctions(self, menuContainer):
        for menuItem in menuContainer:
            if "click" in menuItem and callable(menuItem["click"]):
                self.serializedFunctions.append(menuItem["click"])
                menuItem["click"] = len(self.serializedFunctions)
            if "submenu" in menuItem:
                self.serializeFunctions(menuItem["submenu"])

    def clean(self):
        self.ws_server.send({"command": "clean"})

    def executeMenuAction(self, id):
        try:
            self.serializedFunctions[int(id) - 1]()
        except:
            print("Menu: Invalid action")

    def printMessage(
        self,
        message,
        mnemonic="Unknown",
        type="message",
        target="Unknown",
        keyboardInput=None,
        audioFile=None,
    ):
        self.ws_server.send(
            {
                "message": [
                    strftime("%x"),
                    strftime("%X"),
                    mnemonic,
                    target,
                    type,
                    message,
                    keyboardInput,
                    audioFile,
                ]
            }
        )
