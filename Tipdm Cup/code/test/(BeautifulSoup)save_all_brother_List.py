'''
	爬取标签所有的兄弟节点,并以合适的格式保存到列表中
'''
from urllib.request import urlopen, HTTPError, URLError
import json
from bs4 import BeautifulSoup as bs
import re


# 文件夹路径
path = "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\"


# 寻找此标签下所有标签
def Find_class(soup):
	soup = str(soup)
	the_class = re.findall("(?<=class=\").+(?=\")",soup)
	return the_class



url = "https://maijia.bbs.taobao.com/detail.html?spm=a210m.7699124.0.0.NXNfTI&postId=6838418"  # 网页url
req = urlopen(url)
soup = bs(req)
# soup = soup.next_element
# soup = soup.div.next_siblings

for si in soup.div.next_siblings:
	the_class = Find_class(si)
	print(repr(the_class))
	with open(path + "brother_tag.txt", 'a', encoding='gb18030') as file_keep:
		file_keep.write(str(the_class))
'''
for si in soup.div.find_all_next():
    print(soup)
    with open(path + "brother_tag.txt", 'a', encoding='gb18030') as file_keep:
    	file_keep.write(str(soup))
'''