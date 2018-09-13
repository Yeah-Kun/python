'''
	使用bs搜索某节点，再遍历此节点下的内容,此方法不太可行，因为提取seletor路径非常困难
'''
from urllib.request import urlopen, HTTPError, URLError
import json
from bs4 import BeautifulSoup as bs
import re


# 文件夹路径
path = "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\"


url = "https://zhitongche.bbs.taobao.com/detail.html?spm=0.0.0.0.DlATBe&postId=7186061"  # 网页url
req = urlopen(url)
soup = bs(req)
soup = soup.select("body > div.rain-layout.nb-detail > div:nth-of-type(5)")
print(soup)
'''
for si in soup.div.next_siblings:
	the_class = Find_class(si)
	print(repr(the_class))
	with open(path + "brother_tag.txt", 'a', encoding='gb18030') as file_keep:
		file_keep.write(str(the_class))
'''
