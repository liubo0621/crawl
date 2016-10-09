import urllib
import socket
import re
import pymongo #使用pip安装
from urllib.parse import quote
from urllib.error import URLError,HTTPError
from builtins import UnicodeDecodeError
from pymongo.collection import Collection


client = pymongo.MongoClient("localhost",27017)
db = client.iqiyi_struts

def getHtml(url):
    try:
        page = urllib.request.urlopen(quote(url,safe='/:?='))#获取网页page
        html = page.read().decode('utf-8','ignore')#读取页面代码
        page.close()
    except HTTPError as e:
        print(e.code)
        return 0
    except URLError as e:
        print(e.code)
        return 0
    except UnicodeDecodeError as e:
        print(e.code)
        return 0
    except socket.timeout as e:
        print(e.code)
        return 0
    return html

def getUrls(htmls):
    urls = re.compile('<a.*?\"(http:.+?)\".*?<\/a>').findall(str(htmls))
    return urls

#参数2为网址标识，如iqiyi.com
#返回url过滤后的新列表
def fitUrl(urls, identi):
    usus = []
    for link in urls:
        if identi in link:
            usus.append(link)
    return usus

def getInfo(htmls,regular):
    info = re.compile(regular).findall(str(htmls))
    info = '.'.join(info)
    return info

def dbSave(collections,dictInfo):
    db.collections.save(dictInfo)

def dbUpdata(collections,dictInfo,newdictInfo):
    db.collections.update(dictInfo,{'$set':newdictInfo})
