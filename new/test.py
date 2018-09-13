import requests
newurl = "http://course.wyu.cn/xsyzc/eoexam/main.asp"
r = requests.get(newurl)
r.encoding = "utf8"
print(r.headers)