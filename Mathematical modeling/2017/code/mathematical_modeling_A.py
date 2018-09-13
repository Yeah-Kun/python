'''将数学建模A题各种图像
	create by Ian in 2017-9-14 20:53:26
'''

import numpy as np
from matplotlib import pyplot as plt
import xlrd
import plotly.plotly as py
from mpl_toolkits.mplot3d import Axes3D

def twoD_1(data):
	'''附件一2D图'''
	table = data.sheets()[0]
	nrows = table.nrows # 获取行数
	ncols = table.ncols # 获取列数
	fig = plt.figure(figsize=(10,10))
	ax = fig.gca()

	y = [table.col_values(i) for i in range(nrows)] # 获取其每行的值
	x = np.arange(1,ncols+1,1) # 横坐标x

	for i in range(nrows):
		y[i] = [y[i][j]*i for j in range(ncols)]
		ax.scatter(x, y[i], color='r')
	ax.scatter(128,128, color='k',marker='x')
	ax.scatter(128-33/2,128+24/2, color='k',marker='x')
	# 图标注
	ax.annotate('center of rotation', xy=(128-33/2+2,128+24/2+2))
	return ax

def twoD_2(data):
	'''附件二2D图'''
	table = data.sheets()[1]
	nrows = table.nrows # 获取行数
	ncols = table.ncols # 获取列数

	'''
	y = [table.row_values(i) for i in range(1,nrows)] # 获取其每行的值
	x = np.arange(1,ncols+1,1)
	print(nrows)
	for i in range(ncols):
		plt.scatter(x, y[i], label='info', color='r', s=180, marker="x")
	'''
	y = [table.col_values(i) for i in range(ncols)] # 获取其每列的值
	x = np.arange(1,nrows+1,1) # 横坐标x

	for i in range(ncols):
		plt.plot(x, y[i], label='info', color='r')

	# 图标注
	plt.xlabel("512个探测器") # X轴
	plt.ylabel("吸收强度") # Y轴
	y = np.array(y)
	print(y.shape)


def twoD_2_special(data):
	'''经过处理的附件二2D图'''
	table = data.sheets()[4]
	nrows = table.nrows # 获取行数512
	ncols = table.ncols # 获取列数180
	x = np.arange(1,nrows+1,1) # 初始化x，x为512个探测器
	#y = [table.col_values(i) for i in range(ncols)] # 获取其每行的值
	y = []

	for i in range(ncols):
		y.append(table.col_values(i))
		for j in range(nrows):
			if y[i][j] != 0:
				y[i][j] = 1

	for i in range(ncols):
		y[i] = [y[i][j]*i for j in range(nrows)]
		plt.scatter(x,y[i],s=0.1)
'''
	# 用于消除大椭圆的值，只保留小圆柱的值
	for i in range(ncols):
		temp = 0
		sign_j = 0
		for j in range(nrows):
			if y[i][j] != 0:
				if sign_j == 0: 
					sign_j = j
				temp = temp + 1
				if temp > 30:
					while y[i][sign_j] != 0:
						y[i][sign_j] = 0
						sign_j = sign_j + 1
			else:
				sign_j = 0

	#print(len(y))
	print(y)
'''

'''	
	# xlwt只能保存255行/列数据，弃用
	wb = xlwt.Workbook()
	sheet = wb.add_sheet("test")
	for i in range(ncols):
		for j in range(255):
			sheet.write(i,j,y[i][j])
	wb.save('test.xls')
	'''
	#plt.plot(x, y, label='info', color='r')
	#plt.show()

def threeD_1(data):
	'''附件一3D图'''
	table = data.sheets()[0]
	nrows = table.nrows # 获取行数
	ncols = table.ncols # 获取列数
	x = np.arange(1,nrows+1,1) # 初始化x，y轴
	y = np.arange(1,ncols+1,1)
	X, Y = np.meshgrid(x, y) # 生成网格
	z = []
	fig = plt.figure()
	ax = Axes3D(fig)
	for i in range(nrows):
		z.append(table.row_values(i))
	ax.plot_surface(X,Y,z,rstride=1, cstride=1, cmap='rainbow')


def threeD_2(data):
	'''附件二3D图'''
	table = data.sheets()[1]
	nrows = table.nrows # 获取行数
	ncols = table.ncols # 获取列数
	x = np.arange(1,nrows+1,1) # 初始化x，y轴
	y = np.arange(1,ncols+1,1)
	k = []
	for i in range(nrows):
		k.append(0)
	z = []

	for i in range(ncols):
		if i%20 == 0:
			z.append(table.col_values(i))
		else:
			z.append(k)

	X, Y = np.meshgrid(x, y) # 生成网格

	fig = plt.figure()
	ax = Axes3D(fig)
	#ax.plot_surface(X,Y,z,rstride=1, cstride=1, cmap='rainbow') 
	ax.plot_surface(X,Y,z,rstride=1, cstride=1,linewidth=0, antialiased=False) # 蓝图
	#plt.contourf(X, Y, z, 8, alpha = 0.75, cmap = 'rainbow') # 等高线图
	#plt.xticks(np.linspace(0, 512, 20)) # 设置x轴的标尺


def gridlines():
	'''网格线'''
	grid = np.arange(0,512,50) # 初始化网格
	fig = plt.figure(figsize=(10,10))
	ax = fig.gca()
	#ax.set_xticks(np.arange(0, 512, 1)) # 设置网格
	#ax.set_yticks(np.arange(0, 512, 1))
	ax.scatter(256, 256) # 绘点
	#ax.scatter(289,232)
	ax.scatter(219.5, 245.5)
	ax.scatter(142, 98)
	ax.scatter(142, 393)
	ax.scatter(297, 98)
	ax.scatter(297, 393)
	ax.annotate('(256, 256)', xy=(258, 258))
	#ax.annotate('(289, 232)', xy=(291, 234))
	ax.annotate('(219.5, 245.5)', xy=(219.5+3, 245.5-10))
	plt.yticks(grid)
	plt.xticks(grid)
	plt.xlabel("x") # X轴
	plt.ylabel("y") # Y轴
	plt.grid(c='black')
	return ax


def main():
    path = "D:/code/python/Mathematical modeling/CUMCM2017Problems/A/"
    data = xlrd.open_workbook(path + 'A题附件.xls')
    #threeD(data)
    #trace = go.Heatmap(z=z,x=x,y=y)
    #data = [trace]
    #py.iplot(data, filename='labelled-heatmap')

    #twoD_1(data)
    #twoD(data)
    #twoD_2(data)
    #twoD_2_special(data)
    #threeD_2(data)
    gridlines()
    plt.show()

if __name__ == '__main__':
    main()
