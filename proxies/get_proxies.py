#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = "wuy1019@live.com"

import requests
from bs4 import BeautifulSoup
import re
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def get_proxies(pageNum):
    "url = http://www.xicidaili.com/nn"
    ips = []
    url = "http://www.xicidaili.com/nt/" + str(pageNum)
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.text, "html.parser")

    for pox in soup.find_all("tr")[1:]:
        ip = pox.contents[3].text
        port = pox.contents[5].text

        ips.append(":".join([ip, port]))
    return ips

def check_proxies(Num):
    "find n good ips"


    for page in range(1,100):
        ips = get_proxies(page)
        n = Num
        while n > 0:
            for ip in ips:
                proxies = {"http": ip}
                try:
                   # r = requests.get("http://1212.ip138.com/ic.asp", proxies=proxies, timeout=3)
                    r = requests.get("http://www.dianping.com/", proxies=proxies, timeout=3)
                    if r:
                       ## soup = BeautifulSoup(r.text, "html.parser")
                        #tmp = re.search("(\d+\.\d+\.\d+\.\d+)", soup.body.text).group(1)
                        #if tmp and tmp == ip.split(":")[0]:
                            #print tmp
                            print "good:", ip
                            n -= 1
                        #else:
                         #   print "bad:", ip
                    #else:
                        #print "bad:", ip
                except:
                    pass
                    #print "bad:", ip

check_proxies(10)

