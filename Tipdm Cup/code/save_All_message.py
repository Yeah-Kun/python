from urllib.request import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup as bs   # Extract content
import pickle    # save file
from chardet.universaldetector import UniversalDetector

all_url_file = open(
    "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url.pkl", "rb")

# Analysis of Web site coding format


def Detection_coding_format(html):
    detector = UniversalDetector()
    for line in html.readlines():
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result['encoding']

# find the title in the page code


def Find_title(bs0bj):
    title = bs0bj.find('title').get_text()
    title = str(n) + '.' + str(title) + '\r'
    return title

def Find_date(bs0bj):
    

html = pickle.load(all_url_file)
n = 0
for each in html:
    try:
        each_html = urlopen(each)  # open the page code
        chardet = Detection_coding_format(each_html)# find the page encoding format
        each_html = urlopen(each)
        bs0bj = bs(each_html)    
        title = Find_title(bs0bj)

        save_file = open(
            "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url_title_new.txt", "a")
        save_file.writelines(title)
        save_file.close()
        n += 1
        print(n)
    except (HTTPError, ConnectionResetError, URLError, AttributeError, TypeError, UnicodeEncodeError) as reason:
        error_file = open(
            "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url_error_new.txt", "a")
        n += 1
        reason = str(n) + '.' + str(reason) + '\r'
        error_file.writelines(reason)
        error_file.close()
        print(reason)
        continue

all_url_file.close()
