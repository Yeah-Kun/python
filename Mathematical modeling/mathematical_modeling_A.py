'''将数学建模A题附件一变成热力图
	create by Ian in 2017-9-14 20:53:26
'''

import numpy
import matplotlib
import xlrd
import plotly.plotly as py
import plotly.graph_objs as go

def main():
    path = "D:/Users/Yeah_Kun/Desktop/CUMCM2017Problems/A/"
    data = xlrd.open_workbook(path + 'A题附件.xls')
    table = data.sheets()[0]
    nrows = table.nrows # 获取行数
    ncols = table.ncols # 获取列数
    row_values = table.row_values(100)  # 获取某行的值
    x = [m for m in range(1, nrows + 1)]
    y = x
    z = [table.row_values(i) for i in range(1,256)]
    trace = go.Heatmap(z=z,x=x,y=y)
    data = [trace]
    py.iplot(data, filename='labelled-heatmap')

if __name__ == '__main__':
    main()
