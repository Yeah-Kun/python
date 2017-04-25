'''
	用爬取单个网站的url：本url及下一页url
'''
from urllib.request import urlopen, Request, HTTPError, URLError
import json
from bs4 import BeautifulSoup as bs
import re
from TDcup import tree_algorithm, the_module
from lxml import etree


# 模仿用户登录
data = {"user": "YeahKun", "password": "pass"}
headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
           "Accept-Encoding": "gzip",
           "Accept-Language": "zh-CN,zh;q=0.8",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
           }

url = "http://bbs1.people.com.cn/post/129/1/2/159586300.html"  # 网页url
req = Request(url)
req.add_header(headers)
respond = urlopen(req)
