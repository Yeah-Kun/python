'''
	计时器增强版
	小甲鱼第44课课程内容	
	两个计时器的值可相加
'''
import time

class Mytimer(object):
	"""docstring for Mytimer"""
	def __init__(self,set_timer=0):
		self.begin = 0
		self.end = 0
		self.format = ['年','月','日','时','分','秒']
		self.set_timer = set_timer
		print("计时器建立完毕！")

	# 让实例化对象显示计时器内容
	def __str__(self):
		return self.prompt

	__repr__ = __str__

	# 使两个实例化对象可以相加
	def __add__(self,other):
		return float.__add__(self.lasted,other.lasted)

	# 计时器开始
	def start(self):
		print("计时开始...")
		if self.set_timer == 0:
			self.begin = time.perf_counter()
		else:
			self.begin = time.process_time()

	# 计时器关闭
	def stop(self):
		if self.begin == 0:
			print("请先使用start()方法启动计时器！")
		else:
			if self.set_timer == 0 :
				self.end = time.perf_counter()
			else:
				self.begin = time.process_time()
			print("计时结束！")
			self.calc()

	# 内置函数，用于求得计时器运算时间
	def calc(self):
		self.lasted = []
		self.prompt = "总共运行了"
		self.lasted = self.end - self.begin
		self.prompt += str(self.lasted)
	

