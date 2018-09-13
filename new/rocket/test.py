"""
	测试模块
	create by Ian in 2018-6-18 19:50:41

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def readdata():
	"""数据测试模块，读数据并进行测试，必须拟合内容
	"""
	reader = pd.read_csv('data.csv',names=['t','P','m','C_Y', 'C_D', 'C_M', 'J']) 
	
	t = reader['t'][27:149]
	P = reader['C_M'][27:149]

	
	P_curve = np.polyfit(t,P,200)
	y = np.polyval(P_curve, t)
	print(np.polyval(P_curve, 0.22))
	plt.plot(t,P)
	plt.plot(t,y)
	plt.show()


def pltdata():
	"""读取某些系数特征值并拟合，非必须拟合内容
	"""
	reader = pd.read_csv('test.csv',names=['t','M']) 
		
	t = reader['t']
	C_M = reader['M']

	C_M_curve = np.polyfit(t,C_M,200)
	y = np.polyval(C_M_curve, t)
	print(np.polyval(C_M_curve, 0.8))
	plt.plot(t,C_M)
	plt.plot(t,y)
	plt.show()



def gen_data():
	"""生成的数据
	"""
	pass


def main():
	pltdata()
	#readdata()


if __name__ == '__main__':
	main()