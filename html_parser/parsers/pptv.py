# enconding = utf-8
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

    # 匹配带期数的
    regex = 'ui-list-ct.*?href=\'(.*?)\'.*?class="msk-txt">(.*?)<.*?class="main-tt">(.*?)</span>'
    infos = tools.getInfo(html, regex)
    for info in infos:
        print(info)
        videoUrl = info[0]
        videoReleaseTime = info[1]
        videoName = info[2]
        log.debug('\n片名 %s\n发布时间 %s\nnurl %s\n'%(videoName, videoReleaseTime, videoUrl))
        basePaser.addDocumentary(websiteId, videoName, '', videoUrl, '', '', '', videoReleaseTime)



    print('-'*40)
    regex = 'ui-list-ct.*?href=\'(.*?)\'.*?class="main-tt">(.*?)</span>'
    infos = tools.getInfo(html, regex)
    for info in infos:
        videoUrl = info[0]
        videoName = info[1]
        log.debug('\n片名 %s\nurl %s\n'%(videoName, videoUrl))
        basePaser.addDocumentary(websiteId, videoName, '', videoUrl, '', '', '', '', '')

    basePaser.updateUrl(sourceUrl, Constance.DONE)