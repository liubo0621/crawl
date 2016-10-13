# encoding=utf8
import sys
sys.path.append("..")

import threading
import base.constance as Constance
import utils.tools as tools
from utils.log import log

db = tools.connectDB()

class AddRootUrl(threading.Thread):
    def __init__(self):
        super(AddRootUrl, self).__init__()

    def run(self):
        self.addYoukuUrl()

    def addUrl(self, url, websiteId, depth = 0, status = Constance.TODO):
        for i in db.urls.find({'url':url}):
            return

        urlDict = {'url':url, 'website_id':websiteId, 'depth':depth, 'status':status}
        db.urls.save(urlDict)

    def addYoukuUrl(self):
        baseUrl = 'http://list.youku.com/category/show/c_84_s_1_d_1_p_%d.html'
        pageCount = 30
        websiteId = tools.getWebsiteId(Constance.YOUKU)

        for i in range(1, pageCount + 1):
            url = 'http://list.youku.com/category/show/c_84_s_1_d_1_p_%d.html'%i
            # log.debug("youku base url = %s"%url)
            self.addUrl(url, websiteId)


