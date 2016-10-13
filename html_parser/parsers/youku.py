# encoding=utf8
import sys
sys.path.append("../..")

import base.constance as Constance
import utils.tools as tools
from utils.log import log

db = tools.connectDB()

#外部传进url
def parseUrl(urlInfo):
    log.debug(urlInfo)

    url = urlInfo['url']
    depth = urlInfo['depth']

    if depth == 0:
        parseDepth0(url)

# http://v.youku.com/v_show/id_XMTc1NDAxOTE1Mg==.html
def parseDepth0(url):
    html = tools.getHtml(url)
    # html = '<a href= "http://v.youku.com/v_show/id_XMzc4NDM3MjUy.html"/>'
    urls = tools.getUrls(html)
    for url in videoUrl:
        print(url)


