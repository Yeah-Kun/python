'''
	朴素贝叶斯分类器
	create by Ian in 2018-4-8 16:21:55
'''
from PyQt5.QtWidgets import QApplication,QWidget,QFileDialog
import PyQt5.uic
import re
import sys
import jieba
import pickle


ui_file = 'FBBC.ui'
(class_ui, class_basic_class) = PyQt5.uic.loadUiType(ui_file)

class MainWindow(class_basic_class,class_ui):
	"""窗口类"""
	def __init__(self):
		super(MainWindow,self).__init__()
		self.setupUi(self)
		self.setWindowTitle('朴素贝叶斯分类器（中文）')  
		self.openbtn.clicked.connect(self.open_file)
		self.cleanbtn.clicked.connect(self.clean_textEdit)
		self.trainbtn.clicked.connect(self.train_model)
		self.loadmodelbtn.clicked.connect(self.load_model)
		self.savemodelbtn.clicked.connect(self.save_model)
		self.predictbtn.clicked.connect(self.predict)

		self.txtstring = None # 存储文本框数据
		self.bc = BayesClassifier() # 贝叶斯分类器
	
	def open_file(self):
		"""打开文件操作"""
		filename, filetypes = QFileDialog.getOpenFileName(self, "选取文件", "./", "Text Files (*.txt)")
		print(filename)

		if filename != None:
			if filetypes == "Text Files (*.txt)":
				with open(filename,"r") as file:
					self.txtstring = file.read()
					self.textEdit.setText(self.txtstring)
			else:
				print(filetypes)
				print("暂时无法读取这种格式的数据")
		return filename

	def clean_textEdit(self):
		"""清空文本框"""
		self.textEdit.clear()

	def get_textEdit(self):
		"""获得textEdit的当前值
		"""
		self.txtstring = self.textEdit.toPlainText()


	def load_model(self):
		"""加载模型"""
		filename, filetypes = QFileDialog.getOpenFileName(self, "选取模型", "./", "All Files (*)")
		print(filename)
		if filename != "":
			with open(filename, "rb") as f:
				self.bc = pickle.load(f)


	def save_model(self):
		"""保存模型
		"""
		filename, filetypes = QFileDialog.getSaveFileName(self, "保存模型", "./", "All Files (*)")
		if filename != "":
			with open(filename, "wb") as f:
				pickle.dump(self.bc, f)


	def train_model(self):
		"""训练模型"""
		self.get_textEdit()
		if self.txtstring == "": # 如果没装入数据就pass了
			pass
		else:
			if self.likerdb.isChecked():
				self.bc.calcu_word(self.txtstring, "like")
			elif self.normalrdb.isChecked():
				self.bc.calcu_word(self.txtstring, "normal")
			elif self.unlikerdb.isChecked():
				self.bc.calcu_word(self.txtstring, "unlike")


	def predict(self):
		"""模型预测
		"""
		self.get_textEdit()
		if self.txtstring == "": # 如果没装入数据就pass了
			pass
		else:
			selector, like, normal, unlike = self.bc.predict(self.txtstring)
			self.likeline.setText(str(like))
			self.normalline.setText(str(normal))
			self.unlikeline.setText(str(unlike))
			if selector == "like":
				self.predictline.setText("喜欢")
			elif selector == "normal":
				self.predictline.setText("一般般")
			elif selector == "unlike":
				self.predictline.setText("不喜欢")
			else:
				self.predictline.setText("无法预测")


class BayesClassifier(object):
	"""朴素贝叶斯分类器"""
	def __init__(self):
		self.all_word = {} # 存放训练集所有词，词频
		self.like_word = {} # 存放喜欢的词
		self.normal_word = {} # 存放一般的词
		self.unlike_word = {} # 存放不喜欢的词
		self.like_prob = {}
		self.normal_prob = {}
		self.unlike_prob = {}
		self.seg_list = [] # 暂存切割好的词（列表）
		self.selector = None # 判断文本喜欢的类别

		# 概率
		self.like = 1.
		self.normal = 1.
		self.unlike = 1.


	def cut_word(self, origin):
		"""结巴分词
		"""
		origin = re.sub(r"[^\u4e00-\u9fa5]+", "", origin) # 除去所有非中文的字符
		self.seg_list = jieba.lcut(origin) # jieba搜索引擎模式分词


	def calcu_word(self, word, mode):
		"""训练模型，输入新训练集，计算新词频
		"""
		self.cut_word(word)
		for i in range(len(self.seg_list)):
			i = self.seg_list[i]
			if i in self.all_word:
				self.all_word[i] += 1
			else:
				self.all_word[i] = 1
			if mode == "like":
				if i in self.like_word:
					self.like_word[i] += 1
				else:
					self.like_word[i] = 1
			
			elif mode == "normal":
				if i in self.normal_word:
					self.normal_word[i] += 1
				else:
					self.normal_word[i] = 1

			elif mode == "unlike":
				if i in self.unlike_word:
					self.unlike_word[i] += 1
				else:
					self.unlike_word[i] = 1
		print(self.all_word)

		# 计算词在like中出现的概率
		for i in self.like_word:
			prob = self.like_word[i] / self.all_word[i]
			self.like_prob[i] = prob
		for i in self.normal_word:
			prob = self.normal_word[i] / self.all_word[i]
			self.normal_prob[i] = prob
		for i in self.unlike_word:
			prob = self.unlike_word[i] / self.all_word[i]
			self.unlike_prob[i] = prob


	def predict(self, word):
		"""模型预测
		"""
		self.cut_word(word)
		for i in self.seg_list:
			if i in self.like_word:
				self.like *= self.like_prob[i]
			else:
				self.like *= (len(self.like_word) + 1) / (len(self.all_word) + 3)  # 拉普拉斯平滑
			if i in self.normal_word:
				self.normal *= self.normal_prob[i]
			else:
				self.normal *= (len(self.normal_word) + 1) / (len(self.all_word) + 3)
			if i in self.unlike_word:
				self.unlike *= self.unlike_prob[i]
			else:
				self.unlike *= (len(self.unlike_word) + 1) / (len(self.all_word) + 3)

			if (self.like <= 1e-5 and self.normal <= 1e-5 and self.unlike <= 1e-5):
				self.like *= 10000
				self.normal *= 10000
				self.unlike *= 10000

		if self.like > self.normal and self.like > self.unlike:
			self.selector = "like"
		elif self.normal > self.like and self.normal > self.unlike:
			self.selector = "normal"
		elif self.unlike > self.like and self.unlike > self.normal:
			self.selector = "unlike"
		else:
			self.selector = "error"

		print(self.unlike_prob)
		return (self.selector, self.like, self.normal, self.unlike)


if __name__=='__main__':
    app=QApplication(sys.argv)
    w=MainWindow()
    w.show()
    app.exec_()