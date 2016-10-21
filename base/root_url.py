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
        self.addTencentUrl()

    def addUrl(self, url, websiteId, description = '', depth = 0, status = Constance.TODO):
        for i in db.urls.find({'url':url}):
            return

        urlDict = {'url':url, 'description':description, 'website_id':websiteId, 'depth':depth, 'status':Constance.TODO}
        db.urls.save(urlDict)

    def addYoukuUrl(self):
        # 取页数
        def getPageNum(pageUrl):
            html = tools.getHtml(pageUrl)

            pageNumRegexs = ['<ul class="yk-pages">.*>(.*?)</a></li><li class="next"',
                             '<ul class="yk-pages">.*>(.*?)</span></li><li class="next"'
                           ]
            pageNum = tools.getInfo(html, pageNumRegexs)
            pageNum = len(pageNum) == 0 and '0' or pageNum[0]
            # log.debug(pageNum)
            return int(pageNum)

        showUrl = 'http://list.youku.com/category/show/c_84_s_1_d_1_p_1.html'
        videoUrl = 'http://list.youku.com/category/video/c_84_d_1_s_1_p_1.html'
        showPageCount = getPageNum(showUrl)
        videoPageCount = getPageNum(videoUrl)
        websiteId = tools.getWebsiteId(Constance.YOUKU)

        ## 全部节目类
        for i in range(1, showPageCount + 1):
            url = showUrl.replace('_p_1.html', '_p_%d.html'%i)
            # log.debug("youku base url = %s"%url)
            self.addUrl(url, websiteId, 'show')

        ## 全部视频类
        for i in range(1, videoPageCount + 1):
            url = videoUrl.replace('_p_1.html', '_p_%d.html'%i)
            # log.debug("youku base url = %s"%url)
            self.addUrl(url, websiteId, 'video')

        log.debug('----------------------按节目分类-----------------------')
        ## 节目 按分类
        html = tools.getHtml(showUrl)
        # 取地区url
        regex = '<label>地区：</label>(.*?)</ul>'
        regionUrlBlock = tools.getInfo(html, regex)
        regex = 'href="(.*?)">'
        regionUrls = tools.getInfo(regionUrlBlock, regex)
        for regionUrl in regionUrls:
            log.debug("地区url = " + regionUrl)
            # 取地区下类型url
            html = tools.getHtml(regionUrl)
            regex = "<label>类型：</label>(.*?)</ul>"
            typeUrlBlock = tools.getInfo(html, regex)
            regex = 'href="(.*?)">'
            typeUrls = tools.getInfo(typeUrlBlock, regex)
            # 取每个类型的页数，拼出每页的地址，存到数据库
            for typeUrl in typeUrls:
                log.debug("typeUrl = " + typeUrl)
                pageNum = getPageNum(typeUrl)
                for i in range(1, pageNum + 1):
                    url = typeUrl.replace('.html', '_p_%d.html'%i)
                    self.addUrl(url, websiteId, 'show')

        log.debug('----------------------按视频分类-----------------------')
        ## 视频 按分类
        regex = "<label>类型：</label>(.*?)</ul>"
        html = tools.getHtml(videoUrl)
        typeUrlBlock = tools.getInfo(html, regex)
        regex = 'href="(.*?)">'
        typeUrls = tools.getInfo(typeUrlBlock, regex)
         # 取每个类型的页数，拼出每页的地址，存到数据库
        for typeUrl in typeUrls:
            log.debug("typeUrl = " + typeUrl)
            pageNum = getPageNum(typeUrl)
            for i in range(1, pageNum + 1):
                url = typeUrl.replace('.html', '_p_%d.html'%i)
                self.addUrl(url, websiteId, 'video')

    def addTencentUrl(self):
        baseUrl = 'http://v.qq.com/x/documentarylist/?itype=-1&offset=%d&sort=4'
        pageCount = 121     # 后续改成动态获取网页上的尾页  正则：'data-total="(.+)"></div)'
        websiteId = tools.getWebsiteId(Constance.TENCENT)
        #self.addUrl('http://v.qq.com/x/documentarylist/?itype=-1&offset=0&sort=4', websiteId)
        for i in range(0, pageCount * 20, 20):
            url = 'http://v.qq.com/x/documentarylist/?itype=-1&offset=%d&sort=4'%i
            log.debug("tencent base url = %s"%url)
            self.addUrl(url, websiteId)

