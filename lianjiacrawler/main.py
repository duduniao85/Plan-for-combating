#coding=utf-8
__author__ = 'xuyuming'
import secondHandHouseDeal
import time
import pandas as pd
i=1
itemUrlList=set()
itemList=[]
#先模拟登录
secondHandHouseDeal.lianjialogin()
while(i<2):
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

starttime= time.clock()
for itemUrl in itemUrlList:
    item= secondHandHouseDeal.getAttr(itemUrl)
    #print item
    itemList.append(secondHandHouseDeal.getAttr(itemUrl))
data=pd.DataFrame(itemList)
endtime=time.clock()
print endtime-starttime
print data