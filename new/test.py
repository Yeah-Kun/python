import jieba  # 分词模块
from collections import OrderedDict as order
import re


# 词频分析
def count_word(path):
	count = {}
	x = 0
	with open(path) as file_diary:
		file_diary = file_diary.read()
		list_count = re.findall("(?<=').*?(?=[',\s])",file_diary)
		for word in list_count:
			if word not in count:
				count[word] = 1
			count[word] += 1
		return count

# 字典倒序排序
def sort_count(d):
	d = order(sorted(d.items(),key = lambda t:-t[1]))
	return d

diary_path = "D:\\Users\\YeahKun\\Desktop\\play\\Splict_the_diary.txt"
keyword_path = "D:\\Users\\YeahKun\\Desktop\\play\\keyword_and_statistics.txt"
word_count = count_word(diary_path)
word_count = sort_count(word_count)

with open(keyword_path,"a") as keyword_file:
	for key,value in word_count.items():
		word = str(key)+":"+str(value)+'\r'
		keyword_file.writelines(word)
		print(word)
