from urllib.request import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup as bs   # Extract content
import pickle    # save file
from chardet.universaldetector import UniversalDetector
import re


# 提取标题
def Find_title(bs0bj):
    title = bs0bj.find('title')
    Title = {'title': title}
    return Title


#  提取时间
def Find_date(bs0bj):
    date = re.findall("发表于 \d{4}-\d{2}-\d{2}", bs0bj)
    if date == None:
        date = re.findall("\d{4}/\d{2}/\d{2}", bs0bj)
    if date == None:
        date = re.findall("\d{4}-\d{2}-\d{2}", bs0bj)
    if date == None:
        date = re.findall("\d{2}-\d{2}-\d{4}", bs0bj)
    if date == None:
        date = re.findall("时间 \d{4}/\d{2}/\d{2}", bs0bj)
 #   date = str(date)
    dict_date = {'publish_date': date}
    return dict_date


# 提取正文
def Find_main(bs0bj):
    bs0bj = re.sub("[^\u4e00-\u9fa5，。-！？\r\n]", "", bs0bj)
    for line in bs0bj.readlines():
        if len(line) >= 30:
            return (line)
    return None


# 文件夹路径
path = "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\"


#  打开文件并读取文件
all_url_file = open(
    path + "all_url.pkl", "rb")
html = pickle.load(all_url_file)
all_url_file.close()


# 提取
n = 0
for each in html:
    try:
        each_html = urlopen(each)
        bs0bj = bs(each_html).get_text()
        title = Find_title(bs0bj)  # 爬取标题
        date = Find_date(bs0bj)  # 爬取时间

        # 保存数据
        save_file = open(
            path + "all_url_title_new.txt", "a", encoding='gb18030')
        save_file.writelines(title)
        save_file.close()
        n += 1
        print(n)
    except (HTTPError, ConnectionResetError, URLError, AttributeError, TypeError, UnicodeEncodeError) as reason:
        error_file = open(
            path + "all_url_error_new.txt", "a")
        n += 1
        reason = str(n) + '.' + str(reason) + '\r'
        error_file.writelines(reason)
        error_file.close()
        print(reason)
        continue
