'''
	爬取学校子系统
	create by Ian in 2017-11-30 21:22:43
'''
import requests
import time
import re

class Perfomance():

	def __init__(self):
		self.cookies = ''
		self.img = ''

	def crawl(self):
		'''抓取验证码，并保存验证码以及cookies'''
		url = "http://202.192.240.29/yzm?=11"
		try:
			r = requests.Session().get(url)
			self.cookies = str(r.cookies)
			i = time.time()
			with open("../data/{0}.png".format(i),'wb') as file:
				file.write(r.content)
			self.img = self.img.join([str(i),'.png']) # 拼接字符串
		except Exception as reason:
			return False

if __name__ == '__main__':
	b = Perfomance()
	b.crawl()