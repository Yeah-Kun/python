'''
	对网页源文件进行清洗，把不需要的内容都删掉
	这个程序主要是删除非中文，非数字和中文符号的内容
'''
#  引入第三方包，用作数据处理
from urllib.request import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup as bs   # Extract content
import re

# 文件夹的保存路径，就是你想保存在的那个文件夹的路径
path = "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\"

with open(path + "one_url_data.txt", "r", encoding="gb18030") as file_keep:   # 打开指定文件
    bs0bj = file_keep.read()    # 读取文件里面的内容
bs0bj = re.sub("[^\u4e00-\u9fa5，。！？0-9\r\n]", "", bs0bj)  # 正则表达式删除非中文，非数字和中文符号的内容

with open(path + "clean_url_data.txt", "w") as file_clean:   # 打开存放文件的
    file_clean.write(bs0bj)

# 统计每一行的文本密度，并将大于文本密度阈值的文本保存
with open(path + "clean_url_data.txt", "r", encoding="gb18030") as file_keep:
    for line in file_keep.readlines():
        if len(line) >= 60:
            with open(path + "save_url_main.txt", "a", encoding="gb18030") as file_main:
                file_main.write(line)
                file_main.write("\r")
            print(line)
            break
