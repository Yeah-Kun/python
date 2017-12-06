'''
	多个资源的银行家算法
	create by Ian in 2017-11-28 10:30:38
	描述：假设每个进程都需要同样的三种资源
'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import random
from copy import deepcopy


class AnalogSystem(list):
    '''模拟系统'''

    def __init__(self):
        self.Avaliable = [10, 10, 10]  # 系统拥有的资源数
        self.gave = []  # 系统给新进程的资源
        self.processing = []  # 进程
        self.counter = 0  # 进程计数器
        self.finish = []
        self.work = []
        self.safe_sequ = [] # 安全序列

    def randResource(self, R):
        '''随机分配资源给进程'''
        self.counter += 1
        del self.gave[:]  # 清空列表内容
        self.gave.append(random.randint(0, R[0]))
        self.gave.append(random.randint(0, R[1]))
        self.gave.append(random.randint(0, R[2]))
        for i in range(3):
            if(self.Avaliable[i] >= self.gave[i]):  # 如果有资源，才提供
                self.Avaliable[i] -= self.gave[i]
            else:  # 资源不足，进程不获取资源
                i -= 1  # 回退一个i，因为当前i下并没有分配资源给gave
                while i != -1:
                    self.Avaliable[i] += self.gave[i]  # 资源回收
                    i -= 1
                self.gave = [0, 0, 0]
                return self.Avaliable
        return self.Avaliable

    def returnGave(self):
        '''传递随机分配的资源'''
        return self.gave


    def checkSafety(self):
    	'''安全检测算法'''
    	del self.work[:] # 初始化
    	del self.finish[:]
    	del self.safe_sequ[:]
    	def isAllow(p):
    		'''判断Work是否大于Need'''
    		Need = []
    		Need = self.processing[p].returnNeed()
    		for i in range(3):
    			if self.work[i] < Need[i]:
    				return False
    		return True
    	def recycling(p):
    		'''回收资源'''
    		Need = []
    		Need = self.processing[p].returnNeed()
    		for i in range(3):
    			self.work[i] += Need[i]

    	self.work = deepcopy(self.Avaliable)
    	self.finish = [False for i in range(self.counter)]
    	k = 0
    	while k <= self.counter**2 : # 最多循环n的平方次
    		for p in range(self.counter):
    			if self.finish[p] == False and isAllow(p):
    				self.finish[p] = True 
    				self.safe_sequ.append(self.processing[p]) # 记录安全序列
    				recycling(p) # 回收资源
    			k += 1
    	if len(self.safe_sequ) == self.counter: # 检测是否存在安全序列
    		return True
    	else:
    		return False

    def getResource(self,p,r1,r2,r3):
    	'''进程请求系统资源'''
    	self.Avaliable[0] -= r1
    	self.Avaliable[1] -= r2
    	self.Avaliable[2] -= r3
    	if self.checkSafety():
    		p.addResource(r1,r2,r3)
    		return True
    	else:
    		self.Avaliable[0] += r1
    		self.Avaliable[1] += r2
    		self.Avaliable[2] += r3
    		return False

class Process():
    '''每个进程的数据内容'''

    def __init__(self):
        self.name = None
        self.Max = []  # 需要的最大资源数
        self.Allocation = []  # 已经分配的资源
        self.Need = []  # 还需要的资源

    def setName(self, name):
        self.name = name

    def setMax(self, R1, R2, R3):
        '''设置进程需要的最大资源数'''
        self.Max.append(R1)
        self.Max.append(R2)
        self.Max.append(R3)
        return [R1, R2, R3]

    def setAllocation(self, gave):
        '''获取系统分配的资源'''
        self.Allocation = deepcopy(gave)
        self.Need = list(
            map(lambda x: x[0] - x[1], zip(self.Max, self.Allocation)))

    def addResource(self,r1,r2,r3):
    	'''请求系统资源'''
    	self.Allocation = list(map(lambda x:x[0]+x[1],zip(self.Allocation,[r1,r2,r3])))
    	self.Need = list(
    	    map(lambda x: x[0] - x[1], zip(self.Max, self.Allocation)))
    	print(self.Need)

    def returnResource(self):
        '''返回进程的资源情况'''
        return [self.name, self.Allocation, self.Need]

    def returnNeed(self):
    	return self.Need


class MulDialog(QDialog):
    '''新建作业弹窗，自定义对话框'''

    def __init__(self):
        super().__init__()
        self.setWindowTitle(u"新建作业")
        self.resize(200, 180)
        self.grid = QGridLayout()
        self.name = QLineEdit()
        self.R1 = QLineEdit()
        self.R2 = QLineEdit()
        self.R3 = QLineEdit()
        self.buttonBox = QDialogButtonBox()
        self.layout = QVBoxLayout()
        self.initUI()

    def initUI(self):
        '''初始化UI'''
        self.grid.addWidget(QLabel(u"进程名：", parent=self), 0, 0, 1, 1)
        self.grid.addWidget(self.name, 0, 1, 1, 1)
        self.grid.addWidget(QLabel(u"需求资源R1：", parent=self), 1, 0, 1, 1)
        self.grid.addWidget(self.R1, 1, 1, 1, 1)
        self.grid.addWidget(QLabel(u"需求资源R2：", parent=self), 2, 0, 1, 1)
        self.grid.addWidget(self.R2, 2, 1, 1, 1)
        self.grid.addWidget(QLabel(u"需求资源R3：", parent=self), 3, 0, 1, 1)
        self.grid.addWidget(self.R3, 3, 1, 1, 1)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)  # 确定
        self.buttonBox.rejected.connect(self.reject)  # 取消
        self.layout.addLayout(self.grid)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        self.reject()  # 点击ok也退出窗口
        if self.name.text() == '' or self.R1.text() == '' or self.R2.text() == '' or self.R3.text() == '':  # 输入错误
            return ['','','','']
        return [self.name.text(), int(self.R1.text()), int(self.R2.text()), int(self.R3.text())]


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.grid = QGridLayout()  # 主体页面是网格布局
        self.hbox_top = QHBoxLayout()
        self.hbox_bottom = QHBoxLayout()
        self.label = QLabel("系统在T0时刻的资源分配表：")
        self.btm_exec = QPushButton("安全检查")
        self.btm_add = QPushButton("新增作业")
        self.btm_requ = QPushButton("请求资源")
        self.tabw = QTableWidget()
        self.row = 0  # 进程数
        self.initUI()
        self.resize(1200, 600)
        self.setWindowTitle("银行家算法")  # 设置窗口标题

    def initUI(self):
        '''初始化UI'''
        self.hbox_top.addWidget(self.label)  # 设置顶部内容
        self.hbox_top.addStretch(1)
        self.hbox_top.addWidget(self.btm_add)
        self.tabw.setColumnCount(4)  # 设置中间内容
        header = ["Process", "Allocation", "Need", "Avaliable"]
        self.tabw.setHorizontalHeaderLabels(header)
        self.hbox_bottom.addStretch(1)  # 设置底部内容
        self.hbox_bottom.addWidget(self.btm_exec)
        self.hbox_bottom.addWidget(self.btm_requ)
        self.hbox_bottom.addStretch(1)
        self.grid.addLayout(self.hbox_top, 1, 1)
        self.grid.addWidget(self.tabw, 2, 1)
        self.grid.addLayout(self.hbox_bottom, 3, 1)
        self.grid.setRowStretch(1, 10)  # 设置宽度比例
        self.grid.setRowStretch(2, 60)
        self.grid.setRowStretch(3, 60)
        self.setLayout(self.grid)
        self.analog_system = AnalogSystem()  # 创建模拟系统对象
        self.btm_add.clicked.connect(self.addTask)
        self.btm_exec.clicked.connect(self.check)
        self.btm_requ.clicked.connect(self.requResource)

    def addTask(self):
        '''增加进程，并自动初始化进程'''
        dialog = MulDialog()
        dialog.show()
        dialog.exec_()  # 程序进入消息循环，等待可能输入进行响应
        name, R1, R2, R3 = dialog.accept()
        if name == '' or R1 == '' or R2 == '' or R3 == '':  # 输入错误
            return
        p = Process()  # 创建新进程
        self.analog_system.processing.append(p)  # 系统把进程加进去
        p.setName(name)
        AvaResource = self.analog_system.randResource(
            p.setMax(R1, R2, R3))  # 系统给进程分配资源
        p.setAllocation(self.analog_system.returnGave())
        resource = p.returnResource()
        resource.append(AvaResource)
        self.tabw.insertRow(self.row)  # 槽函数，从i开始增加行
        for j in range(4):
            newItem = QTableWidgetItem(str(resource[j]))
            self.tabw.setItem(self.row, j, newItem)
        #self.tabw.setSpan(self.row,3,self.row+2,1) # 单元格值合并
        self.row += 1

    def check(self):
    	'''检查是否为安全序列'''
    	if self.analog_system.checkSafety():
    		k = []
    		for i in range(self.analog_system.counter):
    			k.append(self.analog_system.processing[i].name)
    		print("这是安全序列，安全序列为：",k)
    	else:
    		print("no")

    def requResource(self):
    	'''请求资源'''
    	dialog = MulDialog()
    	dialog.show()
    	dialog.exec_()  # 程序进入消息循环，等待可能输入进行响应
    	name, R1, R2, R3 = dialog.accept()
    	if name == '' or R1 == '' or R2 == '' or R3 == '':  # 输入错误
    	    return
    	for p in self.analog_system.processing:
    		if p.name == name:
    			break
    	status = self.analog_system.getResource(p,R1,R2,R3)
    	if status:
    		print("允许分配资源")
    	else:
    		print("请求资源失败")


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 每个PyQt5应用都必须创建一个应用对象
    MainWindows = MainWindow()
    MainWindows.show()
    sys.exit(app.exec_())
