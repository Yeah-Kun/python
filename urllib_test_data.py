from urllib.request import urlopen
import os
import pickle

req = urlopen("http://baa.bitauto.com/changancs75/thread-9819102.html")

file_keep = req.read().decode("utf-8")  # 将获取的文件给变量

pickle_file = open(
    "D:\\Users\\YeahKun\\Desktop\\data process\\file_keep.pkl", "wb")  # 新建坛子文件

pickle.dump(file_keep, pickle_file)  # 将泡菜对象放到坛子文件里面

pickle_file.close()  # 关闭文件

pickle_file = open("file_keep.pkl", "rb")  # 打开文件

file_keep = pickle.load(pickle_file)  # 把泡菜拿出来

print(file_keep)
