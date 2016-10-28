# -*- coding: utf-8 -*-
'''
Created on 2016-10-27 17:44
---------
@summary: 第一视频纪录片
---------
@author: Boris
'''

import sys
sys.path.append("../..")

import html_parser.base_paser as basePaser
from html_parser.base_paser import *

#外部传进url
def parseUrl(urlInfo):
    log.debug('处理 %s'%urlInfo)

    sourceUrl = urlInfo['url']
    websiteId = urlInfo['website_id']

    html = tools.getHtml(sourceUrl)
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    # print(html)
    regex = "\('(.*?)'\)"
    jsonStr = tools.getInfo(html, regex)[0]
    # 去掉多余的反斜杠
    jsonStr = jsonStr.replace('\\\\', '~~~')
    jsonStr = jsonStr.replace('\\', '')
    jsonStr = jsonStr.replace('~~~', '\\')

    # log.debug(u'%s'%jsonStr)
    json = tools.getJson(jsonStr)
    jsonArray = json['result']['data']['items']

    if jsonArray != None:
        # 添加下一页的url
        currentPageRegex = 'page=(\d*?)&'
        currentPage = tools.getInfo(sourceUrl, currentPageRegex)[0]
        nextPage = int(currentPage) + 1
        nextPageUrl = sourceUrl.replace('page=%s'%currentPage, 'page=%d'%nextPage)
        log.debug('nextPageUrl = %s'%nextPageUrl)
        # 添加到urls表 depth为0
        basePaser.addUrl(nextPageUrl, websiteId, 0)

        #取当前页的信息
        for info in jsonArray:
            url = info['url']
            videoName = info['title']
            releaseTime = info['create_time']
            source = info['source']
            abstract = info['intro']
            length = info['duration']
            playtimes = info['pv']

            log.debug('url : %s\n片名 : %s\n发布时间 : %s\n时长 : %s\n播放次数 : %s\n来源 : %s\n简介 : %s'%(url, videoName, releaseTime, length, playtimes, source, abstract))
            basePaser.addDocumentary(websiteId, videoName, abstract, url, '', playtimes, length, releaseTime, source)

    basePaser.updateUrl(sourceUrl, Constance.DONE)

def parseInfo(sourceUrl):
    html = tools.getHtml(sourceUrl)
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    # print(html)
    regex = "\('(.*?)'\)"
    jsonStr = tools.getInfo(html, regex)[0]
    # 去掉多余的反斜杠
    jsonStr = jsonStr.replace('\\\\', '~~~')
    jsonStr = jsonStr.replace('\\', '')
    jsonStr = jsonStr.replace('~~~', '\\')

    # log.debug(u'%s'%jsonStr)
    json = tools.getJson(jsonStr)
    jsonArray = json['result']['data']['items']

    if jsonArray != None:
        # 添加下一页的url
        currentPageRegex = 'page=(\d*?)&'
        currentPage = tools.getInfo(sourceUrl, currentPageRegex)[0]
        nextPage = int(currentPage) + 1
        nextPageUrl = sourceUrl.replace('page=%s'%currentPage, 'page=%d'%nextPage)
        log.debug('nextPageUrl = %s'%nextPageUrl)
        # 添加到urls表 depth为0
        basePaser.addUrl(nextPageUrl, websiteId, 0)

        #取当前页的信息
        for info in jsonArray:
            url = info['url']
            videoName = info['title']
            releaseTime = info['create_time']
            source = info['source']
            abstract = info['intro']
            length = info['duration']
            playtimes = info['pv']

            log.debug('url : %s\n片名 : %s\n发布时间 : %s\n时长 : %s\n播放次数 : %s\n来源 : %s\n简介 : %s'%(url, videoName, releaseTime, length, playtimes, source, abstract))
            basePaser.addDocumentary(websiteId, videoName, abstract, url, '', playtimes, length, releaseTime, source)

    basePaser.updateUrl(sourceUrl, Constance.DONE)

# url = 'http://api.v1.cn/v1Enhanced/interfaceForJsonP?callback=jQuery18308286485691806487_1477619118750&obj=cms.getArticle&cid=1147&page=1&nums=24&_=1477619416282'
# parseInfo(url)