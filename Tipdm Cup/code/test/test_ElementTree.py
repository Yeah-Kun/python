from lxml import etree
from bs4 import BeautifulSoup as bs
import re
from urllib.request import urlopen


# print(bs0bj)
# 目标文件夹路径
path = "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\"

# 由于'r'遇到错误，用'rb'就可以成功读取，原因之后再找
file_keep = open(path + "one_url_data.txt", 'rb')
bs0bj = file_keep.read().decode('gb18030')  # 进行编码读取
file_keep.close()

# 获取解析树
#tree = etree.ElementTree(file="D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\one_url_data.txt") # 建立一颗元素树 对象
#tree = etree.parse("D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\one_url_data.html") # 对文件进行解析，跟上述方法效果一致
# root = tree.getroot() # 获取根节点
# result = etree.tostring(tree,pretty_print=True) # 打印该文档下的内容
#result = tree.xpath('/html')
# print(result)
List_children_tag = [] 
List_children_tag2 = [] 
tree = etree.HTML(bs0bj)  # 用HTML方法解析文件
root = tree.xpath('/html//*') # 找到这个绝对路径下的文本内容
#children = tree[1][7]# 可以把它的子节点赋给children,类型是_Element类型/html/body/div[5]/div[5]
tag_path ="/html/body/div[5]/"
children = tree.xpath(tag_path+'div[5]//*')
#children2 = tree.xpath(tag_path+'div[9]//*')
print(children)
'''
print(children)
for children_tag in children:
	List_children_tag.append(children_tag.tag)
for children_tag in children2:
	List_children_tag2.append(children_tag.tag)
#print(children)
#for child in children:
#	print(child.tag) # tag可以获得标签
#child = children.xpath("./child::*") 
#print(child)
#print(type(children)) 
#print(type(tree[1].tag))
#print(type(tree))
#print(root)

List_tag = []
def Traverse(tree,flag):
	for child in tree:
		List_tag.append(child.tag)
		if len(List_tag) >= flag:
			break

def List_Count_Tag(children):
	List_tag = []
	if 'a' in children:
		List_tag.append(children.count('a'))
	else:
		List_tag.append(0)
	if 'div' in children:
		List_tag.append(children.count('div'))
	else:
		List_tag.append(0)
	if 'p' in children:
		List_tag.append(children.count('p'))
	else:
		List_tag.append(0)
	if 'span' in children:
		List_tag.append(children.count('span'))
	else:
		List_tag.append(0)
	if 'td' in children:
		List_tag.append(children.count('td'))
	else:
		List_tag.append(0)
	return List_tag

print(List_Count_Tag(List_children_tag))
print(List_Count_Tag(List_children_tag2))
'''