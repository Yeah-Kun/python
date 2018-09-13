'''
	计时器，小甲鱼第44课课程内容	
'''
import time

class Mytimer(object):
	"""docstring for Mytimer"""
	def __init__(self):
		self.begin = 0
		self.end = 0
		self.format = ['年','月','日','时','分','秒']
		print("计时器建立完毕！")

	# 让实例化对象显示计时器内容
	def __str__(self):
		return self.prompt

	__repr__ = __str__

	# 计时器开始
	def start(self):
		print("计时开始...")
		self.begin = time.localtime()

	# 计时器关闭
	def stop(self):
		if self.begin == 0:
			print("请先使用start()方法启动计时器！")
		else:
			print("计时结束！")
			self.end = time.localtime()
			self.calc()

	# 内置函数，用于求得计时器运算时间
	def calc(self):
		self.lasted = []
		self.prompt = "总共运行了"
		for i in range(6):
			self.lasted.append(self.end[i] - self.begin[i])
			# 避免时间出现负数，进行分和秒的时间转换
			if self.lasted[i] < 0:
				self.lasted[i-1] -= 1
				self.lasted[i] = 60 - self.lasted[i]
			# 输出计时器信息，如果为0的信息则略过
			if self.lasted[i] != 0:
				self.prompt = self.prompt + str(self.lasted[i]) + self.format[i]
	

