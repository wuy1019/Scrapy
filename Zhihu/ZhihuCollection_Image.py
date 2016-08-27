#!/usr/bin/env python
# -*-coding: utf-8-*-
__author__ = 'wuy'

from urllib2 import urlopen
import requests
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
    "Accept": "*/*",
    "Accept-Encoding": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
}

def retry(url):
    u"""
    如果访问失败，重试
    :return:如果成功，返回结果，如果失败，继续试
    """
    rertyTime = 10
    while rertyTime > 0:
        try:
            return requests.get(url, headers=headers,timeout=5)
        except:
            rertyTime -= 1
            print u"还有{}次重试机会".format(rertyTime)


def parse_html(url):
    u"""
    解析答案html，获取用户id和回答下的所有图片地址
    如果是匿名用户，则采用匿名计数的方式，如：
    匿名1，匿名2
    :param url: 答案链接
    :return:知乎用户id，图片地址
    """
    img_lis = []
    author  = ""
    try:
        r = retry(url)
        soup = BeautifulSoup(r.text, "html.parser")
        ans = soup.find_all("div", attrs={"id": "zh-question-answer-wrap"})[0]
        try:
            author = ans.find_all(attrs={"class": "author-link"})[0].text
        except:
            author = u"匿名用户"
        main = ans.find_all("div", attrs={"class": "zm-editable-content clearfix"})[0]
        imgs = main.find_all("img", attrs={"class": "origin_image zh-lightbox-thumb"})

        if imgs:
            for img in imgs:
                img_lis.append(img.get("data-original"))
        return author, img_lis
    except:
        print u"==访问问题失败：%s=="%url


def download_Image(url, maxPage=1, sleep=2, timeout=5):
    u"""

    解析收藏夹html并依次获得收藏夹下所有问题url，并解析和下载回答下图片
    :param collect_url: 收藏夹链接
    :param maxPage: 反问最大页数
    :param sleep: 控制反问速度
    :param timeout:
    :return:
    """
    root_url = "https://www.zhihu.com"
    user_dic = {}  # 对访问过的用户计数
    for page in range(1, maxPage+1):
        collect_url = url + "?page=" + str(page)
        time.sleep(sleep)
        print u"==正在抓取第%s页=="%page
        try:
            r = retry(collect_url)

            #r = requests.get(collect_url, headers=headers, timeout=timeout)
            soup = BeautifulSoup(r.text, "html.parser")
            answers = soup.find_all("div", attrs={"class": "zm-item-rich-text expandable js-collapse-body"})
            if answers:
                for answer in answers:
                    time.sleep(sleep)
                    ansurl = "/".join([root_url, answer.get("data-entry-url")])
                    try:
                        use, ans = parse_html(ansurl)
                        if not ans:
                            continue
                        if use in user_dic:
                            user_dic[use] += 1
                        else:
                            user_dic[use] = 1
                        for pic in ans:
                            image = urlopen(pic).read()
                            with open("Pic/%s_%s.jpg" % (use,user_dic[use] ), "wb") as file:
                                file.write(image)

                            user_dic[use] += 1


                    except:
                        print
        except:
            print u"=========访问收藏夹失败：页数：%s========="%page




download_Image("https://www.zhihu.com/collection/19799242", maxPage=20)