#coding=utf-8
import requests
from pyquery import PyQuery as Pq
import re

class BaiduSearchSpider(object):
    def __init__(self,searchText,number):
        self.url = "http://www.baidu.com/baidu?wd=%s" % searchText
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17"}
        self._page = None
        self.pagenumber = number
    def page(self,url):
        if not self._page:
            r = requests.get(url, headers=self.headers)
            r.encoding = 'utf-8'
            self._page = Pq(r.text)
        return self._page
    
    def baiduURLs(self):
        li = []
        for i in range(int(self.pagenumber)):
            temp = []
            url = self.url + '&pn=' + str(i*10)
            a= self.page(url)
            a = str(a)         
            temp = temp + re.findall('href="http://www.baidu.com/link\S*"',a)

            temp = list(set(temp))
            li = li + temp
            print '第%s页所有url已经收集完毕' % i
        return li 

    def write_to_file(self,alist):
        f = open('original.txt','w')
        for i in alist:
            f.write(i[6:-1])
            f.write('\n')
        f.close()

##a = BaiduSearchSpider('inurl:php id',1)
##lis = a.baiduURLs()
##for i in lis:
##    print i

