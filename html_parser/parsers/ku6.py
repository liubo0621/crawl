# -*- coding: utf-8 -*-
'''
Created on 2016-10-28 14:20
---------
@summary: 酷六纪录片
---------
@author: Boris
'''

import sys
sys.path.append("../..")

import html_parser.base_paser as basePaser
from html_parser.base_paser import *

VIDEO_INFO     = 0
VIDEO_ABSTRACT = 1

#外部传进url
def parseUrl(urlInfo):
    log.debug('处理 %s'%urlInfo)

    url = urlInfo['url']
    depth = urlInfo['depth']
    websiteId = urlInfo['website_id']

    if   depth == VIDEO_INFO:
        parseVideoInfo(url, websiteId)
    elif depth == VIDEO_ABSTRACT:
        parseVideoAbstract(url, websiteId)

def parseVideoInfo(sourceUrl, websiteId):
    log.debug('取视频信息 %s'%sourceUrl)

    html = tools.getHtml(sourceUrl, 'gbk')
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    regex = 'class="time">(.*?)<.*?href="(http.*?)".*?title="(.*?)".*?播放：(.*?)<.*?发布：(.*?)<'
    infos = tools.getInfo(html, regex)

    for info in infos:
        length = info[0]
        url = info[1]
        videoName = info[2]
        playCount = info[3]
        releaseTime = info[4]

        log.debug('url : %s\n片名 : %s\n发布时间 : %s\n时长 : %s\n播放次数 : %s'%(url, videoName, releaseTime, length, playCount))

        basePaser.addUrl(url, websiteId, VIDEO_ABSTRACT)
        basePaser.addDocumentary(websiteId, videoName, '', url, '', playCount, length, releaseTime)

    basePaser.updateUrl(sourceUrl, Constance.DONE)

def parseVideoAbstract(sourceUrl, websiteId):
    log.debug('取视频 %s'%sourceUrl)

    html = tools.getHtml(sourceUrl, 'gbk')
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    regex = 'class="ckl_neir".*<p>(.*?)</p>'
    abstract = tools.getInfo(html, regex)
    abstract = abstract == [] and '' or abstract[0]
    abstract = abstract.replace('&quot;', '"')
    log.debug("url ：%s\n简介：%s"%(sourceUrl, abstract))

    basePaser.addDocumentary(websiteId, '', abstract, sourceUrl)
    basePaser.updateUrl(sourceUrl, Constance.DONE)
