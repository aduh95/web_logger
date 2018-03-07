#!/usr/bin/env python3

from threading import Thread
import json
import os

from apex import Apex

class Demo(Thread):
    def __init__(self, ws_server=None):
        Thread.__init__(self)
        self.apex = Apex(ws_server)

    def run(self):
        print("WebSocket connected")
        self.apex.defineNewMenu([
            {
                "label": "Configuration",
                "click": None,
                "submenu": [
                    {
                    "label": "test",
                    "click": lambda: print("test")
                    }
                ]
            },
            {
                "label": "Manage targets",
                "submenu": []
            },
            {
                "label": "Quit",
                "click": lambda: os._exit(0)
            }
        ])
        with open("./example.json") as f:
            data = json.load(f)
            for message in data:
                input("Press enter to send a new message")
                self.apex.sendMessage(message[5], mnemonic=message[2], target=message[3], type=message[4])
