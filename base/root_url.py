# encoding=utf8
import sys
sys.path.append("..")

import threading
import fileinput
import base.constance as Constance
import utils.tools as tools
from utils.log import log

db = tools.getConnectedDB()

class AddRootUrl(threading.Thread):
    def __init__(self):
        super(AddRootUrl, self).__init__()

    def run(self):
        website = tools.getConfValue("collector", "website")
        if website == 'all':
            self.addYoukuUrl()
            self.addTencentUrl()
            self.addWangYiUrl()
            self.addPPTVUrl()
            self.addCCTVUrl()
            self.addKanKanUrl()
            self.addTouDouUrl()
            self.addV1Url()

        elif website == Constance.YOUKU:
            self.addYoukuUrl()
        elif website == Constance.TENCENT:
            self.addTencentUrl()
        elif website == Constance.WANG_YI:
            self.addWangYiUrl()
        elif website == Constance.PPTV:
            self.addPPTVUrl()
        elif website == Constance.CCTV:
            self.addCCTVUrl()
        elif website == Constance.KAN_KAN:
            self.addKanKanUrl()
        elif website == Constance.TUDOU:
            self.addTouDouUrl()
        elif website == Constance.V1:
            self.addV1Url()


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

    def addWangYiUrl(self):
        baseUrl = 'http://so.v.163.com/search/000-0-0000-1-%d-0-纪录片/'
        pageCount = 614
        websiteId = tools.getWebsiteId(Constance.WANG_YI)
        for i in range(1, pageCount + 1):
            url = baseUrl%i
            log.debug("wangyi base url = %s"%url)
            self.addUrl(url, websiteId)

    def addPPTVUrl(self):
        baseUrl = 'http://list.pptv.com/channel_list.html?page=%d&type=210548&sort=1'
        pageCount = 17
        websiteId = tools.getWebsiteId(Constance.PPTV)
        for i in range(1, pageCount + 1):
            url = baseUrl%i
            log.debug("pptv base url = %s"%url)
            self.addUrl(url, websiteId)

    def addCCTVUrl(self):
        urlsList = []
        filepath = '..\\urls\\cctv.conf'
        for line in fileinput.input(filepath):
            url = tools.getInfo(line, '= (.+?)\n')
            if url:
                urlsList.extend(url)

        websiteId = tools.getWebsiteId(Constance.CCTV)

        for url in urlsList:
            log.debug("Add url %s to DB"%url)
            self.addUrl(url, websiteId)

    def addKanKanUrl(self):
        def getPageNum(url):
            html = tools.getHtml(url)
            regex = 'list-pager-v2.*>(.*?)</a><a id="pagenav_next"'
            pageNum = tools.getInfo(html, regex)
            pageNum = len(pageNum) == 0 and '1' or pageNum[0]
            # log.debug(pageNum)
            return int(pageNum)

        # 全部视频
        websiteId = tools.getWebsiteId(Constance.KAN_KAN)
        baseUrl = 'http://movie.kankan.com/type/documentary/'
        log.debug("kankan base url = %s"%baseUrl)
        self.addUrl(baseUrl, websiteId)

        pageCount = getPageNum(baseUrl)
        log.debug("kankan 页数 = %d"%pageCount)
        for i in range(2, pageCount + 1):
            url = baseUrl + 'page%d/'%i
            log.debug("kankan base url = %s"%url)
            self.addUrl(url, websiteId)

        # 按类型
        log.debug('----------------------按类型分类-----------------------')
        regex = '"div_genre">(.*?)</dd>'
        html = tools.getHtml(baseUrl)
        typeBlockUrl = tools.getInfo(html, regex)

        regex = ' href="(.*?)"'
        typeUrls = tools.getInfo(typeBlockUrl, regex)
        for typeBaseUrl in typeUrls:
            log.debug("kankan type base url = %s"%typeBaseUrl)
            pageCount = getPageNum(typeBaseUrl)
            log.debug("kankan 页数 = %d"%pageCount)

            self.addUrl(typeBaseUrl, websiteId)

            for i in range(2, pageCount + 1):
                url = typeBaseUrl + 'page%d/'%i
                log.debug("kankan type base url = %s"%url)
                self.addUrl(url, websiteId)

    def addTouDouUrl(self):
        # 全部 剧集
        # 添加首页 后续页面在tudou里添加
        baseUrl = 'http://www.tudou.com/s3portal/service/pianku/data.action?pageSize=90&app=mainsitepc&deviceType=1&tags=&tagType=3&firstTagId=8&areaCode=&initials=&hotSingerId=&pageNo=1&sortDesc=quality'
        websiteId = tools.getWebsiteId(Constance.TUDOU)
        self.addUrl(baseUrl, websiteId, Constance.EPISODE)

        # 视频
        # 添加首页 后续页面在tudou里添加
        baseUrl = 'http://www.tudou.com/list/itemData.action?tagType=1&firstTagId=8&areaCode=&tags=&initials=&hotSingerId=&page=1&sort=2&key='
        websiteId = tools.getWebsiteId(Constance.TUDOU)
        self.addUrl(baseUrl, websiteId, Constance.VIDEO)

        # 栏目
        # 添加首页 后续页面在tudou里添加
        baseUrl = 'http://www.tudou.com/list/playlistData.action?tagType=2&firstTagId=8&areaCode=&tags=&initials=&hotSingerId=&page=1&sort=2&key='
        websiteId = tools.getWebsiteId(Constance.TUDOU)
        self.addUrl(baseUrl, websiteId, Constance.ITERM)

    def addV1Url(self):
        # 添加首页 后续页面在tudou里添加
        baseUrl = 'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery18308286485691806487_1477619118750&obj=cms.getArticle&cid=1147&page=1&nums=24&_=1477619416282'
        websiteId = tools.getWebsiteId(Constance.V1)
        self.addUrl(baseUrl, websiteId)