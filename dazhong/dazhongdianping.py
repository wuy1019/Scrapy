#!/usr/bin/env python
# -*-coding: utf-8-*-
__author__ = 'wuy'

import requests
from bs4 import BeautifulSoup
from urllib2 import urlopen
import time


headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Cookie": "JSESSIONID=8E15B9BEBAC8782FD4F51C5105F11207; cy=5; cye=nanjing; _hc.v=71a83cb6-755b-55bb-71e7-d2c3cef55949.1471437629; __utma=1.849064984.1471437629.1471437629.1471437629.1; __utmb=1.3.10.1471437629; __utmc=1; __utmz=1.1471437629.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; PHOENIX_ID=0a017918-156988528fe-def77; s_ViewType=10; aburl=1",
}
proxies = {"http":"http://113.3.78.124:8118"}

def get_pic(raw_url):
    url = "http://www.dianping.com" + raw_url
    r = requests.get(url, headers = headers, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.find_all(id="aDetail")[0].contents[1].get("src")

def paser(pageNum):

    url = "http://www.dianping.com/shop/32675893/photos/tag-%E8%8F%9C?pg=" + str(pageNum)
    r = requests.get(url, headers = headers, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    infos = soup.find_all("li",attrs={"class":"J_list"})
    lis = []
    for info in infos:
        picUrl = get_pic(info.a.get("href"))
        pic_infos = info.find_all(attrs={"class": "picture-info"})[0]
        mem = pic_infos.find_all(attrs={"class": "info"})[0].a.text
        name = pic_infos.find_all(attrs={"class":"name"})[0].a.text
        lis.append((picUrl, mem, name))
    return lis

def downPic():

    post = {} #mem: n
    unde = 0
    for page in range(1,350):
        time.sleep(2)
        print u"===正在下载第%s页==="% page
        try:
            for pic in paser(page):
                unde += 1
                url = pic[0]
                mem = pic[1]
                name = pic[2]
                if mem in post:
                    post[mem]  += 1
                else:
                    post[mem] = 1
                if name:
                    filename = name + "_" + mem + "_" + str(post[mem])
                else:
                    filename = mem + "_" + str(post[mem])
                try:
                    with open("diaping/" + filename + ".jpg", "wb") as file:
                        file.write(urlopen(url).read())
                except:
                    with open("diaping/" + str(unde) + ".jpg", "wb") as file:
                        file.write(urlopen(url).read())
        except:
            print u"被封锁"
            break

downPic()



