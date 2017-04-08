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


# open the jar
all_url_file = open(
    "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url.pkl", "rb")

url = pickle.load(all_url_file)  # Take the pickles out of the jar
n = 0
for each_url in url:
    try:
        req = urlopen(each_url)
        chardet = Detection_coding_format(req)
        req = urlopen(each_url)
        bs0bj = bs(req,from_encoding=chardet).get_text()
        with open("D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url_data.pkl", "ab") as pickle_file:
        	pickle.dump(bs0bj, pickle_file)
        	pickle_file.close()
        n += 1
        print(n)
    except (HTTPError, ConnectionResetError, URLError) as reason:
        error_file = open(
            "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url_error_new.txt", "a")
        n += 1
        reason = str(n) + '.' + str(reason) + '\r'
        error_file.writelines(reason)
        error_file.close()
        print(reason)
        continue
all_url_file.close()
