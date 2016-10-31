# encoding=utf8
import sys
sys.path.append("..\..")

import html_parser.base_paser as basePaser
import utils.tools as tools
import httplib2 as httplib
import time
from html_parser.base_paser import *
from selenium import webdriver

#depth
TENCENT_VIDEO_URL      = 0
TENCENT_VIDEO_INFO     = 1

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
    log.debug('解析 LeafNode url = %s begin...'%sourceUrl)

    try:
        driver = webdriver.PhantomJS()
        driver.get(sourceUrl)
        time.sleep(2)
        html = driver.page_source
    finally:
        driver.quit()

    #html = tools.getHtml(sourceUrl)
    #h = httplib.Http(timeout=3)
    #resp,content=h.request(sourceUrl)
    #html = content.decode('utf-8','ignore')
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        log.debug('未能正确获取此URL源码%s ！！！'%sourceUrl)
        return
        f = open('D:\cctv_html.txt', 'a+')
        f.write(sourceUrl)
        f.write('\n')
        f.close()
        return

    log.debug('URL=%s正则匹配详细信息开始。。。'%sourceUrl)
    # 专辑名称
    videoName = ''
    regExs = ['player_title">(.+?)[\s]*<']
    for reg in regExs:
        videoName = ''.join(tools.getInfo(html, reg))
        if videoName != '': break
    log.debug('专辑名称: %s'%videoName)

    # 集数
    videoNumber = ''
    regExs = ['专辑总数据.+共([\d]+?)个']
    for reg in regExs:
        videoNumber = ''.join(tools.getInfo(html, reg))
        if videoNumber != '': break
    log.debug('集数: %s'%videoNumber)

    # 简介
    videoDescription = ''
    regExs = ['itemprop="description" content="(.*?)">?']
    for reg in regExs:
        videoDescription = ''.join(tools.getInfo(html, reg))
        if videoDescription != '': break
    log.debug('简介: %s'%videoDescription)

    # 总播放量
    videoPlayCount = ''
    regExs = ['mod_album_total.+?total_count">总播放量.+?>(.*?)</em>']
    for reg in regExs:
        videoPlayCount = ''.join(tools.getInfo(html, reg))
        if videoPlayCount != '': break
    log.debug('总播放量: %s'%videoPlayCount)

    # url
    log.debug('URL = %s'%sourceUrl)

    # 总片长 (单位秒)
    videoAllTime = ''
    regExs = ['<span class="figure_info">(.*?)</span>']
    for reg in regExs:
        videoAllTime = ''.join(tools.timeListToString(tools.getInfo(html, reg)))
        if videoAllTime != '': break
    log.debug('总片长 : %s'%videoAllTime)

    # 发布时间
    videoReleaseTime = ''
    regExs = ['meta itemprop="datePublished" content="(.*?)"']
    for reg in regExs:
        videoReleaseTime = ''.join(tools.getInfo(html, reg))
        if videoReleaseTime != '': break
    log.debug('发布时间 : %s'%videoReleaseTime)

    # 播出机构
    videoPlayCompany = ''
    log.debug('播出机构暂无。。。')

    # 百度百科上的信息
    videoBaiduInfo = ''
    log.debug('百度百科上的信息暂无。。。')

    log.debug('URL=%s正则匹配详细信息结束。。。'%sourceUrl)

    basePaser.addDocumentary(websiteId, videoName, videoDescription, sourceUrl, videoNumber, videoPlayCount, videoAllTime, videoReleaseTime)
    basePaser.updateUrl(sourceUrl, Constance.DONE)

def test():
    sourceUrl = 'http://v.qq.com/x/cover/4oocb872jxju3c6.html'
    driver = webdriver.PhantomJS()
    driver.get(sourceUrl)
    time.sleep(2)

    html = driver.page_source
    driver.quit()

    reg = 'mod_album_total.+?total_count">总播放量.+?>(.*?)</em>'
    info = tools.getInfo(html, reg)
    print(info)

#test()