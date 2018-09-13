'''操作系统实验一：线程锁问题
	create by Ian in 2017-10-24 17:28:07
'''

from PyQt5.QtCore import QThread, QMutex
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QPixmap
import PyQt5.uic
from time import sleep
import random
import threading

ui_file = 'process_and_thread.ui'
(class_ui, class_basic_class) = PyQt5.uic.loadUiType(ui_file)


class Window(class_basic_class, class_ui):
    '''窗口类'''

    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)  # 加载
        self.n = 0  # 线程计数器

        # 按照objectName加载控件
        self.textEdit.append("%s %s %s %s" %
                             (title[0], title[1], title[2], title[3]))
        for i in range(len(city)):
            self.textEdit.append("%s %s  %s  %s" % (
                frequency[i], time[i], ticket[0][i], price[i]))
        for i in city:
            self.comboBox.addItem(i)
        for i in frequency:
            self.comboBox_2.addItem(i)
            self.comboBox_3.addItem(i)

        # 逻辑代码
        self.pushButton.clicked.connect(lambda: self.searchTicket())
        self.pushButton_2.clicked.connect(
            lambda: self.startBuy(self.comboBox_2, self.lineEdit))
        self.pushButton_3.clicked.connect(
            lambda: self.startBuy(self.comboBox_3, self.lineEdit_2))

    def searchTicket(self):
        '''设置文本框内容'''
        cityIndex = self.comboBox.currentIndex()
        self.textEdit.setText("")  # 清空文本框内容
        self.textEdit.append("%s %s %s %s" %
                             (title[0], title[1], title[2], title[3]))
        for i in range(len(city)):
            self.textEdit.append("%s %s  %s  %s" % (
                frequency[i], time[i], ticket[cityIndex][i], price[i]))

    def startBuy(self, freq, button):
        cityIndex = self.comboBox.currentIndex()
        freqIndex = freq.currentIndex()
        amount = int(button.text()) # 获得单行文本框内容
        self.n += 1
        self.thread = MyThread(self.n, cityIndex, freqIndex, amount, self)
        self.thread.start()
        self.searchTicket()


class MyThread(QThread):
    """线程定义"""
    def __init__(self, n, cityIndex, freqIndex, amount, parent=None):
        super(MyThread, self).__init__(parent)
        self.n = n
        self.cityIndex = cityIndex
        self.freqIndex = freqIndex
        self.amount = amount

    def run(self):
        '''买票操作'''
        mutex = threading.Lock() # 建立锁对象
        mutex.acquire() # 获得锁
        #sleep(random.randint(60,61))
        print(self.cityIndex,self.freqIndex)
        if ticket[self.cityIndex][self.freqIndex] >= self.amount:
        	ticket[self.cityIndex][self.freqIndex] -= self.amount
        else:
        	print("no ticket!")
        print("Thread", self.n)
        mutex.release()


if __name__ == '__main__':
    import sys
    ticket = [([40] * 4) for i in range(4)]  # 生成4条线路，4个班次
    city = ["深圳->广州", "广州->深圳", "广州->新会", "新会->广州"]
    time = ["7:00", "8:30", "12:30", "15:00"]
    frequency = ["2001", "2002", "2003", "2004"]
    price = ["$35", "$35", "$35", "$35"]
    title = ["班次", "时间", "剩票", "价格"]
    app = QApplication(sys.argv)  # 每个PyQt5应用都必须创建一个应用对象
    MainWindow = Window()
    MainWindow.show()
    sys.exit(app.exec_())
