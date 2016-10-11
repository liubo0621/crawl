# encoding=utf8
import sys
sys.path.append("..")

import utils.tools as tools
from base.collector import Collector

from html_parser.parser_control import PaserControl

def init():
	pass

if __name__ == '__main__':
	tools.connectDB()

	coll = Collector()
	coll.start()

	paser = PaserControl()
	paser.start()

	paser2 = PaserControl()
	paser2.start()