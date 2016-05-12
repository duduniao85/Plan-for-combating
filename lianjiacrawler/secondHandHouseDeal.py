# -*- coding=utf-8 -*-
__author__ = 'xuyuming'
from bs4 import BeautifulSoup
from urllib import urlopen
import pandas as pd
import time
import HTMLParser
import urlparse
import urllib
import urllib2
import cookielib
import string
import re

def unzip(data):
    import gzip
    import StringIO
    data = StringIO.StringIO(data)
    gz = gzip.GzipFile(fileobj=data)
    data = gz.read()
    gz.close()
    return data

def lianjialogin():
    """
    摸拟链家用户登录
    :param username: 登录用户名
    :param password: 登录密码
    :return:
    """
    #获取Cookiejar对象（存在本机的cookie消息）
    cookie = cookielib.CookieJar()
    #自定义opener,并将opener跟CookieJar对象绑定
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    #安装opener,此后调用urlopen()时都会使用安装过的opener对象
    urllib2.install_opener(opener)

    home_url = 'http://sh.lianjia.com/'
    auth_url = 'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fsh.lianjia.com%2F'
    chengjiao_url = 'http://sh.lianjia.com/chengjiao/'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'passport.lianjia.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
    }
    # 获取lianjia_uuid
    req = urllib2.Request('http://sh.lianjia.com/')
    opener.open(req)
    # 初始化表单
    req = urllib2.Request(auth_url, headers=headers)
    result = opener.open(req)
    #print(cookie)
    # 获取cookie和lt值
    pattern = re.compile(r'JSESSIONID=(.*)')
    jsessionid = pattern.findall(result.info().getheader('Set-Cookie').split(';')[0])[0]
    # print jsessionid
    html_content = result.read()
    html_content = unzip(html_content)
    #print html_content.decode('UTF8')
    pattern = re.compile(r'value=\"(LT-.*)\"')
    lt = pattern.findall(html_content)[0]

    pattern = re.compile(r'name="execution" value="(.*)"')
    execution = pattern.findall(html_content)[0]

    # print(cookie)
    # opener.open(lj_uuid_url)
    # print(cookie)
    # opener.open(api_url)
    # print(cookie)

    # data
    data = {
        'username': '18616153298',
        'password': 'Wuxi1107',
        # 'service': 'http://bj.lianjia.com/',
        # 'isajax': 'true',
        # 'remember': 1,
        'execution': execution,
        '_eventId': 'submit',
        'lt': lt,
        'verifyCode': '',
        'redirect': '',
    }
    # urllib进行编码
    post_data=urllib.urlencode(data)
    # header
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'Content-Length': '152',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'passport.lianjia.com',
        'Origin': 'https://passport.lianjia.com',
        'Pragma': 'no-cache',
        'Referer': 'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fsh.lianjia.com%2F',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'X-Requested-With': 'XMLHttpRequest',
    }

    headers2 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'sh.lianjia.com',
        'Pragma': 'no-cache',
        'Referer': 'https://passport.lianjia.com/cas/xd/api?name=passport-lianjia-com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
    }
    req = urllib2.Request(auth_url, post_data, headers)
    try:
        result = opener.open(req)
    except urllib2.HTTPError, e:
        print e.getcode()
        print e.reason
        print e.geturl()
        print "-------------------------"
        print e.info()
        print(e.geturl())
        req = urllib2.Request(e.geturl())
        result = opener.open(req)
        req = urllib2.Request(chengjiao_url)
        result = opener.open(req).read()
    data = unzip(result.read())
    print data
    return unzip(result.read())


