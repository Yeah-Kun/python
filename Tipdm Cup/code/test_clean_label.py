'''
	保存一个网址的源代码,删除标签后，再保存成 纯文本
'''
from urllib.request import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup as bs   # Extract content
import re


# 文件夹路径
path = "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\"


# 直接在这个地方输入网址，就能得到清洗之后的数据
url = "http://bbs.tianya.cn/post-funinfo-7422008-1.shtml"
req = urlopen(url)
bs0bj = bs(req)


# 保存网址的源代码
file_keep = open(
    path + "one_url_data.html", "w", encoding="gb18030")
file_keep.write(str(bs0bj))
file_keep.close()


# 读取经过源代码
with open(path + "one_url_data.html", "r", encoding="gb18030") as file_keep:
    bs0bj = file_keep.read()

bs0bj = re.sub("[^\u4e00-\u9fa5，。！:；、\-？0-9\r\n]", "", bs0bj)
bs0bj = re.sub("[\n{+}]", "\n", bs0bj)

# 保存经过清洗的文本数据
with open(path + "clean_url_data.txt", "w", encoding="gb18030") as file_keep:
    file_keep.write(bs0bj)
