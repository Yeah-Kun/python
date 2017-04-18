from lxml import etree
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

# 目标文件夹路径
path = "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\"


# 读取文件源代码
file_keep = open(path + "one_url_data.txt", 'rb') # 由于'r'遇到错误，用'rb'就可以成功读取，原因之后再找
bs0bj = file_keep.read() # 进行编码读取
file_keep.close()


# 算法
tree = etree.HTML(bs0bj) # 用HTML方法解析文件
t = tree.getroottree() # 获得一个节点对应的树
body = t.xpath("./body")
body1 = tree[0][13]
print(t.getpath(body1))
print(type(t.getpath(body1)))
print(type(body1))
print(type(body))
print(type(tree))
print(body)
print(t)
