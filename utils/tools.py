# encoding=utf8
from urllib import request
import socket
import re
import pymongo
import configparser #读配置文件的
from urllib.parse import quote
from urllib.error import URLError,HTTPError
from builtins import UnicodeDecodeError
from pymongo.collection import Collection
import sys
sys.path.append("..")
from utils.log import log


def getHtml(url):
    try:
        page = request.urlopen(quote(url,safe='/:?='))
        html = page.read().decode('utf-8','ignore')
        page.close()
    except HTTPError as e:
        print(e)
        return None
    except URLError as e:
        print(e)
        return None
    except UnicodeDecodeError as e:
        print(e)
        return None
    except socket.timeout as e:
        print(e)
        return None
    except Exception as e:
        print(e)
        return None
    return html

def getUrls(html):
    urls = re.compile('<a.*\"(https?.+?)\"').findall(str(html))
    return list(set(urls))

def fitUrl(urls, identi):
    usus = []
    for link in urls:
        if identi in link:
            usus.append(link)
    return list(set(usus))

def getInfo(html,regexs):
    regexs = isinstance(regexs, str) and [regexs] or regexs

    for regex in regexs:
        infos = re.findall(regex,str(html),re.S)
        # infos = re.compile(regexs).findall(str(html))
        if len(infos) > 0:
            break

    return list(set(infos))


##################################################
def getConfValue(section, key):
    cf = configparser.ConfigParser()
    cf.read("../crawl.conf")
    return cf.get(section, key)

##################################################

#################时间转换相关####################
def TimeListToString(timeList):
    Times = 0
    for word in timeList:
        Times = Times + TimeToString(word)
    return str(Times)

def TimeToString(time):
    timeList = time.split(':')
    if len(timeList) == 3 :
        return int(timeList[0]) * 3600 + int(timeList[1]) * 60 + int(timeList[2])
    elif len(timeList) == 2:
        return int(timeList[0]) * 60 + int(timeList[1])

##################################################
class DB():
    client = pymongo.MongoClient("localhost",27017)
    db = client.crawl

db = DB.db
def getConnectedDB():
    return db

def dbSave(collection,dictInfo):
    db.getCollection(collection).save(dictInfo)

def dbUpdata(collection,dictInfo,newdictInfo):
    db.getCollection(collection).update(dictInfo,{'$set':newdictInfo})

def dbFind(collection,condition):
    return db.getCollection(collection).find(condition)


##################################################
def getWebsiteId(domain):
    website = list(db.website.find({'domain':domain}))
    websiteId = None
    if len(website) > 0:
        websiteId = website[0]['_id']
    else:
        log.warning('website表中无%s信息，需先手动添加'%domain)

    return websiteId