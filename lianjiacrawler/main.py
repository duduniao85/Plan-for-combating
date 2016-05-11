#coding=utf-8
__author__ = 'xuyuming'
import secondHandHouseDeal
import time
import pandas as pd
i=1
itemUrlList=set()#房源URL集合
itemBaseList=[]#房源基础信息LIST，包括ID,URL,签约日期，所属板块
itemList=[]#成交详情列表
#先模拟登录
#secondHandHouseDeal.lianjialogin()
#取得需要爬取的ID列表和明细url列表
while(i<=2):
    prefix=r'http://sh.lianjia.com'
    url=r'http://sh.lianjia.com/chengjiao/d'+str(i)
    scndHs4Sale=secondHandHouseDeal.getUrlList(url)
    itemBaseList.extend(scndHs4Sale)
    if len(scndHs4Sale)== 0 :
        break
    print scndHs4Sale
    for item in scndHs4Sale:
        #print item.get('itemId')
        itemUrl=prefix+item.get('itemUrl')
        itemUrlList.add(itemUrl)
    i+=1
print itemBaseList
starttime= time.clock()
for itemUrl in itemUrlList:
    item= secondHandHouseDeal.getAttr(itemUrl)#t签约户源详情
    #print item
    itemList.append(secondHandHouseDeal.getAttr(itemUrl))
data=pd.DataFrame(itemList)
endtime=time.clock()
print endtime-starttime
print data