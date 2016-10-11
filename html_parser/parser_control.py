# encoding=utf8
import sys
sys.path.append("..")

import threading
import time

import base.collector as urlsollector

class  PaserControl(threading.Thread):
	def __init__(self):
		super(PaserControl, self).__init__()

	def run(self):
		while True:
			urls = urlsollector.getUrls(100)
			for url in urls:
				print(url)
				
			time.sleep(2)
		
