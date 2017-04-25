'''
	主函数，用于运行源代码
'''
from urllib.request import urlopen, HTTPError, URLError
import json
from bs4 import BeautifulSoup as bs
import re
from TDcup import tree_algorithm, the_module
from lxml import etree


