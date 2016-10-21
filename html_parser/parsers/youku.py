# encoding=utf8
import sys
sys.path.append("../..")

import html_parser.base_paser as basePaser
from html_parser.base_paser import *

#depth
SHOW_URL      = 0
SHOW_DESCRIBE = 1
SHOW_INFO     = 2

#外部传进url
def parseUrl(urlInfo):
    log.debug('处理 %s'%urlInfo)

    url = urlInfo['url']
    depth = urlInfo['depth']
    websiteId = urlInfo['website_id']
    description = urlInfo['description']

    if description == 'show':
        if   depth == SHOW_URL:
            parseShowUrl(url, websiteId)
        elif depth == SHOW_DESCRIBE:
            parseShowDescribeUrl(url, websiteId)
        elif depth == SHOW_INFO:
            parseShowInfo(url, websiteId)
    elif description == 'video':
        parseVideoInfo(url, websiteId)

def parseShowUrl(sourceUrl, websiteId):
    html = tools.getHtml(sourceUrl)
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    regTypeId = basePaser.getRegexTypeId(Constance.VIDEO_URL)
    regexs = basePaser.getRegex(websiteId, regTypeId)
    urls = tools.getInfo(html, regexs)

    for url in urls:
        log.debug("节目url: %s"%url)
        basePaser.addUrl(url, websiteId, SHOW_DESCRIBE, 'show')

    basePaser.updateUrl(sourceUrl, Constance.DONE)

#取节目简介url
def parseShowDescribeUrl(sourceUrl, websiteId):
    log.debug('取节目简介 url ' + sourceUrl)
    html = tools.getHtml(sourceUrl)
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    log.debug("-------------------")
    regexs = 'class="desc-link".*?href="(.+?)"'
    urls = tools.getInfo(html, regexs)
    for url in urls:
        log.debug("节目简介url: %s"%url)
        basePaser.addUrl(url, websiteId, SHOW_INFO, 'show')

    basePaser.updateUrl(sourceUrl, Constance.DONE)
    log.debug("-------------------")

def parseShowInfo(sourceUrl, websiteId):
    log.debug('解析节目信息%s'%sourceUrl)

    html = tools.getHtml(sourceUrl)
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    #片名
    regexs = '<h1 class="title">.*?class="name">(.+?)</span>'
    showName = tools.getInfo(html, regexs)
    showName = len(showName) > 0 and showName[0] or ''
    log.debug('片名：%s'%showName)

    #集数
    regexs = 'class="basenotice">.*?([\d-]+).*?</div>'
    episodeNum = tools.getInfo(html, regexs)
    episodeNum = len(episodeNum) > 0 and episodeNum[0] or ''
    log.debug('集数: %s'%episodeNum)

    #播放量
    regexs = "总播放:.*?>([\d,]+).*?</"
    playCount = tools.getInfo(html, regexs)
    playCount = len(playCount) > 0 and playCount[0] or ''
    log.debug('播放量: %s'%playCount)

    #简介
    regexs = '<div class="detail">(.*?)</div>'
    abstract = tools.getInfo(html, regexs)
    abstract = len(abstract) > 0 and abstract[0] or ''
    rubbishs = tools.getInfo(abstract, '<.*?>')  #查找简介里面的html标签
    #去掉简介中的html标签
    for rubbish in rubbishs:
        abstract = abstract.replace(rubbish, "")

    rubbishs = tools.getInfo(abstract, '\s')  #查找简介里面的空白字符，包括空格、制表符、换页符等等
    #去掉简介中的空白字符，包括空格、制表符、换页符等等
    for rubbish in rubbishs:
        abstract = abstract.replace(rubbish, "")
    log.debug('简介: %s'%abstract)


    basePaser.addDocumentary(websiteId, showName, abstract, sourceUrl, episodeNum, playCount)

    basePaser.updateUrl(sourceUrl, Constance.DONE)

def parseVideoInfo(sourceUrl, websiteId):
    log.debug("解析视频 baserul = %s"%sourceUrl)
    html = tools.getHtml(sourceUrl)
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    #片名 播放量
    regexs = 'class="info-list">.*?href="(.+?)".*?title="\s*(.+?)\s*">.*?<li class=" ">\s*(.+?)\s*</li>'
    videosInfo = tools.getInfo(html, regexs)
    for videoInfo in videosInfo:
        videoUrl = videoInfo[0]
        videoName = videoInfo[1]
        videoPlayNum = videoInfo[2]
        log.debug("视频：%s\n播放量：%s\nurl: %s\n"%(videoName, videoPlayNum, videoUrl))
        basePaser.addDocumentary(websiteId, videoName, '', videoUrl, 1, videoPlayNum)

    basePaser.updateUrl(sourceUrl, Constance.DONE)

