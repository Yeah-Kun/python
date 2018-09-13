"""
	本地测试lxml抓取试卷关键内容并进行分析
"""
from lxml import etree
from lxml import html
import pickle
import re

class Paper(object):
	"""
		试卷类，包含试卷的题目，答案以及一些试卷的操作
	"""
	def __init__(self):
		self.form = {} # 需提交的form表单，本地code试卷号：数据库试卷号
		self.hd_database = {} # 试卷hd编号：数据库试卷号
		self.local_answer = {} # 对象文件库里的答案，格式 {数据库试卷号：答案}，如{"FX1234":"ABCD"}
		self.write_answer = {} # 判断、单选和多选题，hd编号：答案


	def getKeyValue(self,name,url):
		"""
			获取关键信息：
			本地code试卷号，数据库试卷号，个人信息
		"""
		url = r"D:\Users\Yeah_Kun\Desktop\auto_policy\paper.txt"
		with open(url,"r") as f:
			tree = html.fromstring(f.read())

		node = tree.xpath("//input[@type='hidden']") # 关键节点信息
		for i in node:
			if re.search("qcode",i.get('name')):
				hd = re.sub("qcode","hd",i.get('name')) # hd = hd号：数据库题号
				self.hd_database.update({ hd :i.get('value')})
				self.write_answer.setdefault(hd,None) # 填写试卷答案，初始答案默认为None

			self.form.update({i.get('name'):i.get('value')})
		self.form['sUXM'] = name
		self.form.update({"B1":" 交 卷 "})


	def writeQuestion(self):
		"""
			写入答案到write_answer
		"""
		for hd in self.hd_database.items():
			if hd[1] in self.local_answer.keys() and re.search("DX",hd[1]):
				self.write_answer[hd[0]] = self.local_answer[hd[1]] # 填写答案
			else:
				self.write_answer[hd[0]] = "A" # 单选题默认选A

			if hd[1] in self.local_answer.keys() and re.search("PD",hd[1]):
				self.write_answer[hd[0]] = self.local_answer[hd[1]] # 填写答案
			else:
				self.write_answer[hd[0]] = "R" # 判断题默认选R

			if re.search("FX",hd[1]):
				key = hd[0] # 获取key
				self.write_answer.pop(key) # 将复选标志弹出，意味着有标准答案

				if hd[1] in self.local_answer.keys(): 
					# 如果有答案
					result = re.findall("[A-Z]", self.local_answer[hd[1]]) # 找到答案列表		
					# 逐个答案写进write_answer
					counter = 1 # 复选项form的key从1开始
					for i in result:
						self.write_answer.update({ key+ str(counter) : i})
						counter += 1
				else: 
				# 没答案
					self.write_answer.update({ key + "1" : "A"}) # 默认填A


	def processResult(self, tree):
		"""
			根据网页返回的正确答案，更新本地数据库
			并写回数据库
			输出：answer.pkl
		"""
		file = "D:/Users/Yeah_Kun/Desktop/auto_policy/result2.html"
		with open(file,'r') as f:
			tree = html.fromstring(f.read())
		right = tree.xpath("//font[@color='#FF0000']") # 答案结点，#FF0000红色
		for font in right:
			if font.text is not None:
				strong = font.getprevious().getprevious() # strong标签在font标签上两个
				database_id,qtype = self.signQue(strong,font) # 返回数据库题号，题目类型（database_id）

				# 更新本地答案
				if database_id in self.local_answer.keys():
					self.local_answer.pop(database_id)

				if qtype == "PD" or qtype == "DX":
					self.local_answer[database_id] = re.search("[A-Z]",font.text)[0] # 写入判断或单选题答案
				else:
					if re.search("[A-Z]+(?=A)",font.text) is not None:
						self.local_answer[database_id] = re.search("[A-Z]+(?=A)",font.text)[0] # 写入多选题答案
					else:
						self.local_answer[database_id] = re.search("[A-Z]+(?=B)",font.text)[0] # 写入多选题答案


		wrong = tree.xpath("//font[@color='#0000FF']") # 答案结点，#0000FF蓝色
		for font in wrong:
			strong = font.getprevious().getprevious() # strong标签在font标签上两个
			database_id,qtype = self.signQue(strong,font) # 返回数据库题号，题目类型（database_id）

			# 更新本地答案
			if database_id in self.local_answer.keys():
				self.local_answer.pop(database_id)

			if qtype == "PD" or qtype == "DX":
				self.local_answer[database_id] = re.search("[A-Z]",font.text)[0]
			else:
				self.local_answer[database_id] = re.search("[A-Z]+(?=A)",font.text)[0]

		with open("answer.pkl","wb") as f: # 写回数据库
			pickle.dump(self.local_answer,f)
		print(len(self.local_answer))
		return self.local_answer
			

	def signQue(self,strong,font):
		"""
			识别题目的编号和类型，返回数据库题号

			输入：strong节点
			判断：题目编号num，题目类型flag
			输出：数据库题号,题目类型(PD，DX，FX)
		"""
		num = re.search("\d{1,2}",str(strong.xpath("string(.)")))[0]
		flag = re.findall("[A-Z]",font.text)
		if len(flag) == 2:
			if flag[0] == 'W' or flag[0] == 'R':
				return self.hd_database["pdhd" + num],"PD"

			else:
				return self.hd_database["dxhd" + num],"DX"

		else:
			return self.hd_database["fxhd" + num],"FX"


	def getDBAnswer(self):
		"""
			获取本地数据库答案
		"""
		with open('answer.pkl','rb') as pickle_file:
			self.local_answer = pickle.load(pickle_file)
		return self.local_answer

	def getForm(self):
		"""
			返回Form表单
		"""
		self.form.update(self.write_answer)
		print(self.form)
		return self.form

	def test_id(self):
		for i in self.hd_database.items():
			print(i)

if __name__ == '__main__':
	p = Paper()
	p.getKeyValue("叶坤",None)
	p.getDBAnswer()
	p.writeQuestion()
	p.processResult("tree")
	p.getForm()