def getUrlList(pageUrl):
    """
    传入指定的需要抓取的页面
    返回需要抓取的明细项url列表,以及url列表对应明细项的签约日期
    """
    textdata=urlopen(pageUrl).read()
    soup=BeautifulSoup(textdata,'lxml')
    itemUrlList=soup.select('body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li > div.info-panel > h2 > a')
    #签约日期
    itemDealDate=soup.select('body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li > div.info-panel > div > div.col-2.fr > div > div:nth-of-type(1) > div')
    #ID
    itemIdList=soup.select('body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li > div.info-panel > h2 > a')
    #区县
    itemQuxianList=soup.select('body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li > div.info-panel > div > div.col-1.fl > div.other > div > a:nth-of-type(1)')
    #片区
    itemPianquList=soup.select('body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li > div.info-panel > div > div.col-1.fl > div.other > div > a:nth-of-type(2)')
    #楼层/层高
    itemLoucengList=soup.select('body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li > div.info-panel > div > div.col-1.fl > div.other > div')
    # 面积
    itemMianjiList=soup.select('body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li > div.info-panel > h2 > a')
    # 总价
    itemZongjiaList=soup.select('body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li > div.info-panel > div > div.col-2.fr > div > div.fr > div')
    # 单价
    itemDanjiaList=soup.select('body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li > div.info-panel > div > div.col-2.fr > div > div:nth-of-type(2) > div')
    itemList =[]
    for itemUrl,itemDate,itemId,itemQuxian,itemPianqu,itemLouceng,itemMianji,itemZongjia,itemDanjia in \
            zip(itemUrlList,itemDealDate,itemIdList,itemQuxianList,itemPianquList,itemLoucengList,itemMianjiList,itemZongjiaList,itemDanjiaList):
        temp_strlist=list(itemLouceng.stripped_strings)
        item = {
            'itemurl': itemUrl.get('href'),
            'signdate': itemDate.get_text(),
            'itemid': itemId.get('key'),
            'quxian': itemQuxian.get_text(),
            'pianqu': itemPianqu.get_text(),
            'louceng':temp_strlist[3] if (len(temp_strlist) > 3) else '',#不是所有的房子都包含楼层信息，没有则置空
            'chaoxiang':temp_strlist[5] if (len(temp_strlist) > 5) else '',#不是所有的房子都包含朝向信息，没有则置空
            'mianji': itemMianji.get_text().split(' ')[2].replace(u'平米',''),
            'zongjia': list(itemZongjia.stripped_strings)[0],
            'danjia': list(itemDanjia.stripped_strings)[0],
            'xiaoqu': itemMianji.get_text().split(' ')[0],
            'huxing': itemMianji.get_text().split(' ')[1]
        }
        itemList.append(item)
    return itemList

def getAttr(item_page_url):
    """
    :param item_page_url: 输入明细已经成交房子的网页链接
    :return:返回属性值字典列表
    维度：ID，小区名称，户型，区县， 片区， 楼层，总层高 ，朝向 ，建筑年份， 卖点，是否有钥匙，邻近地铁站，装修情况，地址
    指标：面积，总价，单价，同小区挂牌均价
    """
    textdata=urlopen(item_page_url).read()
    soup=BeautifulSoup(textdata,'lxml')
    #############################################维度#####################################################
    #二手户成交数据ID
    itemId=soup.select('body > div.cj-wrap > div > div.esf-top > div.cj-cun > div.content > div.houseRecord > span.houseNum')[0].get_text().split(u'：')[1]
    # 建筑年份
    jianzhunianfen=soup.findAll('table',class_='aroundInfo')[0].findAll('tr')[1].findAll('td')[3].get_text().strip().replace(u'年建','')
    # 邻近地铁站通过正则表达式提取
    linjindetiezhan=soup.findAll('span',class_='fang-subway-ex')
    linjindetiezhan= linjindetiezhan[0].get_text() if (len(linjindetiezhan) > 0) else ''
    linjindetiezhan,number = re.subn(r'[0-9]+', '', linjindetiezhan,re.S)
    linjindetiezhan=linjindetiezhan.replace(u'距离号线','').replace(u'米','')
    # 装修情况
    zhuangxiuqingkuang=soup.findAll('table',class_='aroundInfo')[0].findAll('tr')[2].findAll('td')[1].get_text().strip()
    item_attr={
            'itemId':itemId,
            'jianzhunianfen':jianzhunianfen,
            'linjinditie':linjindetiezhan,
            'zhuangxiuqingkuang': zhuangxiuqingkuang,
    }
    return item_attr
def unitTest(itemUrl):
    """

    :param itemUrl:
    :return:
    """
    textdata=urlopen(itemUrl).read()
    soup=BeautifulSoup(textdata,'lxml')
    #text=soup.select('body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li > div.info-panel > div > div.col-2.fr > div > div:nth-of-type(2) > div')
    # 建筑年份
    jianzhunianfen=soup.findAll('table',class_='aroundInfo')[0].findAll('tr')[1].findAll('td')[3].get_text().strip().replace(u'年建','')
    # 邻近地铁站通过正则表达式提取
    linjindetiezhan=soup.findAll('span',class_='fang-subway-ex')
    linjindetiezhan= linjindetiezhan[0].get_text() if (len(linjindetiezhan) > 0) else ''
    linjindetiezhan,number = re.subn(r'[0-9]+', '', linjindetiezhan,re.S)
    linjindetiezhan=linjindetiezhan.replace(u'距离号线','').replace(u'米','')
    # 装修情况
    zhuangxiuqingkuang=soup.findAll('table',class_='aroundInfo')[0].findAll('tr')[2].findAll('td')[1].get_text().strip()
    


if __name__ == '__main__':
    #list=getUrlList(r'http://sh.lianjia.com/chengjiao/d20000')
    unitTest(r'http://sh.lianjia.com/chengjiao/sh1226691.html')
    #unitTest(r'http://sh.lianjia.com/chengjiao/')
    #print pd.DataFrame(getUrlList(r'http://sh.lianjia.com/chengjiao/'))['danjia']

