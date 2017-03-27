import pickle
import os

all_url = []  # create a empty list to save all separated url

read_url = open("D:\\Users\\YeahKun\\Desktop\\TDcup\\url\\bbs_urls.txt", "r")

# split the text and save all of it
for each_line in read_url:
    all_url.append(each_line)

#print(len(all_url)) # test, in order to know the the count of all url
#build a new jar to save pickle(all url)
allurl_file = open(
    "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url.pkl", "wb")

pickle.dump(all_url,allurl_file)#put the pickle to the jar

print(all_url[23])
allurl_file.close()#close the file


