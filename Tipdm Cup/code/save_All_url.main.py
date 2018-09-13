from urllib.request import urlopen, HTTPError, URLError
import os
import pickle
from chardet.universaldetector import UniversalDetector
import re
from bs4 import BeautifulSoup as bs

# 编码格式识别
def Detection_coding_format(html):
    detector = UniversalDetector()
    for line in html.readlines():
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result['encoding']


def Find_main(bs0bj):
    bs0bj = re.sub("[^\u4e00-\u9fa5，。！？\r\n]", "", bs0bj)
    for line in bs0bj.readlines():
        if len(line) >= 30:
            return (line)
    return None



all_url_file = open(
    "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url.pkl", "rb")

url = pickle.load(all_url_file)  # Take the pickles out of the jar
n = 0
for each_url in url:
    try:
        req = urlopen(each_url)
        chardet = Detection_coding_format(req)
        req = urlopen(each_url)
        bs0bj = bs(req,from_encoding=chardet)
        bs0bj = str(bs0bj)
        with open("D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url_data.txt", "a",encoding='gb18030') as pickle_file:
        	pickle_file.write(bs0bj)
        with open("D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url_data.txt", "r",encoding='gb18030') as pickle_file:
            bs0bj = pickle_file.readlines()
            with open("D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url_main.txt", "a") as pickle_save:
                main_data = Find_main(bs0bj)
                pickle_save.writelines(main_data)
        n += 1
        print(n)
    except (HTTPError, ConnectionResetError, URLError) as reason:
        error_file = open(
            "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url_error_main.txt", "a")
        n += 1
        reason = str(n) + '.' + str(reason) + '\r'
        error_file.writelines(reason)
        error_file.close()
        print(reason)
        continue
all_url_file.close()
