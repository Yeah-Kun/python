import jieba  # 分词模块
from collections import OrderedDict as order
'''
# 分词
with open("D:\\Users\\YeahKun\\Desktop\\play\\new_分词材料.txt","r") as file_material:
	file_material = file_material.read()
	seg_list = jieba.lcut(file_material)# 分词系统默认为精确模式
	seg_list = str(seg_list)
	with open("D:\\Users\\YeahKun\\Desktop\\play\\Splict_the_diary.txt","a") as file_save:  # 将分好的词放到文件里面
		file_save.write(seg_list)

'''
# 词频分析
def count_word(path):
	count = {}
	x = 0
	with open(path) as file_diary:
		file_diary = file_diary.read()
		for word in file_diary:
			if word not in count:
				count[word] = 1
			count[word] += 1
		return count

# 字典倒序排序
def sort_count(d):
	d = order(sorted(d.items(),key = lambda t:-t[1]))
	return d

path = "D:\\Users\\YeahKun\\Desktop\\play\\Splict_the_diary.txt"
word_count = count_word(path)

for key,value in word_count.items():
	print(key+":%d" %value)
