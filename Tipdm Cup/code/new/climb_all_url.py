'''
    爬取泰迪杯官方给的所有url数据，爬取源代码，保存到all_url_data.pkl文件，错误收集并保存到all_url_error.txt文件
'''
from urllib.request import urlopen, HTTPError, URLError
import os
import pickle
from chardet.universaldetector import UniversalDetector
import re
import socket
from bs4 import BeautifulSoup as bs

# 编码格式识别
# 现在此函数已经失去作用，因为针对中文可以直接使用最强大的gb18030格式编码，它囊括所有中文编码格式
def Detection_coding_format(html):
    detector = UniversalDetector()
    for line in html.readlines():
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result['encoding']


# 获得官方给的所有url数据
all_url_file = open(
    "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url.pkl", "rb")
url = pickle.load(all_url_file)  # 提取url数据
all_url_file.close()  # 提取完之后，关闭文件，否则会引起错误

n = 0   # 计时器，用于提取过程的提取和显示
k = 0
# 提取网站源代码主程序
for each_url in url:
    try:
        req = urlopen(each_url,timeout=2)  # 提取单个网站源代码
        bs0bj = bs(req)   # BeautifulSoup处理
        bs0bj = str(bs0bj) # 将其字符串化，易于保存
        if re.findall("发表于",bs0bj) != None:
            k = k+1
#        with open("D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url_data.txt", "a", encoding='gb18030') as pickle_file:
 #       	pickle_file.write(bs0bj)
        n += 1
        print(n)
        print(k)
    except (HTTPError, ConnectionResetError, URLError,socket.timeout) as reason:    # 异常处理
        error_file = open(
            "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url_error_new.txt", "a")
        n += 1
        reason = str(n) + '.' + str(reason) + '\r'
        error_file.writelines(reason)
        error_file.close()
        print(reason)
        continue

print(k)