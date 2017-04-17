'''
    保存所有url的标题
'''
from urllib.request import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup as bs   # Extract content
import pickle    # save file
import json
import copy
from socket import timeout

# 打开文件，读取信息，关闭文件
all_url_file = open(
    "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url.pkl", "rb")
html = pickle.load(all_url_file)
all_url_file.close()


# 提取标题
def Find_title(bs0bj):
    title = bs0bj.find('title').get_text()
    Title = {'title': title}
    return Title


# 目标文件夹路径
path = "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\"
n = 0
k = 0


# 主函数
for each in html:
    try:
        n += 1
        print(n)
        each_html = urlopen(each,timeout=3)
        bs0bj = bs(each_html)
        title = Find_title(bs0bj)  # 寻找标题
        post = {'post':str(title)}
        with open(path + "all_url_title.txt", 'a', encoding='gb18030') as json_file:
            json.dump(post, json_file, ensure_ascii=False, sort_keys=True)
        print(post)
        
    # 异常处理
    except (HTTPError, ConnectionResetError, URLError, AttributeError, TypeError, UnicodeEncodeError,timeout) as reason:
        error_file = open(
            path + "all_url_error2.txt", "a")
        n += 1
        reason = str(n) + '.' + str(reason) + '\r'
        error_file.writelines(reason)
        error_file.close()
        print(reason)
        continue
