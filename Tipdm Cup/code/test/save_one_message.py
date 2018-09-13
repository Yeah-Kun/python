'''
	保存一个网址的源代码
'''
from urllib.request import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup as bs   # Extract content
import re

# 网址
url = "https://maijia.bbs.taobao.com/detail.html?spm=a210m.7699124.0.0.NXNfTI&postId=6838418"
req = urlopen(url)
bs0bj = bs(req,"xml")

# 打开文件，保存网址源代码，关闭文件
path = "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\"
file_keep = open(
    path + "one_url_data.txt", "w", encoding="gb18030")
file_keep.write(str(bs0bj))
file_keep.close()
