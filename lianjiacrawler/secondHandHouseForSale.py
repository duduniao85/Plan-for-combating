#coding=utf-8
__author__ = 'xuyuming'
from bs4 import BeautifulSoup
def getUrlList(pageUrl):
    """
    传入指定的需要抓取的页面
    返回需要抓取的明细项url列表,
    这里二手房的地铁信息比较特殊只在概述页面看到得，明细页面不展示地铁信息，故需要返回URL_LIST时还需要将URL与最近的地铁站作为字典拼接起来
    如果不近地铁，则默认赋值为“不近地铁"
    """

    item_url_list=[]
    return item_url_list

def getAttr(item_page_url):
    """ 本函数主要用于根据指定的明细页面提取完整的属性列表
    :param item_page_url: 输入明细房子的网页链接
    :return:返回属性值字典列表用于后续合并
    """
    item_attr_list=[]
    return item_attr_list



