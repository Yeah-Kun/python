from urllib.request import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup as bs   # Extract content
import pickle    # save file
from chardet.universaldetector import UniversalDetector
import re

all_url_file = open(
    "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url.pkl", "rb")


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
    return date


html = pickle.load(all_url_file)
n = 0
k = 0
for each in html:
    try:
        n += 1
        print(n)
        if(n == 19):
            continue
        each_html = urlopen(each)  # open the page code
        print(".")
        chardet = Detection_coding_format(each_html)
        each_html = urlopen(each)
        print("..")
        bs0bj = bs(each_html, from_encoding=chardet).get_text()
        date = Find_date(bs0bj)
        print("...")
        print(date)
        date = str(n) + '.' + str(date) + '\r'
        pickle_file = open(
            "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url_date.txt", "a")
        pickle_file.writelines(date)
        pickle_file.close()
        print("....")
    except (HTTPError, ConnectionResetError, URLError, AttributeError, TypeError, UnicodeEncodeError) as reason:
        error_file = open(
            "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url_date_error.txt", "a")
        n += 1
        reason = str(n) + '.' + str(reason) + '\r'
        error_file.writelines(reason)
        error_file.close()
        print(reason)
        continue

all_url_file.close()
