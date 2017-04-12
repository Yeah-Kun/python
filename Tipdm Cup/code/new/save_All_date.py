from urllib.request import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup as bs   # Extract content
import pickle    # save file
from chardet.universaldetector import UniversalDetector
import re


# 编码格式识别
def Detection_coding_format(html):
    detector = UniversalDetector()
    for line in html:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result['encoding']


#  爬取时间
def Find_date(bs0bj):
    date = re.search("发表于 \d{4}-\d{2}-\d{2}", bs0bj)
    if date == None:
        date = re.search("\d{4}/\d{2}/\d{2}", bs0bj)
    if date == None:
        date = re.search("\d{4}-\d{2}-\d{2}", bs0bj)
    if date == None:
        date = re.search("\d{2}-\d{2}-\d{4}", bs0bj)
    if date == None:
        date = re.search("时间 \d{4}/\d{2}/\d{2}", bs0bj)
    return date


# 文件夹路径
path = "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\"

# 打开文件，读取文件，关闭文件
all_url_file = open(
    path + "all_url.pkl", "rb")   # 文件名记得写后缀
html = pickle.load(all_url_file)
all_url_file.close()


n = 0
k = 0
for each in html:
    try:
        # 跟踪程序运行过程
        n += 1
        print(n)

        #
        each_html = urlopen(each)
        chardet = Detection_coding_format(each_html)
        each_html = urlopen(each)
        bs0bj = bs(each_html, from_encoding=chardet).get_text()
        # 找到时间
        date = Find_date(bs0bj)
        print(date)
        date = str(n) + '.' + str(date) + '\r'
        pickle_file = open(
            path + "all_url_date.txt", "a")
        pickle_file.writelines(date)
        pickle_file.close()

    # 异常处理
    except (HTTPError, ConnectionResetError, URLError, AttributeError, TypeError, UnicodeEncodeError) as reason:
        error_file = open(
            path + "all_url_date_error.txt", "a")
        n += 1
        reason = str(n) + '.' + str(reason) + '\r'
        error_file.writelines(reason)
        error_file.close()
        print(reason)
        continue
