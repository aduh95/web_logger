#!/usr/bin/env python3

import os
import webbrowser

from webserver import Server
from websocket_server import Websocket_server
from browser import Browser

def main():
    server = Server(8080, Browser("chromium-browser"))
    websocket_server = Websocket_server(3000)

    server.start()
    websocket_server.start()

    with open("./menu.json") as f:
        websocket_server.sendData(f.read())

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
