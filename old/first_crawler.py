import http.client

conn = http.client.HTTPConnection("WWW.cnblogs.com")  #主机地址
conn.request("GET","/vamei")      #请求方法和资源路径
response = conn.getresponse()     #获得回复

print(response.status,response.reason) #回复的状态码、状态描述
content = response.read()			   #回复的主题内容


import re


pattren = "posted @ (\d{4}-[0-1]\d-[0-9]\d [0-2]\d:[0-6]\d Vamei 阅读 \((\d+)\)) 评论"
for line in content:
	m = re.search(pattren,line)
	if m != None:
		print(m.group(0))
