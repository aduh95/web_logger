#!/usr/bin/env python
import os
import time
import webbrowser
import argparse

from http_server import Server
from ws_server import Websocket_server
from browser import Browser

from demo import Demo


def main(browser_name, http_port, ws_port):
    http_server = Server(http_port, Browser(browser_name))
    ws_server = Websocket_server(ws_port)

    ws_server.attach(Demo(ws_server))

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
    parser.add_argument('--browser', type=str, default="chromium-browser",
                        help='Path / Name of the browser to use')

    args = parser.parse_args()
    try:
        main(args.browser, args.http_port, args.ws_port)
    except KeyboardInterrupt:
        print('Interrupted')
        os._exit(0)
