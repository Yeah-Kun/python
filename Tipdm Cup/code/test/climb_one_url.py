'''
	用于测试单个网站的爬取效果
    爬取单个网页的源代码，保存到one_url_data.txt文件
'''
from urllib.request import urlopen, HTTPError, URLError
import json
from bs4 import BeautifulSoup as bs
import re


url = "http://hongdou.gxnews.com.cn/viewthread-15274301.html"  # 网页url
req = urlopen(url)
bs0bj = req.read().decode('gb18030')
bs0bj = str(bs0bj)
with open("D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\one_url_data.html", "w",encoding='gb18030') as file_obj:
    file_obj.write(bs0bj)
