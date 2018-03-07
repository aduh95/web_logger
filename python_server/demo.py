#!/usr/bin/env python3

from threading import Thread
import json
import time

from menu import menu

class Demo(Thread):
    def __init__(self, ws_server=None):
            Thread.__init__(self)
            self.ws_server=ws_server

    def run(self):
        print("WebSocket connected")
        self.ws_server.sendData(json.dumps(menu))
        with open("./example.json") as f:
            data = json.load(f)
            for message in data:
                time.sleep(.3)
                self.ws_server.sendData(json.dumps({"message":message}))
