import os
import logging
import subprocess
from threading import Thread, Lock

from .loggerException import LoggerException

__all__ = []


class Browser(Thread):
    def __init__(
        self, browserPath=None, appAddress="http://localhost", stop_event=None
    ):
        Thread.__init__(self)
        self.browserPath = browserPath
        self.appAddress = appAddress
        self.stop_event = stop_event
        self.locks = []

    def getLock(self):
        lock = Lock()
        self.locks.append(lock)
        return lock

    def run(self):
        for lock in self.locks:
            lock.acquire()
        if self.browserPath is None:
            logging.info("Logger is ready ({})".format(self.appAddress))
            if self.stop_event:
                self.stop_event.wait()
                logging.debug("Logger received stop signal")
        elif os.access(self.browserPath, os.X_OK):
            subprocess.run(
                [self.browserPath, "--incognito", "--app=" + self.appAddress],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            logging.debug("Browser has been closed")
            if self.stop_event:
                self.stop_event.set()
        else:
            raise LoggerException(
                'FAILURE: "{}" is not executable!'.format(self.browserPath)
            )
        for lock in self.locks:
            lock.release()
