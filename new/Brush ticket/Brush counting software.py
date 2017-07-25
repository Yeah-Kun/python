'''
    2017年6月1日22:53:56
    “我行我素”竞赛刷票插件
    主要是用于给自己队伍刷票用的
'''
import requests
import json
import time
import re

# 请求头信息
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'zh-CN',
    'Connection': 'keep-alive',
    'Content-Length': '16',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'www.dingnf.com',
    'Origin': 'http://www.dingnf.com',
    'Referer': 'http://www.dingnf.com/active/wxws_s',
    'User-Agent': 'Mozilla/4.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# post表单网址
url = "http://www.dingnf.com/active/wxws_t"
params = {'ids': ['22', '22', '22']}


def WriteIPadress():
    all_url = []  # 存储IP地址的容器
    # 代理IP的网址
    url = "http://api.xicidaili.com/free2016.txt"
    r = requests.get(url=url)
    all_url = re.findall("\d+\.\d+\.\d+\.\d+\:\d+", r.text)
    with open("D:\\code\\python\\new\\Brush ticket\\IP.txt", 'w') as f:
        for i in all_url:
            f.write(i)
            f.write('\n')
    return all_url

# 计数器
count = 0
while count < 4000:
    all_url = WriteIPadress()
    for i in all_url:
        proxies = {"http": i}
        try:
            r = requests.post(url=url, data=params,
                              headers=headers, proxies=proxies, timeout=10)
            if(r.json()['flag'] == True):
                count += 1
                print("成功投票%d次！" % (count))
            print(r.json())
        except Exception as reason:
            print("错误原因是：", reason)
