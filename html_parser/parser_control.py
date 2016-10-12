# encoding=utf8
import sys
sys.path.append("..")

import threading
import time
import utils.tools as tools
import base.constance as Constance
from html_parser.parsers import *
from base.collector import Collector

class  PaserControl(threading.Thread):
    def __init__(self):
        super(PaserControl, self).__init__()
        self._collector = Collector()
        self._urlCount = int(tools.getConfValue("html_parser", "url_count"))
        self._interval = int(tools.getConfValue("html_parser", "sleep_time"))

    def run(self):
        while True:
            urls = self._collector.getUrls(self._urlCount)
            for url in urls:
                self.parseUrl(url)

            time.sleep(self._interval)

    def parseUrl(self, urlInfo):
        if urlInfo['site'] == Constance.YOUKU:
            youku.parseUrl(urlInfo)

