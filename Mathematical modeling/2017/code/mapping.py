'''将数学建模A题映射图
	create by Ian in 2017-9-16 16:18:58
'''

import numpy as np
from matplotlib import pyplot as plt
import xlrd
import plotly.plotly as py
import mathematical_modeling_A
from matplotlib.patches import ConnectionPatch


def mapping(data):
	'''映射图'''
    fig = plt.figure()
    ax1 = plt.subplot(121)
    ax2 = plt.subplot(122)
    table = data.sheets()[0]
    nrows = table.nrows  # 获取行数
    ncols = table.ncols  # 获取列数

    y = [table.row_values(i) for i in range(nrows)]  # 获取其每行的值
    x = np.arange(1, nrows + 1, 1)  # 横坐标x

    for i in range(ncols):
        y[i] = [y[i][j] * i for j in range(nrows)]
        ax2.scatter(x, y[i], color='r')
    ax2.scatter(128, 128, color='k', marker='x')
    ax2.scatter(128 - 33 / 2, 128 + 24 / 2, color='k', marker='x')
    # 图标注
    ax2.annotate('center of rotation', xy=(128 - 33 / 2 + 2, 128 + 24 / 2 + 2))
    ax2.set_title('calibration template')
    grid = np.arange(0, 512, 50)  # 初始化网格
    ax1.scatter(256, 256)  # 绘点
    ax1.scatter(289, 232)
    ax1.annotate('(256, 256)', xy=(258, 258+4))
    ax1.annotate('(289, 232)', xy=(291, 234+4))
    ax1.set_yticks(grid)
    ax1.set_xticks(grid)
    ax1.set_title("detector array")
    ax1.set_xlabel("x")  # X轴
    ax1.set_ylabel("y")  # Y轴
    ax1.grid(c='black')
    con1 = ConnectionPatch(xyA=(128 - 33 / 2, 128 + 24 / 2), xyB=(256, 256),coordsA="data", coordsB="data",
                          axesA=ax2, axesB=ax1, arrowstyle="->", shrinkB=5)
    con2 = ConnectionPatch(xyA=(128,128), xyB=(289, 232),coordsA="data", coordsB="data",
                          axesA=ax2, axesB=ax1, arrowstyle="->", shrinkB=5)
    ax2.add_artist(con1)
    ax2.add_artist(con2)
    plt.show()


def main():
    path = "D:/code/python/Mathematical modeling/CUMCM2017Problems/A/"
    data = xlrd.open_workbook(path + 'A题附件.xls')
    mapping(data)


if __name__ == '__main__':
    main()
