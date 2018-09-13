'''
	模拟处理机调度算法2.0
	update：重写代码，使用继承和多态
	create by Ian in 2017-11-17 19:34:13
'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import time


class MulDialog(QDialog):
    '''新建作业弹窗，自定义对话框'''

    def __init__(self):
        super().__init__()
        self.setWindowTitle(u"新建作业")
        self.resize(100, 80)
        self.grid = QGridLayout()
        self.name = QLineEdit()
        self.lenth = QLineEdit()
        self.buttonBox = QDialogButtonBox()
        self.layout = QVBoxLayout()
        self.initUI()

    def initUI(self):
        '''初始化UI'''
        self.grid.addWidget(QLabel(u"作业名：", parent=self), 0, 0, 1, 1)
        self.grid.addWidget(self.name, 0, 1, 1, 1)
        self.grid.addWidget(QLabel(u"作业长度：", parent=self), 1, 0, 1, 1)
        self.grid.addWidget(self.lenth, 1, 1, 1, 1)
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
        return [self.name.text(), self.lenth.text()]


class DialogPS(MulDialog):
    '''优先级调度算法定制弹窗'''

    def __init__(self):
        super().__init__()

    def initUI(self):
        '''初始化UI'''
        self.prior = QLineEdit()
        self.grid.addWidget(QLabel(u"作业名：", parent=self),
                            0, 0, 1, 1)  # 控件，行，列，行宽，列宽
        self.grid.addWidget(self.name, 0, 1, 1, 1)
        self.grid.addWidget(QLabel(u"作业长度：", parent=self), 1, 0, 1, 1)
        self.grid.addWidget(self.lenth, 1, 1, 1, 1)
        self.grid.addWidget(QLabel(u"优先级：", parent=self), 2, 0, 1, 1)
        self.grid.addWidget(self.prior, 2, 1, 1, 1)
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
        return [self.name.text(), self.lenth.text(), self.prior.text()]

class DialogHRRF(MulDialog):
	'''高响应比调度算法定制弹窗'''

	def __init__(self):
	    super().__init__()

	def initUI(self):
	    '''初始化UI'''
	    self.grid.addWidget(QLabel(u"作业名：", parent=self),
	                        0, 0, 1, 1)  # 控件，行，列，行宽，列宽
	    self.grid.addWidget(self.name, 0, 1, 1, 1)
	    self.grid.addWidget(QLabel(u"要求服务时间：", parent=self), 1, 0, 1, 1)
	    self.grid.addWidget(self.lenth, 1, 1, 1, 1)
	    self.buttonBox.setOrientation(Qt.Horizontal)
	    self.buttonBox.setStandardButtons(
	        QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
	    self.buttonBox.accepted.connect(self.accept)  # 确定
	    self.buttonBox.rejected.connect(self.reject)  # 取消
	    self.layout.addLayout(self.grid)
	    self.layout.addWidget(self.buttonBox)
	    self.setLayout(self.layout)


class TaskRR(list):
    '''作业的具体内容，时间片算法'''

    def __init__(self):
        super().__init__()
        # 初始化作业内容
        self.taskName = []  # 作业名
        self.taskStatus = []  # 作业状态
        self.lenth = []  # 长度
        self.schedule = []  # 进度
        self.completion = []  # 完成率
        self.task = []  # 作业列表
        self.counter = 0

    def addTask(self, taskName, lenth):
        '''增加作业'''
        self.counter += 1
        self.taskName.append(taskName)
        self.lenth.append(int(lenth))
        if (len(self.taskStatus) == 0):
            self.taskStatus.append(1)  # 就绪状态为0，运行态为1，阻塞态为-1
        else:
            self.taskStatus.append(0)
        self.schedule.append(0)  # 最开始进度为0
        self.completion.append(0)

    def showAll(self):
        '''单个作业的所有内容'''
        self.task = zip(self.taskName, self.taskStatus,
                        self.lenth, self.schedule, self.completion)
        return self.task

    def len(self):
        '''作业的总数'''
        return self.counter

    def show(self):
        '''展现当前新建的作业内容(也是最后一个作业)'''
        i = self.counter - 1
        self.task = list(self.showAll())
        return self.task[i]

    def run(self):
        '''执行算法'''
        for i in range(self.counter):
            print(self.taskName[i], self.taskStatus[i],
                  self.lenth[i], self.schedule[i], self.completion[i])
            if self.taskStatus[i] == 1:
                self.schedule[i] += 1  # 进度值+1
                # 完成率
                self.completion[i] = "%d/%d" % (self.schedule[i],
                                                self.lenth[i])
                self.taskStatus[i] = 0  # 状态值设为0
                if i + 1 < self.counter:
                    # 设置下一个任务的状态值，这里有个不好的设计，状态设置在了独立的list里
                    self.taskStatus[i + 1] = 1
                else:
                    self.taskStatus[0] = 1
                break
        for i in range(self.counter):
            if i >= self.counter:  # 由于counter会修改，所以会出现i大于counter的情况
                break
            if self.schedule[i] == self.lenth[i]:  # 进度值达到最大
                print("删除%d" % i)
                del self.taskName[i]
                del self.taskStatus[i]
                del self.lenth[i]
                del self.schedule[i]
                del self.completion[i]
                self.counter -= 1


class TaskPS(TaskRR):
    '''作业的具体内容，优先级调度算法'''

    def __init__(self):
        super().__init__()
        self.prior = []  # 优先级

    def addTask(self, taskName, lenth, prior):
        '''增加作业'''
        self.counter += 1
        self.taskName.append(taskName)
        self.lenth.append(int(lenth))
        if (self.counter - 1 == 0):
            self.taskStatus.append(1)  # 就绪状态为0，运行态为1，阻塞态为-1
        else:
            self.taskStatus.append(0)
        self.prior.append(int(prior))
        self.schedule.append(0)  # 最开始进度为0
        i = self.counter - 1
        self.completion.append("%d/%d" % (self.schedule[i], self.lenth[i]))

    def showAll(self):
        '''作业的所有内容'''
        self.complete()
        self.task = zip(self.taskName, self.taskStatus,
                        self.lenth, self.prior, self.schedule, self.completion)
        return self.task

    def run(self):
        '''执行算法'''
        i = self.prior.index(max(self.prior))  # 最高优先级索引
        self.taskStatus[i] = 1
        self.schedule[i] += 1
        if self.schedule[i] == self.lenth[i]:  # 进度值达到最大
            print("删除%d" % i)
            del self.taskName[i]
            del self.taskStatus[i]
            del self.lenth[i]
            del self.schedule[i]
            del self.completion[i]
            del self.prior[i]
            self.counter -= 1

    def complete(self):
    	for i in range(self.counter):
    		self.completion[i] = ("%d/%d" % (self.schedule[i], self.lenth[i]))
    	return self.completion


class TaskHRRF(TaskPS):
	'''作业的具体内容，优先级调度算法'''

	def __init__(self):
	    super().__init__()
	    self.response = []  # 响应比
	    self.wait = [] # 等待时间

	def addTask(self, taskName, lenth):
	    '''增加作业'''
	    self.counter += 1
	    i = self.counter - 1
	    self.taskName.append(taskName)
	    self.lenth.append(int(lenth))
	    self.taskStatus.append(0) # 就绪状态为0，运行态为1，阻塞态为-1
	    self.schedule.append(0)  # 最开始进度为0
	    self.wait.append(0) # 等待时间最初为0
	    self.response.append(1+self.wait[i]/self.lenth[i])
	    self.completion.append("%d/%d" % (self.schedule[i], self.lenth[i]))

	def showAll(self):
	    '''作业的所有内容'''
	    self.complete()
	    self.task = zip(self.taskName, self.taskStatus,
	                    self.lenth, self.response, self.schedule, self.completion)
	    return self.task

	def respond(self):
		'''计算所有任务的响应比'''
		for i in range(self.counter):
			self.response[i] = ("%.2f"  %(1 + self.wait[i]/self.lenth[i]))

	def run(self):
		'''执行算法'''
		self.respond()
		i = self.response.index(max(self.response))  # 最高响应比索引
		self.taskStatus[i] = 1
		self.schedule[i] += 1
		for j in range(self.counter):
			if j != i:
				self.wait[j] += 1

		if self.schedule[i] == self.lenth[i]:  # 进度值达到最大
		    print("删除%d" % i)
		    del self.taskName[i]
		    del self.taskStatus[i]
		    del self.lenth[i]
		    del self.schedule[i]
		    del self.completion[i]
		    del self.response[i]
		    self.counter -= 1




class UIRR(QWidget):
    '''时间片算法的界面'''

    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()  # 主体页面是网格布局
        self.hbox = QHBoxLayout()  # 水平布局，囊括基本的控件和提示语
        self.labl = QLabel()
        self.newTask = QPushButton("新建作业")
        self.btn = QPushButton("开始作业")
        self.split = QSplitter(Qt.Horizontal)
        self.tabw = QTableWidget()
        self.timer = QBasicTimer()
        self.labl.setText("每个作业的长度都为50~100间的随机值")
        self.hbox.addWidget(self.newTask)
        self.hbox.addWidget(self.labl)
        self.hbox.addStretch()  # 增加弹性布局，把空间都压缩在右边
        self.hbox.addWidget(self.btn)
        self.task = TaskRR()
        self.row = 0  # 记录数据的行数
        self.initUI()

    def initUI(self):
        '''初始化UI'''
        self.tabw.setColumnCount(5)
        horizontalHeader = ["作业名", "作业状态", "作业长度", "进度", "完成率"]
        self.tabw.setHorizontalHeaderLabels(horizontalHeader)
        self.split.addWidget(self.tabw)
        self.grid.addLayout(self.hbox, 1, 1)
        self.grid.addWidget(self.split, 2, 1)
        self.grid.setRowStretch(1, 10)  # 设置宽度比例
        self.grid.setRowStretch(2, 90)
        self.setLayout(self.grid)
        self.newTask.clicked.connect(self.addTask)
        self.btn.clicked.connect(self.doAction)

    def addTask(self):
        '''新增作业'''
        dialog = MulDialog()
        dialog.show()
        dialog.exec_()  # 程序进入消息循环，等待可能输入进行响应
        self.taskname, self.lenth = dialog.accept()
        if self.lenth == '':  # 输入错误
            return
        self.task.addTask(self.taskname, self.lenth)  # 新增任务
        task = self.task.show()
        j = 0
        self.tabw.insertRow(self.row)  # 槽函数，从i开始增加行
        for item in task:
            if j == 3:
                self.qpr = QProgressBar()
                self.qpr.setValue(int(item))
                self.tabw.setCellWidget(self.row, j, self.qpr)
            else:
                # 将其他对象转换为QTableWidgetItem对象
                newItem = QTableWidgetItem(str(item))
                self.tabw.setItem(self.row, j, newItem)
            j += 1
        self.row += 1

    def updateUI(self):
        '''更新界面内容'''
        self.tabw.clearContents()  # 清除表头以外的所有信息
        task = self.task.showAll()
        self.i = 0
        for one in task:
            one = list(one)
            j = 0
            for item in one:
                if j == 3:
                    self.qpr = QProgressBar()
                    self.qpr.setValue(int(item / one[2] * 100))  # 进度条值
                    self.tabw.setCellWidget(self.i, j, self.qpr)
                else:
                    # 将其他对象转换为QTableWidgetItem对象
                    newItem = QTableWidgetItem(str(item))
                    self.tabw.setItem(self.i, j, newItem)
                j += 1
            self.i += 1

    def doAction(self):
        '''开始作业事件'''
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText("开始作业")
        else:
            self.timer.start(100, self)  # 每100ms启动一次计时器
            self.btn.setText("停止作业")

    def timerEvent(self, e):
        '''时间触发事件，还有进程为空没有写'''
        if self.task.len() == 0:
            self.btn.setText('作业已完成')
            return
        else:
            self.task.run()
            self.updateUI()


class UIPS(UIRR):
    '''优先级调度算法界面'''

    def __init__(self):
        super().__init__()

    def initUI(self):
        '''初始化UI'''
        self.tabw.setColumnCount(6)
        horizontalHeader = ["作业名", "作业状态", "作业长度", "作业优先级", "进度", "完成率"]
        self.tabw.setHorizontalHeaderLabels(horizontalHeader)
        self.split.addWidget(self.tabw)
        self.grid.addLayout(self.hbox, 1, 1)
        self.grid.addWidget(self.split, 2, 1)
        self.grid.setRowStretch(1, 10)  # 设置长度比例
        self.grid.setRowStretch(2, 90)
        self.setLayout(self.grid)
        self.task = TaskPS()
        self.newTask.clicked.connect(self.addTask)
        self.btn.clicked.connect(self.doAction)

    def addTask(self):
        '''新增作业'''
        dialog = DialogPS()
        dialog.show()
        dialog.exec_()  # 程序进入消息循环，等待可能输入进行响应
        self.taskname, self.lenth, self.prior = dialog.accept()
        if self.taskname == '' or self.lenth == '' or self.prior == '':  # 输入错误
            return
        self.task.addTask(self.taskname, self.lenth, self.prior)  # 新增任务
        task = self.task.show()
        j = 0
        self.tabw.insertRow(self.row)  # 槽函数，从i开始增加行
        for item in task:
            if j == 4:
                self.qpr = QProgressBar()
                self.qpr.setValue(int(item))
                self.tabw.setCellWidget(self.row, j, self.qpr)
            else:
                # 将其他对象转换为QTableWidgetItem对象
                newItem = QTableWidgetItem(str(item))
                self.tabw.setItem(self.row, j, newItem)
            j += 1
        self.row += 1

    def updateUI(self):
        '''更新界面内容'''
        self.tabw.clearContents()  # 清除表头以外的所有信息
        task = self.task.showAll()
        self.row = 0
        for one in task:
            one = list(one)
            j = 0
            for item in one:
                if j == 4:
                    self.qpr = QProgressBar()
                    self.qpr.setValue(int(item / one[2] * 100))  # 进度条值
                    self.tabw.setCellWidget(self.row, j, self.qpr)
                else:
                    # 将其他对象转换为QTableWidgetItem对象
                    newItem = QTableWidgetItem(str(item))
                    self.tabw.setItem(self.row, j, newItem)
                j += 1
            self.row += 1


class UIHRRF(UIRR):
    '''高响应比调度算法界面'''

    def __init__(self):
        super(UIHRRF, self).__init__()

    def initUI(self):
        '''初始化UI'''
        self.tabw.setColumnCount(6)
        horizontalHeader = ["作业名", "作业状态", "作业长度", "作业响应比", "进度", "完成率"]
        self.tabw.setHorizontalHeaderLabels(horizontalHeader)
        self.split.addWidget(self.tabw)
        self.grid.addLayout(self.hbox, 1, 1)
        self.grid.addWidget(self.split, 2, 1)
        self.grid.setRowStretch(1, 10)  # 设置长度比例
        self.grid.setRowStretch(2, 90)
        self.setLayout(self.grid)
        self.task = TaskHRRF()
        self.newTask.clicked.connect(self.addTask)
        self.btn.clicked.connect(self.doAction)

    def addTask(self):
        '''新增作业'''
        dialog = DialogHRRF()
        dialog.show()
        dialog.exec_()  # 程序进入消息循环，等待可能输入进行响应
        self.taskname, self.lenth = dialog.accept()
        if self.taskname == '' or self.lenth == '':  # 输入错误
            return
        self.task.addTask(self.taskname, self.lenth)  # 新增任务
        task = self.task.show()
        j = 0
        self.tabw.insertRow(self.row)  # 槽函数，从i开始增加行
        for item in task:
            if j == 4:
                self.qpr = QProgressBar()
                self.qpr.setValue(int(item))
                self.tabw.setCellWidget(self.row, j, self.qpr)
            if j == 3:
            	newItem = QTableWidgetItem(str(item*100) + "%")
            	self.tabw.setItem(self.row, j, newItem)
            else:
                # 将其他对象转换为QTableWidgetItem对象
                newItem = QTableWidgetItem(str(item))
                self.tabw.setItem(self.row, j, newItem)
            j += 1
        self.row += 1

    def updateUI(self):
        '''更新界面内容'''
        self.tabw.clearContents()  # 清除表头以外的所有信息
        task = self.task.showAll()
        self.row = 0
        for one in task:
            one = list(one)
            j = 0
            for item in one:
                if j == 4:
                    self.qpr = QProgressBar()
                    self.qpr.setValue(int(item / one[2] * 100))  # 进度条值
                    self.tabw.setCellWidget(self.row, j, self.qpr)
                if j == 3:
                    newItem = QTableWidgetItem(str(float(item)*100) + "%")
                    self.tabw.setItem(self.row, j, newItem)
                else:
                    # 将其他对象转换为QTableWidgetItem对象
                    newItem = QTableWidgetItem(str(item))
                    self.tabw.setItem(self.row, j, newItem)
                j += 1
            self.row += 1


class Window(QTabWidget):
    '''主窗口'''

    def __init__(self):
        super(Window, self).__init__()
        self.RR = UIRR()
        self.PS = UIPS()
        self.HRRF = UIHRRF()
        self.initUI()
        self.resize(1200, 600)
        self.setWindowTitle("处理机调度算法") # 设置窗口标题

    def initUI(self):
        '''初始化UI'''
        self.addTab(self.RR, u"时间片轮转")
        self.addTab(self.PS, u"动态优先调度")
        self.addTab(self.HRRF, u"高响应比优先调度")


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 每个PyQt5应用都必须创建一个应用对象
    MainWindow = Window()
    MainWindow.show()
    sys.exit(app.exec_())
