# encoding=utf8
import sys
sys.path.append("..\..")

import html_parser.base_paser as basePaser
import utils.tools as tools
import httplib2 as httplib
import time
from html_parser.base_paser import *

#depth
TENCENT_VIDEO_URL      = 0
TENCENT_VIDEO_INFO     = 1

# 腾讯纪录片相关正则列表
regularList = ['player_title">(.+?)\s*<', '专辑总数据.+共([\d]+)', 'itemprop="description" content="(.+?)">?', 'total_count">总播放量.+?>(.+?)</em>', '<span class="figure_info">(.+?)</span>', '', 'meta itemprop="datePublished" content="(.+?)"', '']

def parseUrl(urlInfo):
	log.debug('处理 %s'%urlInfo)

	url = urlInfo['url']
	depth = urlInfo['depth']
	websiteId = urlInfo['website_id']

	if depth == TENCENT_VIDEO_URL:
		parseRootUrl(url, websiteId, depth)
	elif depth == TENCENT_VIDEO_INFO:
		parseLeafUrl(url, websiteId)

def parseRootUrl(sourceUrl, websiteId, depth):
    #html = tools.getHtml(sourceUrl)
    h = httplib.Http()
    resp,content=h.request(sourceUrl)
    html = content.decode('utf-8','ignore')

    regexs = 'data-trigger-class="list_item_hover">.+?href="(.+?)"'
    urls = tools.getInfo(html, regexs)

    for url in urls:
        log.debug("保存视频url到DB: %s"%url)
        basePaser.addUrl(url, websiteId, depth + 1, '')

    basePaser.updateUrl(sourceUrl, Constance.DONE)

def parseLeafUrl(sourceUrl, websiteId):
    log.debug("视频url: %s"%sourceUrl)
    #html = tools.getHtml(sourceUrl)
    h = httplib.Http()
    resp,content=h.request(sourceUrl)
    html = content.decode('utf-8','ignore')

    albumInfo = []
    for i in regularList:
        albumInfo.append(tools.getInfo(html, i, True))

    # 分集时间求出总时间 单位：s
    albumInfo[4] = tools.timeListToString(albumInfo[4])

    basePaser.addDocumentaryList(websiteId, albumInfo)

    basePaser.updateUrl(sourceUrl, Constance.DONE)