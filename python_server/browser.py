import os
import subprocess
from threading import Thread

class Browser(Thread):
    def __init__(self, browserPath="chrome", appAddress = "http://localhost"):
        Thread.__init__(self)
        self.browserPath = browserPath
        self.appAddress = appAddress

    def run(self):
        subprocess.run([self.browserPath,"--app="+self.appAddress])
        os._exit(0)
