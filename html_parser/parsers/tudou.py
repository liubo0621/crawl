# -*- coding: utf-8 -*-
'''
Created on 2016-10-26 10:23
---------
@summary: 土豆
---------
@author: Boris
'''
import sys
sys.path.append("../..")

import html_parser.base_paser as basePaser
from html_parser.base_paser import *

EPISODE_URL      = 0
EPISODE_DESCRIBE = 1
EPISODE_INFO     = 2

VIDEO_JSON       = 0
VIDEO_URL        = 1

ITERM_JSON       = 0
ITERM_URL        = 1

#外部传进url
def parseUrl(urlInfo):
    log.debug('处理 %s'%urlInfo)

    url = urlInfo['url']
    depth = urlInfo['depth']
    websiteId = urlInfo['website_id']
    description = urlInfo['description']

    if description == Constance.EPISODE:
        if   depth == EPISODE_URL:
            parseEpisodeUrl(url, websiteId)
        elif depth == EPISODE_DESCRIBE:
            parseEpisodeDescribeUrl(url, websiteId)
        elif depth == EPISODE_INFO:
            parseEpisodeInfo(url, websiteId)
    elif description == Constance.VIDEO:
        if   depth == VIDEO_JSON:
            parseVideoInfo(url, websiteId)
        elif depth == VIDEO_URL:
            parseVideoAbstract(url, websiteId)
    elif description == Constance.ITERM:
        if   depth == ITERM_JSON:
            parseItermInfo(url, websiteId)
        elif depth == ITERM_URL:
            parseItermAbstract(url, websiteId)

def parseEpisodeUrl(sourceUrl, websiteId):
    log.debug('取剧集url %s'%sourceUrl)

    html = tools.getHtml(sourceUrl)
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    regex = '"playUrl":"(.*?)"'
    urls = tools.getInfo(html, regex, True)

    for url in urls:
        log.debug("剧集url: %s"%url)
        basePaser.addUrl(url, websiteId, EPISODE_DESCRIBE, Constance.EPISODE)

    basePaser.updateUrl(sourceUrl, Constance.DONE)

    #添加下一页的url
    if urls != []:
        currentPageRegex = 'pageNo=(\d*?)&'
        currentPage = tools.getInfo(sourceUrl, currentPageRegex)[0]
        nextPage = int(currentPage) + 1
        nextPageUrl = sourceUrl.replace('pageNo=%s'%currentPage, 'pageNo=%d'%nextPage)
        log.debug('nextPageUrl = %s'%nextPageUrl)
        # 添加到urls表 depth为0
        basePaser.addUrl(nextPageUrl, websiteId, EPISODE_URL, Constance.EPISODE)

#取剧集简介url
def parseEpisodeDescribeUrl(sourceUrl, websiteId):
    log.debug('取剧集简介 url ' + sourceUrl)
    html = tools.getHtml(sourceUrl)
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    regex = 'videoKw.*?href="(.*?)"'
    urls = tools.getInfo(html, regex)
    for url in urls:
        log.debug("剧集简介url: %s"%url)
        basePaser.addUrl(url, websiteId, EPISODE_INFO, Constance.EPISODE)

    basePaser.updateUrl(sourceUrl, Constance.DONE)

def parseEpisodeInfo(sourceUrl, websiteId):
    log.debug('解析剧集信息%s'%sourceUrl)

    html = tools.getHtml(sourceUrl, 'gbk')
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    # 片名
    regex = 'class="cover_info">.*?title="(.*?)"'
    showName = tools.getInfo(html, regex)
    showName = len(showName) > 0 and showName[0] or ''
    log.debug('片名：%s'%showName)

    # 发布时间
    regex = 'class="first".*?>(.*?)<'
    releaseTime = tools.getInfo(html, regex)
    releaseTime = len(releaseTime) > 0 and releaseTime[0] or ''
    log.debug('发布时间: %s'%releaseTime)

    # 播放量
    regex = 'class="key_item t_1".*?</span>(.*?)</span>'
    playCount = tools.getInfo(html, regex)
    playCount = len(playCount) > 0 and playCount[0] or ''
    log.debug('播放次数: %s'%playCount)

    # 集数
    regex = 'update:\'(.*?)\''
    episodeNum = tools.getInfo(html, regex)
    episodeNum = len(episodeNum) > 0 and episodeNum[0] or ''
    log.debug('集数: %s'%episodeNum)

    # 简介
    regex = 'class=\'desc\'>(.*?)</div>'
    abstract = tools.getInfo(html, regex)
    abstract = len(abstract) > 0 and abstract[0] or ''
    abstract = tools.replaceStr(abstract, '<.*?>')
    log.debug('简介: %s\n'%abstract)

    basePaser.addDocumentary(websiteId, showName, abstract, sourceUrl, episodeNum, playCount, '', releaseTime)

    basePaser.updateUrl(sourceUrl, Constance.DONE)


