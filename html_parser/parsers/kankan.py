# enconding = utf-8
import sys
sys.path.append("../..")

import html_parser.base_paser as basePaser
from html_parser.base_paser import *

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

    if   depth == SHOW_URL:
        parseShowUrl(url, websiteId)
    elif depth == SHOW_DESCRIBE:
        parseShowDescribeUrl(url, websiteId)
    elif depth == SHOW_INFO:
        parseShowInfo(url, websiteId)

def parseShowUrl(sourceUrl, websiteId):
    html = tools.getHtml(sourceUrl)
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    regex = 'movielist_tt.*?href="(.*?)"'
    urls = tools.getInfo(html, regex)

    for url in urls:
        log.debug("节目url: %s"%url)
        if url.endswith('.shtml'):
            basePaser.addUrl(url, websiteId, SHOW_DESCRIBE)
        else:
            basePaser.addUrl(url, websiteId, SHOW_INFO)

    basePaser.updateUrl(sourceUrl, Constance.DONE)


#取节目简介url
def parseShowDescribeUrl(sourceUrl, websiteId):
    log.debug('取节目简介 url ' + sourceUrl)
    html = tools.getHtml(sourceUrl)
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    regex = 'movieTitle.*?href="(.*?)"'
    urls = tools.getInfo(html, regex)
    for url in urls:
        log.debug("节目详情url: %s"%url)
        basePaser.addUrl(url, websiteId, SHOW_INFO)

    basePaser.updateUrl(sourceUrl, Constance.DONE)



def parseShowInfo(sourceUrl, websiteId):
    log.debug('解析节目信息%s'%sourceUrl)

    html = tools.getHtml(sourceUrl)
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    # 节目名
    regex = "<h1>(.*?)</h1>"
    showName = tools.getInfo(html, regex)
    showName = len(showName) > 0 and showName[0] or ''
    showName = tools.replaceStr(showName, '<.*?>')
    log.debug('片名：%s'%showName)

    # 播放次数
    regex = "播放次数.*?>(.*?)<"
    playCount = tools.getInfo(html, regex)
    playCount = len(playCount) > 0 and playCount[0] or ''
    log.debug('播放次数: %s'%playCount)

    # 发布时间
    regex = '<li>年份.*?>(.*?)<'
    releaseTime = tools.getInfo(html, regex)
    releaseTime = len(releaseTime) > 0 and releaseTime[0] or ''
    log.debug('发布时间: %s'%releaseTime)

    # 集数
    regex = '更新至\s*?(.*?)<'
    episodeNum = tools.getInfo(html, regex)
    episodeNum = len(episodeNum) > 0 and episodeNum[0] or ''
    log.debug('集数: %s'%episodeNum)

    # 片长
    regex = '片长.*?>(.*?)<'
    showLength = tools.getInfo(html, regex)
    showLength = len(showLength) > 0 and showLength[0] or ''
    log.debug('片长: %s'%showLength)

    # 简介
    # 带详情的和不带详情的
    regexs = ['intro_cont_all.*?<p>(.*?)<span', 'introduction.*?<p>(.*?)</div>']
    abstract = tools.getInfo(html, regexs)
    abstract = len(abstract) > 0 and abstract[0] or ''
    abstract = tools.replaceStr(abstract, '<.*?>')
    abstract = tools.replaceStr(abstract, '&ldquo;|&rdquo;')
    log.debug('简介: %s\n'%abstract)

    basePaser.addDocumentary(websiteId, showName, abstract, sourceUrl, episodeNum, playCount, showLength, releaseTime)

    basePaser.updateUrl(sourceUrl, Constance.DONE)
