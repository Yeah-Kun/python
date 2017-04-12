'''
	保存一个网址的源代码
'''
from urllib.request import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup as bs   # Extract content
import re

# 网址
url = "http://bbs.rednet.cn/thread-46761095-1-1.html"
req = urlopen(url)
bs0bj = bs(req)

# 打开文件，保存网址源代码，关闭文件
path = "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\"
file_keep = open(
    path + "one_url_data.txt", "w", encoding="gb18030")
file_keep.write(str(bs0bj))
file_keep.close()
