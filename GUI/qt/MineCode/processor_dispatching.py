'''
	模拟处理机调度算法
	create by Ian in 2017-11-9 19:28:46
'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import time


class MultiInPutDialog(QDialog):
    '''新建作业弹窗，自定义对话框'''

    def __init__(self):
        super(MultiInPutDialog, self).__init__()
        self.initUI()

    def initUI(self):
        '''初始化UI'''
        self.setWindowTitle(u"新建作业")
        self.resize(100, 80)
        grid = QGridLayout()
        grid.addWidget(QLabel(u"作业名：", parent=self), 0, 0, 1, 1)
        self.name = QLineEdit()
        grid.addWidget(self.name, 0, 1, 1, 1)
        grid.addWidget(QLabel(u"作业长度：", parent=self), 1, 0, 1, 1)
        self.lenth = QLineEdit()
        grid.addWidget(self.lenth, 1, 1, 1, 1)
        buttonBox = QDialogButtonBox()
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)  # 确定
        buttonBox.rejected.connect(self.reject)  # 取消
        layout = QVBoxLayout()
        layout.addLayout(grid)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

    def accept(self):
        self.reject()  # 点击ok也退出窗口
        return [self.name.text(), self.lenth.text()]


class TaskContant(list):
    '''作业的具体内容，时间片算法'''
    def __init__(self):
        super(TaskContant, self).__init__()
        # 初始化作业内容
        self.taskName = []  # 作业名
        self.taskStatus = []  # 作业状态
        self.lenth = []  # 长度
        self.schedule = []  # 进度
        self.completion = []  # 完成率
        self.priority = []  # 优先级
        self.response = []  # 响应比
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
            print(self.taskName[i], self.taskStatus[i],self.lenth[i], self.schedule[i], self.completion[i])
            if self.taskStatus[i] == 1:
                self.schedule[i] += 1 # 进度值+1
                self.completion[i] = "%d/%d" %(self.schedule[i],self.lenth[i])  # 完成率
                self.taskStatus[i] = 0 # 状态值设为0
                if i+1 < self.counter:
                    # 设置下一个任务的状态值，这里有个不好的设计，状态设置在了独立的list里
                    self.taskStatus[i+1] = 1
                else: 
                    self.taskStatus[0] = 1
                break
        for i in range(self.counter):
            if i >= self.counter: # 由于counter会修改，所以会出现i大于counter的情况
                break
            if self.schedule[i] == self.lenth[i]: # 进度值达到最大
                print("删除%d" %i)
                del self.taskName[i]
                del self.taskStatus[i]
                del self.lenth[i]
                del self.schedule[i]
                del self.completion[i]
                self.counter -= 1

class TaskPS(TaskContant):
	'''作业的内容，动态优先级调度'''
	def __init__(self):
		super().__init__()

	def addTask(self, taskName, lenth=100, priority=0):
	    '''增加作业'''
	    super().addTask()
	    self.priority.append(priority)


class Window(QTabWidget):
    '''主窗口'''

    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        '''初始化UI'''
        self.tab_RR = QWidget()  # 时间片轮转
        self.tab_PS = QWidget()  # 动态优先调度
        self.tab_HRRF = QWidget()  # 高响应比优先调度
        self.addTab(self.tab_RR, u"时间片轮转")
        self.addTab(self.tab_PS, u"动态优先调度")
        self.addTab(self.tab_HRRF, u"高响应比优先调度")
        self.tab_RR.tabw = QTableWidget()
        self.resize(1200, 600)
        self.task = TaskContant()
        self.tab_RRUI()
        self.i = 0
        task = []  # 临时容器i,测试用

    def tab_RRUI(self):
        '''时间片轮转容器内部代码'''
        # 初始化各种组件
        hbox = QHBoxLayout()
        grid = QGridLayout()
        split = QSplitter(Qt.Horizontal)
        labl = QLabel()

        labl.setText("每个作业的长度都为50~100间的随机值")
        newTask = QPushButton("新建作业")
        hbox.addWidget(newTask)
        hbox.addWidget(labl)
        hbox.addStretch()  # 增加弹性布局，把空间都压缩在右边
        self.btn = QPushButton("开始作业", self)
        self.btn.clicked.connect(self.doAction)
        self.timer = QBasicTimer()
        hbox.addWidget(self.btn)
        

        self.tab_RR.tabw.setColumnCount(5)
        horizontalHeader = ["作业名", "作业状态", "作业长度", "进度", "完成率"]
        self.tab_RR.tabw.setHorizontalHeaderLabels(horizontalHeader)
        # self.tab_RR.tabw.resizeRowsToContents() # 自动调整单元格的大小
        split.addWidget(self.tab_RR.tabw)
        grid.addLayout(hbox, 1, 1)
        grid.addWidget(split, 2, 1)
        grid.setRowStretch(1, 10)
        grid.setRowStretch(2, 90)
        self.tab_RR.setLayout(grid)
        newTask.clicked.connect(self.addTask)

    def addTask(self):
        '''新增作业'''
        dialog = MultiInPutDialog()
        dialog.show()
        dialog.exec_()  # 程序进入消息循环，等待可能输入进行响应
        self.taskname, self.lenth = dialog.accept()
        if self.lenth == '': # 输入错误
            return
        self.task.addTask(self.taskname,self.lenth)  # 新增任务
        task = self.task.show()
        j = 0
        self.tab_RR.tabw.insertRow(self.i)  # 槽函数，从i开始增加行
        for item in task:
            if j == 3:
                self.qpr = QProgressBar()
                self.qpr.setValue(int(item))
                self.tab_RR.tabw.setCellWidget(self.i,j,self.qpr)
            else:
                newItem = QTableWidgetItem(str(item))  # 将其他对象转换为QTableWidgetItem对象
                self.tab_RR.tabw.setItem(self.i, j, newItem)
            j += 1
        self.i += 1

    def updateUI(self):
        '''更新界面内容'''
        self.tab_RR.tabw.clearContents() # 清除表头以外的所有信息
        task = self.task.showAll()
        self.i = 0
        for one in task:
            one = list(one)
            j = 0
            for item in one:
                if j == 3:
                    self.qpr = QProgressBar()
                    self.qpr.setValue(int(item/one[2]*100))
                    self.tab_RR.tabw.setCellWidget(self.i,j,self.qpr)
                else:
                    newItem = QTableWidgetItem(str(item))  # 将其他对象转换为QTableWidgetItem对象
                    self.tab_RR.tabw.setItem(self.i, j, newItem)
                j += 1
            self.i += 1
    
    def doAction(self):
        '''开始作业事件'''
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText("开始作业")
        else:
            self.timer.start(100, self) # 每100ms启动一次计时器
            self.btn.setText("停止作业")

    def timerEvent(self,e):
        '''时间触发事件，还有进程为空没有写'''
        if self.task.counter == 0:
            self.btn.setText('作业已完成')
            return
        else:
            self.task.run()
            self.updateUI()




if __name__ == '__main__':
    app = QApplication(sys.argv)  # 每个PyQt5应用都必须创建一个应用对象
    MainWindow = Window()
    MainWindow.show()
    sys.exit(app.exec_())
