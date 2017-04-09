from urllib.request import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup as bs   # Extract content
import re

with open("D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\one_url_data.txt", "r", encoding="gb18030") as file_keep:
    bs0bj = file_keep.read()
bs0bj = re.sub("[^\u4e00-\u9fa5，。！？\r\n]", "", bs0bj)

with open("D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\clean_url_data.txt", "w") as file_clean:
    file_clean.write(bs0bj)


with open("D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\clean_url_data.txt", "r", encoding="gb18030") as file_keep:
    for line in file_keep.readlines():
    	if len(line) >= 60:
    		with open("D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\save_url_main.txt", "a", encoding="gb18030") as file_main:
    			file_main.write(line)
    			file_main.write("\r")	
    		print(line)
    		break
	