'''
	抓取1024信息核心模块
	create by Ian in 2018-2-8 09:57:51
'''
import requests
from lxml import html
import re

class CrawlMain(object):
	"""docstring for CrawlMain
	   抓取主模块，包含抓取模块、存储模块、智能处理模块
	"""
	def __init__(self, originURL):
		super(CrawlMain, self).__init__()
		self.originURL = originURL # 主页面前的警告页面

	def do_main(self):
		'''模块主函数
		'''
		self.mainURL =self.get_main_url()
		ci = CrawlItems(self.mainURL)
		ci.get_plate_url()


	def get_main_url(self):
		'''获得主页面url
		'''
		try:
			r = requests.get(self.originURL)
		except Exception as e:
			raise e
		r = html.fromstring(r.text)
		a = r.xpath("/html/body/p[3]/b/font/a")[0].attrib # attrib获得标签内的值
		return self.originURL + a['href']

class CrawlItems(object):
	"""docstring for CrawlItems
	   爬取1024页面主要内容
	"""
	def __init__(self, mainURL):
		super(CrawlItems, self).__init__()
		self.mainURL = mainURL # 主要页面URL

	def get_plate_url(self):
		'''获取不同板块的url
		'''
		try:
			r = requests.get(self.mainURL)
		except Exception as e:
			raise e
		r = html.fromstring(r.text)
		trs = r.xpath('//tr[@class="tr3 f_one"]')
		url_contain = {} # 板块url容器
		for tr in trs:
			a = tr.xpath("/th[1]/h2/a")
			print(a.text)
			# url_contain.update({a[0].text : a['href']}) # 获得板块url
			# print({a.text : a['href']})
	

if __name__ == '__main__':
	c = CrawlMain("http://jinersi.tk/")
	c.do_main()