'''
	爬取天涯论坛一万个url数据，用于测试
'''
from urllib.request import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup as bs
import re
import os


pages = set()  # 定义一个集合，用于 去重 操作
n = 0
k = 100


# 提取url函数
def getLinks(url, file_path):
    global pages
    global n
    html = urlopen(url)    # input tianya URL
    bs0bj = bs(html)   # BeautifulSoup objectization

    # 
    for link in bs0bj.findAll("a", href=re.compile("http://bbs.tianya.cn/post-\w+-\d+-\d\.shtml")):
        link = str(link)
        substring = "http://bbs.tianya.cn/post-\w+-\d+-\d\.shtml"  # 网址的指定格式
        link = re.search(substring, link)  # 正则表达式提取指定格式的网址
        
        # 去重操作，然后再保存url到文件里
        try:
            if link.group(0) not in pages:
                pages.add(link.group(0))
                print(link.group(0))
                file_keep = open(file_path, "a")
                file_keep.writelines(link.group(0))
                file_keep.writelines("\r")
                file_keep.close()
                if len(pages) >= 10000:
                    break
                # 递归算法，重复调用函数
                getLinks(link.group(0), path)

        # 异常处理
        except (HTTPError, ConnectionResetError, URLError, IndexError) as reason:
            print(reason)
            continue


# 自定义保存路径
path =  "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\tianya_10000_url.txt"
getLinks("http://bbs.tianya.cn/", path)  # 天涯的网址:http://bbs.tianya.cn/
