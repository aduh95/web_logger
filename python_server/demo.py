#!/usr/bin/env python3

import json
import os


def demo(client):
    print("WebSocket connected")
    client.defineNewMenu([
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
    data = []
    with open("./example.json") as f:
        data = json.load(f)
    while True:
        for message in data:
            client.printMessage(
                message[5], mnemonic=message[2], target=message[3], type=message[4])
            input("Press enter to send a new message\n")
