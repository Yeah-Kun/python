from urllib.request import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup as bs   # Extract content
import re


url = "http://bbs.rednet.cn/thread-46761095-1-1.html"
req = urlopen(url)
bs0bj = bs(req,from_encoding='utf-8')
file_keep = open(
    "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\one_url_data.txt", "w", encoding="gb18030")
file_keep.write(str(bs0bj))
file_keep.close()
