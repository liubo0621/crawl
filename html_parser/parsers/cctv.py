# encoding=utf8
import sys
sys.path.append("..\..")

import html_parser.base_paser as basePaser
import utils.tools as tools
import httplib2 as httplib
import time
import fileinput
from html_parser.base_paser import *

#depth
CCTV_VIDEO_URL      = 0
CCTV_VIDEO_INFO     = 1

# CCTV纪录片相关正则
regularList1 = ['text_mod.+?<h3>(.+?)</h3>', '<p><span>集数：</span>(.+?)</p>', '<p id="shuoqi".+?简介：</span>(.+?)<a', '', '', '', '']
regularList2 = ['<td>名.*?称：</td>.+?href!="">(.+?)</a></td>', '<td>集.*?数：</td>.+?href!="">(.+?)</a></td>', '内容简介：</td>.+?brief=\'(.+?)\'', '', '', '', '', '']

def parseUrl(urlInfo):
    log.debug('处理 %s'%urlInfo)
    url = urlInfo['url']
    depth = urlInfo['depth']
    websiteId = urlInfo['website_id']

    if depth == CCTV_VIDEO_URL:
        parseRootUrl(url, websiteId, depth)
    elif depth == CCTV_VIDEO_INFO:
        parseLeafUrl(url, websiteId)

# 解析根节点
def parseRootUrl(sourceUrl, websiteId, depth):
    log.debug('解析 RootNode url = %s begin...'%sourceUrl)

    html = tools.getHtml(sourceUrl)

    reg = '<ul.*?<h3><a href="(.+?)".*?<h3><a href="(.+?)".*?<h3><a href="(.+?)".*?<h3><a href="(.+?)".*?<h3><a href="(.+?)".*?</ul>'

    urlss = tools.getInfo(html, reg)

    for urls in urlss:
        for url in urls:
            log.debug("保存视频url到DB: %s"%url)
            basePaser.addUrl(url, websiteId, depth + 1, '')

    basePaser.updateUrl(sourceUrl, Constance.DONE)

# 解析叶节点
def parseLeafUrl(sourceUrl, websiteId):
    log.debug('解析 LeafNode url = %s begin...'%sourceUrl)

    #html = tools.getHtml(sourceUrl)
    h = httplib.Http(timeout=3)
    resp,content=h.request(sourceUrl)
    html = content.decode('utf-8','ignore')
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
    regExs = ['text_mod.+?<h3>(.+?)</h3>', '<td>名.*?称：</td>.+?<a.+?>(.+?)</a></td>']
    for reg in regExs:
        videoName = ''.join(tools.getInfo(html, reg))
        if videoName != '': break
    log.debug('专辑名称: %s'%videoName)

    # 集数
    videoNumber = ''
    regExs = ['<p><span>集.*?数：.*?</span>(.*?)</p>', '<td>集.*?数：</td>.+?<a.+?>(.*?)</a></td>']
    for reg in regExs:
        videoNumber = ''.join(tools.getInfo(html, reg))
        if videoNumber != '': break
    log.debug('集数: %s'%videoNumber)

    # 简介
    videoDescription = ''
    regExs = ['<p id="shuoqi".+?简.*?介：</span>(.+?)<a', '内.*?容.*?简.*?介：</td>.+?brief=\'(.+?)\'']
    for reg in regExs:
        videoDescription = ''.join(tools.getInfo(html, reg))
        if videoDescription != '': break
    log.debug('简介: %s'%videoDescription)

    # 总播放量
    videoPlayCount = ''
    log.debug('总播放量暂无。。。')

    # url
    log.debug('URL = %s'%sourceUrl)

    # 总片长 (单位秒)
    videoAllTime = ''
    log.debug('总片长暂无。。。')

    # 播出机构
    videoPlayCompany = ''
    log.debug('播出机构暂无。。。')

    # 发布时间
    videoReleaseTime = ''
    log.debug('发布时间暂无。。。')

    # 百度百科上的信息
    videoBaiduInfo = ''
    log.debug('百度百科上的信息暂无。。。')

    log.debug('URL=%s正则匹配详细信息结束。。。'%sourceUrl)

    basePaser.addDocumentary(websiteId, videoName, videoDescription, sourceUrl, videoNumber)
    basePaser.updateUrl(sourceUrl, Constance.DONE)

def myTest():
    websiteId = tools.getWebsiteId('cctv.com')
    urls = []
    f = open('D:\html.txt', 'r')
    while True:
        line = f.readline()
        if not line: break
        url = tools.getInfo(line, '"url".+"(.+?)"')
        if url != []:
            urls.extend(url)

    for url in urls:
        parseLeafUrl(url, websiteId)

#myTest()