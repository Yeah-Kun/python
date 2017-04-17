from lxml import etree
from bs4 import BeautifulSoup as bs
import re
from urllib.request import urlopen


# print(bs0bj)
# 目标文件夹路径
path = "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\"

# 由于'r'遇到错误，用'rb'就可以成功读取，原因之后再找
file_keep = open(path + "one_url_data.html", 'rb')
bs0bj = file_keep.read().decode('gb18030')  # 进行编码读取
file_keep.close()

# 获取解析树
# tree = etree.ElementTree(file="D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\one_url_data.txt") # 建立一颗元素树 对象
# tree = etree.parse("D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\one_url_data.html") # 对文件进行解析，跟上述方法效果一致
# root = tree.getroot() # 获取根节点
# result = etree.tostring(tree,pretty_print=True) # 打印该文档下的内容
#result = tree.xpath('/html')
# print(result)
tree = etree.HTML(bs0bj)  # 用HTML方法解析文件
root = tree.getchildren()
root = tree.xpath('/html/body') # 找到这个绝对路径下的文本内容
print(type(root))
