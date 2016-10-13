# encoding=utf8
import urllib
import socket
import re
import pymongo
import configparser #读配置文件的
from urllib.parse import quote
from urllib.error import URLError,HTTPError
from builtins import UnicodeDecodeError
from pymongo.collection import Collection


def getHtml(url):
    try:
        page = urllib.request.urlopen(quote(url,safe='/:?='))
        html = page.read().decode('utf-8','ignore')
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

##################################################
def getConfValue(section, key):
    cf = configparser.ConfigParser()
    cf.read("../crawl.conf")
    return cf.get(section, key)

##################################################
class DB():
    client = pymongo.MongoClient("localhost",27017)
    db = client.crawl

db = DB.db
def connectDB():
    return db

def dbSave(collection,dictInfo):
    db.getCollection(collection).save(dictInfo)

def dbUpdata(collection,dictInfo,newdictInfo):
    db.getCollection(collection).update(dictInfo,{'$set':newdictInfo})

def dbFind(collection,condition):
    return db.getCollection(collection).find(condition)