def parseVideoInfo(sourceUrl, websiteId):
    log.debug('解析视频信息 %s'%sourceUrl)

    html = tools.getHtml(sourceUrl)
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    json = tools.getJson(html)
    jsonArray = json['data']

    # 当没有数据时（到最后一页）  jsonArray 为[]
    #添加下一页的url
    if jsonArray != []:
        currentPageRegex = 'page=(\d*?)&'
        currentPage = tools.getInfo(sourceUrl, currentPageRegex)[0]
        nextPage = int(currentPage) + 1
        nextPageUrl = sourceUrl.replace('page=%s'%currentPage, 'page=%d'%nextPage)
        log.debug('nextPageUrl = %s'%nextPageUrl)
        # 添加到urls表 depth为0
        basePaser.addUrl(nextPageUrl, websiteId, VIDEO_JSON, Constance.VIDEO)

    # 解析当前页的信息
    for info in jsonArray:
        title = info['title']
        playTimes = str(info['playTimes'])
        pubDate = info['pubDate']
        totalTimeStr = info['totalTimeStr']
        urlCode = info['code']
        url = 'http://www.tudou.com/programs/view/%s/'%urlCode
        log.debug('视频：%s 播放次数：%s 发布时间：%s 总时长：%s url: %s'%(title, playTimes, pubDate, totalTimeStr, url))

        # # 进入url  取简介
        # videoHtml = tools.getHtml(url)
        # regex = 'class="v_desc">(.*?)</p>'
        # abstract = tools.getInfo(videoHtml, regex)
        # abstract = len(abstract) > 0 and abstract[0] or ''
        # # abstract = tools.replaceStr(abstract, '<.*?>')
        # log.debug('简介: %s\n'%abstract)
        basePaser.addUrl(url, websiteId, VIDEO_URL, Constance.VIDEO)
        basePaser.addDocumentary(websiteId, title, '', url, '', playTimes, totalTimeStr, pubDate)

    basePaser.updateUrl(sourceUrl, Constance.DONE)

def parseVideoAbstract(sourceUrl, websiteId):
    # 进入url  取简介
    videoHtml = tools.getHtml(sourceUrl)
    videoHtml = tools.getHtml(sourceUrl)
    if videoHtml == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    regex = 'class="v_desc">(.*?)</p>'
    abstract = tools.getInfo(videoHtml, regex)
    abstract = len(abstract) > 0 and abstract[0] or ''
    # abstract = tools.replaceStr(abstract, '<.*?>')
    log.debug('url: %s\n简介: %s\n'%(sourceUrl, abstract))

    basePaser.addDocumentary(websiteId, '', abstract, sourceUrl)
    basePaser.updateUrl(sourceUrl, Constance.DONE)


def parseItermInfo(sourceUrl, websiteId):
    print(websiteId)
    log.debug('解析栏目信息 %s'%sourceUrl)

    html = tools.getHtml(sourceUrl)
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    json = tools.getJson(html)
    jsonArray = json['data']
    # 当没有数据时（到最后一页）  jsonArray 为[]
    #添加下一页的url
    if jsonArray != []:
        currentPageRegex = 'page=(\d*?)&'
        currentPage = tools.getInfo(sourceUrl, currentPageRegex)[0]
        nextPage = int(currentPage) + 1
        nextPageUrl = sourceUrl.replace('page=%s'%currentPage, 'page=%d'%nextPage)
        log.debug('nextPageUrl = %s'%nextPageUrl)
        # 添加到urls表 depth为0
        basePaser.addUrl(nextPageUrl, websiteId, ITERM_JSON, Constance.ITERM)

    for info in jsonArray:
        title = info['name']
        url = info['playUrl']
        releaseTime = info['createdTime']
        itemsCount = str(info['itemsCount'])
        log.debug('视频：%s 发布时间：%s 集数：%s url: %s'%(title, releaseTime, itemsCount, url))

        basePaser.addUrl(url, websiteId, ITERM_URL, Constance.ITERM)
        basePaser.addDocumentary(websiteId, title, '', url, itemsCount, '', '', releaseTime)

    basePaser.updateUrl(sourceUrl, Constance.DONE)

def parseItermAbstract(sourceUrl, websiteId):
    # 进入url  取简介
    html = tools.getHtml(sourceUrl)
    html = tools.getHtml(sourceUrl)
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    regex = '<span class="desc">(.*?)</span>'
    abstract = tools.getInfo(html, regex)
    abstract = len(abstract) > 0 and abstract[0] or ''
    # abstract = tools.replaceStr(abstract, '<.*?>')
    log.debug('url: %s\n简介: %s\n'%(sourceUrl, abstract))

    basePaser.addDocumentary(websiteId, '', abstract, sourceUrl)
    basePaser.updateUrl(sourceUrl, Constance.DONE)

# sourceUrl = 'http://www.tudou.com/list/playlistData.action?tagType=2&firstTagId=8&areaCode=&tags=&initials=&hotSingerId=&page=1&sort=2&key='
# parseItermInfo(sourceUrl, '')