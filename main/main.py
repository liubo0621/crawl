# encoding=utf8
import sys
sys.path.append("..")

import utils.tools as tools
from utils.log import log
from base.collector import Collector
from html_parser.parser_control import PaserControl
import os

def init():
    pass

if __name__ == '__main__':
    log.info("--------begin--------")
    tools.connectDB()

    coll = Collector()
    coll.start()

    paserCount = int(tools.getConfValue("html_parser", "parser_count"))
    while paserCount:
       paser = PaserControl()
       paser.start()
       paserCount = paserCount - 1