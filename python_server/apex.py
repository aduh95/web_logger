#!/usr/bin/env python3

from threading import Thread
from time import strftime


class ApexClient(Thread):
    def __init__(self, ws_server):
        Thread.__init__(self)
        self.executeOnReady = lambda _: None
        self.ws_server = ws_server
        ws_server.apex = self

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

    def executeMenuAction(self, id):
        try:
            self.serializedFunctions[int(id) - 1]()
        except:
            print("Menu: Invalid action")

    def printMessage(self, message, mnemonic="Unknown", type="message", target="Unknown", keyboardInput=None, audioFile=None):
        self.ws_server.send({"message": [
            strftime("%x"),
            strftime("%X"),
            mnemonic,
            target,
            type,
            message,
            keyboardInput,
            audioFile
        ]})
