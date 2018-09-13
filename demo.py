#!/usr/bin/env python3.5

import os
import sys
import json
import argparse

sys.path.append("./python_server")

from python_server.apexClient import ApexClient


def commandExample():
    print("""
    This function is pointless, but it *COULD* be awesome!

                 (__) 
                 (oo) 
           /------\/ 
          / |    ||   
         *  /\---/\ 
            ~~   ~~   
..."Have you mooed today?"...
    """)


def cleanClient(client):
    print("Let's flush all those non-sense messages")
    client.clean()


def demo(client):
    print("WebSocket connected")
    client.defineNewMenu([
        {
            "label": "Configuration",
            "click": None,
            "submenu": [
                {
                    "label": "test",
                    "click": commandExample
                },
                {
                    "label": "Clean APEX",
                    "click": lambda: cleanClient(client)
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
    with open("../example.json") as f:
        data = json.load(f)
    while True:
        for message in data:
            client.printMessage(
                message[5], mnemonic=message[2], target=message[3], type=message[4])
            input("Press enter to send a new message\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Launch APEX server.')
    parser.add_argument('--http-port', type=int, default=8080,
                        help='Port used for HTTP web server')
    parser.add_argument('--ws-port', type=int, default=8081,
                        help='Port used for websocket server')
    parser.add_argument('--browser', type=str, default="chromium-browser",
                        help='Path / Name of the browser to use')
    parser.add_argument('--www', type=str, default="./www",
                        help='Path of the `www` directory')

    args = parser.parse_args()
    try:
        os.chdir(args.www)
        ApexClient(args.browser, args.http_port, args.ws_port, onReady=demo)
    except KeyboardInterrupt:
        print('Interrupted')
        os._exit(0)
