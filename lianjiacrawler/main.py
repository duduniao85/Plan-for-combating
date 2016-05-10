#coding=utf-8
__author__ = 'xuyuming'
import secondHandHouseDeal
i=1
itemUrlList=set()
itemList=[]
while(True):
    prefix=r'http://sh.lianjia.com'
    url=r'http://sh.lianjia.com/chengjiao/d'+str(i)
    scndHs4Sale=secondHandHouseDeal.getUrlList(url)
    if len(scndHs4Sale)== 0 :
        break
    #print scndHs4Sale
    for item in scndHs4Sale:
        itemUrl=prefix+item
        itemUrlList.add(itemUrl)
    i+=1
for itemUrl in itemUrlList:
    itemList.append(secondHandHouseDeal.getAttr(itemUrl))
