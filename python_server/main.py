#!/usr/bin/env python3

import os
import time
import webbrowser
import argparse

from http_server import Server
from ws_server import Websocket_server
from browser import Browser

from demo import Demo

def main(http_port, ws_port):
    http_server = Server(http_port, Browser("chromium-browser"))
    ws_server = Websocket_server(ws_port, Demo())

    http_server.start()
    ws_server.start()

    http_server.join()
    ws_server.join()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Launch APEX server.')
    parser.add_argument('--http-port', type=int, default=8080,
                    help='Port used for HTTP web server')
    parser.add_argument('--ws-port', type=int, default=8081,
                    help='Port used for websocket server')

    args = parser.parse_args()
    print(args)
    try:
        main(args.http_port, args.ws_port)
    except KeyboardInterrupt:
        print ('Interrupted')
        try:
            sys.exit(0)
        except:
            os._exit(0)
