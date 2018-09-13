'''
	2017年6月1日15:15:15
	读取代理IP网站的API，并获得代理IP
	1. 访问西祠代理的API接口
	2. 获得数据，并用正则表达式提取关键内容
	3. 用列表保存关键内容
'''
from requests import ProxyError
import re


all_url = [] # 存储IP地址的容器

# 代理IP的网址
url = "http://api.xicidaili.com/free2016.txt"
r = requests.get(url=url)
all_url = re.findall("\d+\.\d+\.\d+\.\d+\:\d+",r.text)

with open("D:\\code\\python\\new\\Brush ticket\\IP.txt",'w') as f:
	for i in all_url:
		f.write(i)
		f.write('\n')

for i in all_url:
	print(i)