# encoding=utf8
import sys
sys.path.append("..")

import threading
import base.constance as Constance
import utils.tools as tools
from utils.log import log

db = tools.getConnectedDB()

class AddRootUrl(threading.Thread):
    def __init__(self):
        super(AddRootUrl, self).__init__()

    def run(self):
        self.addYoukuUrl()

    def addUrl(self, url, description, websiteId, depth = 0, status = Constance.TODO):
        for i in db.urls.find({'url':url}):
            return

        urlDict = {'url':url, 'description':description, 'website_id':websiteId, 'depth':depth, 'status':Constance.TODO}
        db.urls.save(urlDict)

    def addYoukuUrl(self):
        showUrl = 'http://list.youku.com/category/show/c_84_s_1_d_1_p_%d.html'
        videoUrl = 'http://list.youku.com/category/video/c_84_d_1_s_1_p_%d.html'
        showPageCount = 0
        videoPageCount = 19
        websiteId = tools.getWebsiteId(Constance.YOUKU)

        # 节目类
        for i in range(1, showPageCount + 1):
            url = showUrl%i
            # log.debug("youku base url = %s"%url)
            self.addUrl(url, 'show', websiteId)

        # 视频类
        for i in range(1, videoPageCount + 1):
            url = videoUrl%i
            # log.debug("youku base url = %s"%url)
            self.addUrl(url, 'video', websiteId)