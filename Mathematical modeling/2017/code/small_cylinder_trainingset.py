'''将数学建模A题小柱训练集
	create by Ian in 2017-9-16 17:39:31
'''

import numpy as np
from matplotlib import pyplot as plt
from openpyxl import load_workbook
import plotly.plotly as py


def new_set(data):
	sheet = data.get_sheet_by_name("附件2")
	y = []

	for i in list(sheet.rows): # 遍历表的所有行：rows，列:columns
		print(i)

	print(y)

def main():
	path = "D:/Users/Yeah_Kun/Desktop/"
	data = load_workbook(path+'A.xlsx')
	new_set(data)
	


if __name__ == '__main__':
	main()