from urllib.request import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup as bs   # Extract content
import pickle    # save file
from chardet.universaldetector import UniversalDetector
import re

all_url_file = open(
    "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url.pkl", "rb")

# Analysis of Web site coding format


def Detection_coding_format(html):
    detector = UniversalDetector()
    for line in html:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result['encoding']

html = pickle.load(all_url_file)
n = 0
k = 0
for each in html:
    try:
        n += 1
        print(n)
        each_html = urlopen(each)  # open the page code
        chardet = Detection_coding_format(each_html)
        each_html = urlopen(each)
        bs0bj = bs(each_html, from_encoding=chardet)
        date = re.search("发表于 \d{4}-\d{2}-\d{2}",bs0bj.get_text())
        print(date)
        date = str(n) + '.' + str(date) + '\r'
        pickle_file = open(
            "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url_date.txt", "a")
        pickle_file.writelines(date)
        pickle_file.close()
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
