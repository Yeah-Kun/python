'''
    保存所有url的标题
'''
from urllib.request import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup as bs   # Extract content
import pickle    # save file
from chardet.universaldetector import UniversalDetector


# 
all_url_file = open(
    "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url.pkl", "rb")
html = pickle.load(all_url_file)
all_url_file.close()


n = 0
k = 0
for each in html:
    try:
        n += 1
        print(n)
        each_html = urlopen(each)  # open the page code
        chardet = Detection_coding_format(each_html)
        each_html = urlopen(each)
        bs0bj = bs(each_html)
        title = bs0bj.find('title').get_text()
        title = str(n) + '.' + str(title) + '\r'
        pickle_file = open(
            "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url_title2.txt", "a",encoding='gb18030')
        pickle_file.writelines(title)
        pickle_file.close()

    # 异常处理
    except (HTTPError, ConnectionResetError, URLError, AttributeError, TypeError, UnicodeEncodeError) as reason:
        error_file = open(
            "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url_error2.txt", "a")
        n += 1
        reason = str(n) + '.' + str(reason) + '\r'
        error_file.writelines(reason)
        error_file.close()
        print(reason)
        continue

