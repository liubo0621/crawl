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
def addUrl(url, websiteId, depth, description = '', status = Constance.TODO):
    for i in db.urls.find({'url':url}):
        return

    urlDict = {'url':url, 'website_id':websiteId, 'depth':depth, 'description':description, 'status':status}
    db.urls.save(urlDict)

def updateUrl(url, status):
    db.urls.update({'url':url}, {'$set':{'status':status}}, multi=True)

def addDocumentary(websiteId, docName, abstract, url, episodeNum = '', playNum = '', totalLength = '', releaseTime = '', institutions = '', cyclopediaMsg = ''):
    '''
    @summary: 添加纪录片
    ---------
    @param websiteId: 网站id
    @param docName: 片名
    @param abstract: 简介
    @param url: 纪录片url
    @param episodeNum: 集数
    @param playNum: 播放次数
    @param totalLength: 时长
    @param releaseTime: 发布时间
    @param institutions: 播出机构
    @param cyclopediaMsg: 百科信息
    ---------
    @result:
    '''
    aocumentaryDict = {
        'website_id':websiteId,
        'doc_name':docName,
        'abstract':abstract,
        'url':url,
        'episode_num':episodeNum,
        'play_num':playNum,
        'total_length':totalLength,
        'release_time':releaseTime,
        'institutions':institutions,
        'cyclopedia_msg':cyclopediaMsg
        }

    # 查找数据库，根据url和websiteid看是否有相同的纪录片，若有，则比较纪录片信息，将信息更全的纪录片更新到数据库中
    for doc in db.documentary.find({'website_id':websiteId, 'url':url}, {'_id':0}):
        isDiffent = False
        warning = '\n' + '-' * 50 + '\n'
        for key, value in doc.items():
            if len(str(doc[key])) < len(str(aocumentaryDict[key])):
                isDiffent = True
                warning = warning + '更新 old %s: %s\n     new %s: %s\n'%(key, doc[key], key, aocumentaryDict[key])
                doc[key] = aocumentaryDict[key]

            else:
                warning = warning + '留守 old %s: %s\n     new %s: %s\n'%(key, doc[key], key, aocumentaryDict[key])

        if isDiffent:
            warning = '已存在：\n' + warning + '-' * 50
            log.warning(warning)

            db.documentary.update({'website_id':websiteId, 'url':url}, {'$set':doc})
        else:
            log.warning('已存在url:  ' + url)
        return

    db.documentary.save(aocumentaryDict)

def addDocumentaryList(websiteId, inforList):
    addDocumentary(websiteId, inforList[0], inforList[2], inforList[8], inforList[1], inforList[3], inforList[4], inforList[5], inforList[6], inforList[7])

# addDocumentary('580981f95344650b3c285522', "勿忘国耻！吾辈当自强！！", "abstract", "http://v.youku.com/v_show/id_XMTc2Nzc2OTEwNA==.html")