import os
import subprocess
from threading import Thread, Lock


class Browser(Thread):
    def __init__(self, browserPath="chrome", appAddress="http://localhost"):
        Thread.__init__(self)
        self.browserPath = browserPath
        self.appAddress = appAddress
        self.locks = []

    def getLock(self):
        lock = Lock()
        self.locks.append(lock)
        return lock

    def run(self):
        for lock in self.locks:
            lock.acquire()
        if os.access(self.browserPath, os.X_OK):
            subprocess.run(
                [self.browserPath, "--incognito", "--app=" + self.appAddress],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        else:
            print("ERROR: browser is not executable! Aborting...")
        print("Browser has been closed")
        os._exit(0)
