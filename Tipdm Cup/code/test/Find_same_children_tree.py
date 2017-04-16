'''
	爬取标签下面所有子节点,并保存到一个列表中
'''
from urllib.request import urlopen, HTTPError, URLError
import json
from bs4 import BeautifulSoup as bs
import re


# 文件夹路径
path = "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\"


# 寻找此标签下所有标签
def Find_tag(soup):
    all_tag = re.findall("<\w+", soup)
    return all_tag

url = "https://maijia.bbs.taobao.com/detail.html?spm=a210m.7699124.0.0.NXNfTI&postId=6838418"  # 网页url
req = urlopen(url)
soup = bs(req)
soup = soup.div.next_sibling # 这里需要给出节点信息
soup = str(soup)
print(repr(soup))
all_tag = Find_tag(soup)
all_tag = str(all_tag)
print(all_tag)

with open(path + "all_tag.txt", 'w', encoding='gb18030') as file_keep:
    file_keep.write(all_tag)
