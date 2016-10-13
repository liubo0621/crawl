# encoding=utf8
import sys
sys.path.append("../..")

import base.constance as Constance
import utils.tools as tools
from utils.log import log

db = tools.connectDB()

def parseUrl(url):
    log.debug(url)
