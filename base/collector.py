# encoding=utf8
import sys
sys.path.append("..")

import threading  
import time
# from collections import deque

import utils.tools as tools

mylock = threading.RLock()

# queue.append("Terry") 
# queue.popleft()

urls = []

class Collector(threading.Thread):
	def __init__(self):
		super(Collector, self).__init__()
		self._interval = int(tools.getConfValue("collector", "sleep_time"))
		self._threadStop = False

	def run(self):
		while not self._threadStop:
			self.__inputData()
			time.sleep(self._interval)

	def stop(self):
		self._threadStop = False

	def __inputData(self):
		mylock.acquire() #加锁

		db = tools.connectDB()
		site = tools.getConfValue("collector", "site")
		deep = int(tools.getConfValue("collector", "deep"))
		urlCount = int(tools.getConfValue("collector", "url_count"))
		if site == 'all':
			urlsList = db.urls.find({"status":0, "deep":{"$lte":deep}},{"url":1, "_id":0,"deep":1, "site":1}).sort([("deep",1)]).limit(urlCount)#sort -1 降序 1 升序
		else:
			urlsList = db.urls.find({"status":0, "site":site, "deep":{"$lte":deep}},{"url":1, "_id":0,"deep":1, "site":1}).sort([("deep",1)]).limit(urlCount)

		global urls
		urls.extend(urlsList)

		mylock.release()
			

def getUrls(count):
		mylock.acquire() #加锁
		
		urls_ = urls[:count]
		del urls[:count]
		
		mylock.release()

		return urls_
		

	

