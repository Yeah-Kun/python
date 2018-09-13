'''
    保存所有url的标题
'''
from urllib.request import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup as bs   # Extract content
import pickle    # save file
import json
import copy
from socket import timeout
from lxml import etree
from chardet.universaldetector import UniversalDetector
import re


def Chardetection(html):
    detector = UniversalDetector()
    for line in html.readlines():
        #分块进行测试，直到达到阈值
        detector.feed(line)
        if detector.done: break
    #关闭检测对象
    detector.close()
    html.close()
    return detector.result['encoding']

# 提取标题
def FindTitle(bs0bj, tree):
    titledata = tree.xpath('//*[@id="thread_subject"]/text()')
    if len(titledata) != 0:
        titledata = titledata[0]
    if len(titledata) == 0:
        titledata = tree.xpath('//title//text()')
        if len(titledata) == 0:
            pass
        else:
            titledata = re.sub("-(.*?)","",titledata[0])
            titledata = re.sub("_(.*?)","",titledata)
    if len(titledata) == 0:
        title = 'None'
    else:
        title = titledata
    return title


# 目标文件夹路径
path = "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\"

# 打开文件，读取信息，关闭文件
all_url_file = open(
    "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url.pkl", "rb")
html = pickle.load(all_url_file)
all_url_file.close()


# 主函数
for each in html:
    try:
        each_html = urlopen(each,timeout=3)
        bs0bj = bs(each_html)
        bs0bj = str(bs0bj)
        tree = etree.HTML(bs0bj) # 解析树
        title = FindTitle(bs0bj,tree)  # 寻找标题
        title = str(n)+'.'+ title +'\n'
        with open(path + "all_url_title.txt", 'a', encoding='gb18030') as json_file:
            json_file.write(title)
        n += 1
        print(n)
        print(title)
        
    # 异常处理
    except (HTTPError, ConnectionResetError, URLError, AttributeError, TypeError, UnicodeEncodeError,timeout) as reason:
        error_file = open(
            path + "all_url_error2.txt", "w")
        n += 1
        reason = str(n) + '.' + str(reason) + '\r'
        error_file.writelines(reason)
        error_file.close()
        print(reason)
        continue
