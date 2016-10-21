# encoding=utf8
import sys
sys.path.append("..")

import base.constance as Constance
import utils.tools as tools
from utils.log import log

db = tools.getConnectedDB()

def getWebsiteId(domain):
    website = list(db.website.find({'domain':domain}))
    websiteId = None
    if len(website) > 0:
        websiteId = website[0]['_id']
    else:
        log.warning('website表中无%s信息，需先手动添加'%domain)

    return websiteId

def getRegexTypeId(regType):
    regexType = list(db.regex_type.find({'type':regType}))
    regexTypeId = None
    if len(regexType) > 0:
        regexTypeId = regexType[0]['_id']
    else:
        log.warning('regex_type无%s信息，需先手动添加'%regType)

    return regexTypeId

def getRegex(websiteId, regTypeId):
    regexs = []
    for regex in db.regexs.find({'website_id':websiteId, 'type_id':regTypeId}, {'regex':1, '_id':0}):
        regexs.append(regex['regex'])
    return regexs

##################################################
def addUrl(url, websiteId, depth, description, status = Constance.TODO):
    for i in db.urls.find({'url':url}):
        return

    urlDict = {'url':url, 'website_id':websiteId, 'depth':depth, 'description':description, 'status':status}
    db.urls.save(urlDict)

def updateUrl(url, status):
    db.urls.update({'url':url}, {'$set':{'status':status}}, multi=True)

# |doc_name||||片名|
# |episode_num||||集数|
# |abstract||||简介|
# |play_num||||总播放量|
# |url||||纪录片url|
# |total_length||||总片长 (单位秒)|
# |institutions||||播出机构|
# |release_time||||发布时间|
# |cyclopedia_msg||||百度百科上的信息|
# |website_id||||网站id|
def addAocumentary(websiteId, docName, abstract, url, episodeNum = '', playNum = '', totalLength = '', institutions = '', releaseTime = '', cyclopediaMsg = ''):
    aocumentaryDict = {
        'website_id':websiteId,
        'doc_name':docName,
        'abstract':abstract,
        'url':url,
        'episode_num':episodeNum,
        'play_num':playNum,
        'total_length':totalLength,
        'institutions':institutions,
        'release_time':releaseTime,
        'cyclopedia_msg':cyclopediaMsg
        }

    for i in db.documentary.find(aocumentaryDict):
        return

    db.documentary.save(aocumentaryDict)

def addAocumentaryList(websiteId, inforList):
    aocumentaryDict = {
        'website_id':websiteId,
        'doc_name':inforList[0],
        'episode_num':inforList[1],
        'abstract':inforList[2],
        'play_num':inforList[3],
        'total_length':inforList[4],
        'institutions':inforList[5],
        'release_time':inforList[6],
        'cyclopedia_msg':inforList[7]
        }

    for i in db.documentary.find(aocumentaryDict):
        return

    db.documentary.save(aocumentaryDict)