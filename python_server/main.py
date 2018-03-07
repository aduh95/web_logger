#!/usr/bin/env python3

import os
import time
import webbrowser
import json

from http_server import Server
from ws_server import Websocket_server
from browser import Browser

from menu import menu

def main():
    server = Server(8080, Browser("chromium-browser"))
    websocket_server = Websocket_server(8081)

    server.start()
    websocket_server.start()

    time.sleep(1)
    websocket_server.sendData(json.dumps(menu))

    server.join()
    websocket_server.join()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print ('Interrupted')
        try:
            sys.exit(0)
        except:
            os._exit(0)
