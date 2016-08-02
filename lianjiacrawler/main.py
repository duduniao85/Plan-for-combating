#coding=utf-8
__author__ = 'xuyuming'
import secondHandHouseDeal
import time
import pandas as pd
from sqlalchemy import *
from sqlalchemy.dialects.oracle import \
            BFILE, BLOB, CHAR, CLOB, DATE, \
            DOUBLE_PRECISION, FLOAT, INTERVAL, LONG, NCLOB, \
            NUMBER, NVARCHAR, NVARCHAR2, RAW, TIMESTAMP, VARCHAR, \
            VARCHAR2  #引入ORACLE专用字符集
from sqlalchemy.sql import select
from sqlalchemy.sql import text #用于导入自定义文本SQL
from sqlalchemy.schema import *
i=1
itemUrlList=set()#房源URL集合
itemBaseList=[]#房源基础信息LIST，包括ID,URL,签约日期，所属板块
itemList=[]#成交详情列表
#先模拟登录
#secondHandHouseDeal.lianjialogin()
#取得需要爬取的ID列表和明细url列表
#50页提交一次

from selenium import webdriver
driver=webdriver.Chrome()
driver.get("https://passport.lianjia.com/cas/login?service=http://user.sh.lianjia.com/index/ershou")
#xueqiu login
driver.find_element_by_name("username").clear()
driver.find_element_by_name("username").send_keys("18616153298")
driver.find_element_by_name("password").clear()
driver.find_element_by_name("password").send_keys("Wuxi1107")
driver.find_element_by_xpath("//*[@id='loginUserForm']/ul/li[5]/button").submit()
time.sleep(1)
cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
print cookie
starttime= time.clock()
db_engine=create_engine('oracle+cx_oracle://quant:1@127.0.0.1:1521/XE?charset=utf8', echo=True)
conn=db_engine.connect()
i=1
cookiestr = ';'.join(item for item in cookie)
headers = {'cookie':cookiestr}
while(i<=2800):
    prefix=r'http://sh.lianjia.com'
    url=r'http://sh.lianjia.com/chengjiao/d'+str(i)
    scndHs4Sale=secondHandHouseDeal.getUrlList(headers,url)

    itemBaseList.extend(scndHs4Sale)
    if len(scndHs4Sale)== 0 :#
        break
    if i%50 == 0:#50页提交一次，以便支持断点续传
        dfChengjiao=pd.DataFrame(itemBaseList)
        dfChengjiao.to_sql('dealbasics_lianjia',db_engine,if_exists='append',dtype={'chaoxiang': VARCHAR2(6), 'itemid':VARCHAR2(24), 'itemurl':VARCHAR2(48),\
                                                               'louceng':VARCHAR2(64),'pianqu':VARCHAR2(64),'danjia':VARCHAR2(16),'mianji':VARCHAR2(16),\
                                                               'signdate':VARCHAR2(64),'zongjia':VARCHAR2(64),'quxian':VARCHAR2(64),'xiaoqu':VARCHAR2(64),\
                                                                             'huxing':VARCHAR2(64)})
        itemBaseList=[]
        time.sleep(1)
    for item in scndHs4Sale:
        #print item.get('itemId')
        itemUrl=prefix+item.get('itemurl')
        itemUrlList.add(itemUrl)
    i+=1

dfChengjiao.to_csv(r'd:\temp\chengjiao.csv',encoding='gb2312',index=False)
conn.close()
endtime=time.clock()
print u'总耗时'+str(endtime-starttime)+u'秒'
print 'done!'
#
#
# ###################################获取除基础信息之外的小区信息附加信息,通过多进程解决#########################################
# starttime= time.clock()
# for itemUrl in itemUrlList:
#     item= secondHandHouseDeal.getAttr(itemUrl)#t签约户源详情
#     #print item
#     itemList.append(secondHandHouseDeal.getAttr(itemUrl))
# data=pd.DataFrame(itemList)
# endtime=time.clock()
# print endtime-starttime
# print data
driver.quit()
