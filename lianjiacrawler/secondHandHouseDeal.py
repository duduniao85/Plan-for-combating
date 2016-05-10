#coding=utf-8
__author__ = 'xuyuming'
from bs4 import BeautifulSoup
from urllib import urlopen
import time
def getUrlList(pageUrl):
    """
    传入指定的需要抓取的页面
    返回需要抓取的明细项url列表
    """
    textdata=urlopen(pageUrl).read()
    soup=BeautifulSoup(textdata,'lxml')
    searchlist=soup.select('body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li > div.info-panel > h2 > a')
    itemList=[]
    for item in searchlist:
        itemList.append(item.get('href'))
    return itemList

def getAttr(item_page_url):
    """
    :param item_page_url: 输入明细房子的网页链接
    :return:返回属性值字典列表
    维度：ID，小区名称，户型，区县， 片区， 楼层，总层高 ，朝向 ，建筑年份， 卖点，是否有钥匙，邻近地铁站，装修情况，地址
    指标：面积，总价，单价，看房人数，同小区挂牌均价
    """
    item_attr_list=[]
    return item_attr_list

# if __name__ == '__main__':
#     list=getUrlList(r'http://sh.lianjia.com/chengjiao/d20000')
#     print len(list)

