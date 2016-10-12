# encoding=utf8
import sys
sys.path.append("..")

import threading
import time

from base.collector import Collector

class  PaserControl(threading.Thread):
    def __init__(self):
        super(PaserControl, self).__init__()
        self._collector = Collector()

    def run(self):
        while True:
            urls = self._collector.getUrls(100)
            for url in urls:
                print(url)

            time.sleep(2)

