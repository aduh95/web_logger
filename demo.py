#!/usr/bin/env python3

import os
import argparse
import logging

from pyhtmllogger import Logger, LoggerException


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


def cleanClient(logger):
    logging.debug("Demo: Let's flush all those non-sense messages")
    logger.clean()


def demo(logger):
    logging.debug("Demo: Client is ready")
    logger.defineNewMenu(
        [
            {
                "label": "Configuration",
                "click": None,
                "submenu": [
                    {"label": "test", "click": commandExample},
                    {"label": "Clean APEX", "click": lambda: cleanClient(logger)},
                ],
            },
            {"label": "Manage targets", "submenu": []},
            {"label": "Quit", "click": logger.stop},
        ]
    )
    while not logger.stop_event.is_set():
        try:
            logger.log("DEMO", input("Send a demo message: "))
        except LoggerException as e:
            if logger.stop_event.is_set():
                logging.debug("Demo: Closing")
            else:
                logging.debug("Demo: Cannot log last message")
                raise e


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch APEX server.")
    parser.add_argument(
        "--http-port", type=int, default=8080, help="Port used for HTTP web server"
    )
    parser.add_argument(
        "--ws-port", type=int, default=8081, help="Port used for websocket server"
    )
    parser.add_argument(
        "--browser", type=str, default=None, help="Path / Name of the browser to use"
    )
    parser.add_argument(
        "--www", type=str, default="./www", help="Path of the `www` directory"
    )

    args = parser.parse_args()
    logger = None
    try:
        # Setting the working dir for the HTTP server
        os.chdir(args.www)
        # Comment next line to disable verbose debugging output
        logging.basicConfig(level=logging.DEBUG)
        # Starting the logger using the CLI arguments
        logger = Logger(args.browser, args.http_port, args.ws_port, onReady=demo)
        # thread will now awaits until logger terminates
        logging.info("Logger has ended")
    except KeyboardInterrupt:
        logging.debug("Demo: Interrupted")
    finally:
        while logger and logger.is_alive():
            # If input is blocking the thread
            print("Demo: Press Enter to quit")
            logger.join(3)  # print the message every 3 seconds
        else:
            logging.debug("Demo: Exiting")
