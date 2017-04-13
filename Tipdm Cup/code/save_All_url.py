'''
	快速查找177个网站url的任何一个url
'''
import pickle
import os

# 打开文件，创建列表，将每一个url添加到列表，关闭文件
read_url = open("D:\\Users\\YeahKun\\Desktop\\TDcup\\C题资料\\bbs_urls.txt", "r")
all_url = []
for each_line in read_url:
    all_url.append(each_line)
read_url.close()


# 存储列表中的url
allurl_file = open(
    "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url.pkl", "wb")
pickle.dump(all_url,allurl_file)
print(all_url[42]) # 输出列表代号的url ，用于快速查找
allurl_file.close()


