#!/usr/bin/env python3

import os
import argparse

from lib.logger import Logger
from lib.loggerException import LoggerException


def commandExample():
    print(
        """
    This function is pointless, but it *COULD* be awesome!

                 (__) 
                 (oo) 
           /------\/ 
          / |    ||   
         *  /\---/\ 
            ~~   ~~   
..."Have you mooed today?"...
    """
    )


def cleanClient(client):
    print("Let's flush all those non-sense messages")
    client.clean()


def demo(client):
    print("Client is ready")
    client.defineNewMenu(
        [
            {
                "label": "Configuration",
                "click": None,
                "submenu": [
                    {"label": "test", "click": commandExample},
                    {"label": "Clean APEX", "click": lambda: cleanClient(client)},
                ],
            },
            {"label": "Manage targets", "submenu": []},
            {"label": "Quit", "click": client.stop},
        ]
    )
    while not client.should_terminate:
        try:
            client.printMessage("DEMO", input("Send a demo message: "))
        except LoggerException as e:
            if client.should_terminate:
                print("Closing")
            else:
                print("Cannot print last message")
                raise e


def close(client):
    if client and client.is_alive():
        # If input is blocking the thread
        print("Press Enter to quit")
    else:
        print("Exiting")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch APEX server.")
    parser.add_argument(
        "--http-port", type=int, default=8080, help="Port used for HTTP web server"
    )
    parser.add_argument(
        "--ws-port", type=int, default=8081, help="Port used for websocket server"
    )
    parser.add_argument(
        "--browser",
        type=str,
        default="chromium-browser",
        help="Path / Name of the browser to use",
    )
    parser.add_argument(
        "--www", type=str, default="./www", help="Path of the `www` directory"
    )

    args = parser.parse_args()
    try:
        # Setting the working dir for the HTTP server
        os.chdir(args.www)
        # Comment next line to disable verbose debugging output
        Logger.DEBUG_ENABLED = True
        # Starting the logger using the CLI arguments
        Logger(
            args.browser, args.http_port, args.ws_port, onReady=demo, onClosing=close
        )
    except KeyboardInterrupt:
        print("Interrupted")
        close(None)
