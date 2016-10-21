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

    html = tools.getHtml(sourceUrl, 'gb2312')
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return

    regex = '<span class="length">(.*?)</span>.*? href="(.*?)">(.*?)</a>.*?<p>(.*?)</p>'
    infos = tools.getInfo(html, regex)

    for info in infos:
        videoLength = info[0]
        videoUrl = info[1]
        videoName = info[2]
        videoReleaseTime = info[3]
        # 名称中有<span id='video_hl'>纪录片</span>这个信息将其过滤
        rubbishs = tools.getInfo(videoName, '<span.*?</span>')  #查找简介里面的html标签
        for rubbish in rubbishs:
            videoName = videoName.replace(rubbish, "")

        log.debug('\n片名 %s\n发布时间 %s\n时长 %s\nurl %s\n'%(videoName, videoReleaseTime, videoLength, videoUrl))
        basePaser.addDocumentary(websiteId, videoName, '', videoUrl, 1, '', videoLength, '', videoReleaseTime)

    basePaser.updateUrl(sourceUrl, Constance.DONE)