'''
	用于测试单个网站的爬取效果
'''
from urllib.request import urlopen, HTTPError, URLError
import json
from bs4 import BeautifulSoup as bs
import re
from TDcup import tree_algorithm, the_module
from lxml import etree

url = "http://hongdou.gxnews.com.cn/viewthread-15258185.html"  # 网页url
req = urlopen(url)
bs0bj = bs(req)
bs0bj = str(bs0bj) 
tree = etree.HTML(bs0bj) # 解析树
t = tree.getroottree()  # 构造元素树对象

# 提取主题帖信息
title = the_module.FindTitle(bs0bj,tree)
author = the_module.FindAuthor(bs0bj,tree)
date  = the_module.FindDate(bs0bj)
content  = the_module.FindMain(bs0bj)
dict_all = dict(author, **title, **content, **date) # 将多个字典合在一起
dict_all = str(dict_all)
main_data = {'post':dict_all}

# 回帖预处理
standard_value = the_module.StandardValue(bs0bj) 
tag_path = tree_algorithm.TreeAlgotithm(bs0bj,standard_value) # 获取楼层绝对路径容器


return_data = []
# 提取回帖信息
if tag_path != None:
	for one_path in tag_path: # 解析绝对路径容器，获得单个楼层的绝对路径

		date = the_module.FindFloorDate(tree,one_path) # 时间提取
		author = the_module.FindUserName(tree,one_path) # 用户名提取
		content = the_module.FindFloorContent(tree,one_path) # 回帖内容提取
		dict_one_all = dict(author, **content, **date) # 字典包装
		return_data.append(dict_one_all)
else:
	pass

reply = {'replys':return_data}
print(standard_value)
print(main_data,reply)