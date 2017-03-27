from urllib.request import urlopen,HTTPError,URLError
from bs4 import BeautifulSoup as bs
import re
import os

# tianya URL:http://bbs.tianya.cn/
pages = set()
n = 0
k = 100
def getLinks(url):
	global pages
	global n
	html = urlopen(url)    # input tianya URL
	bs0bj = bs(html)   # BeautifulSoup objectization

	for link in bs0bj.findAll("a",href= re.compile("http://bbs.tianya.cn/post-\w+-\d+-\d\.shtml")):
		link = str(link)
		substring = "http://bbs.tianya.cn/post-\w+-\d+-\d\.shtml"  # Substring format
		link = re.search(substring,link) # search the substring   
		try:
			if link.group(0) not in pages:   
				pages.add(link.group(0))
				print(link.group(0))
				file_keep = open("D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\tianya_10000_url.txt", "a")
				file_keep.writelines(link.group(0))
				file_keep.writelines("\r")
				file_keep.close()
				if len(pages) >= 10000:
					break
				getLinks(link.group(0))

		except (HTTPError,ConnectionResetError,URLError,IndexError) as reason:
			print(reason)
			continue


getLinks("http://bbs.tianya.cn/")