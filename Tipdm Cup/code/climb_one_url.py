from urllib.request import urlopen, HTTPError, URLError
import json
from bs4 import BeautifulSoup as bs
import re


url = "http://bbs.pcauto.com.cn/topic-11421426.html"
req = urlopen(url)
req = urlopen(url)
bs0bj = bs(req)
bs0bj = str(bs0bj)
with open("D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\one_url_data.txt", "w",encoding='gb18030') as file_obj:
    file_obj.write(bs0bj)
