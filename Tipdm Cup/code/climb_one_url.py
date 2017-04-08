from urllib.request import urlopen, HTTPError, URLError
import json
from bs4 import BeautifulSoup as bs
from chardet.universaldetector import UniversalDetector
import re
# 编码格式识别
def Detection_coding_format(html):
    detector = UniversalDetector()
    for line in html.readlines():
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result['encoding']

url = "http://bbs.tianya.cn/post-worldlook-1774393-1.shtml"
req = urlopen(url)
chardet = Detection_coding_format(req)
req = urlopen(url)
bs0bj = bs(req).get_text()
with open("D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\one_url_data.txt", "a+",encoding=chardet) as file_obj:
    file_obj.write(bs0bj)