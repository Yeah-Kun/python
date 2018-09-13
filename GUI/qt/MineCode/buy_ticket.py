'''操作系统实验一：线程锁问题
	create by Ian in 2017-10-24 17:28:07
'''

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QPixmap
import PyQt5.uic

ui_file = 'process_and_thread.ui'
(class_ui, class_basic_class) = PyQt5.uic.loadUiType(ui_file)

class Ticket():
	'''卖票类'''

	def __init__(self,number):
		# 生成4条线路，4个班次
		self.ticket = [([number]*4) for i in range(4)]

		self.city = ["深圳->广州","广州->深圳","广州->新会","新会->广州"]
		self.time = ["7:00","8:30","12:30","15:00"]
		self.frequency = ["2001","2002","2003","2004"]
		self.price = ["$35","$35","$35","$35"]
		self.title = ["班次","时间","剩票","价格"]
	

class Window(class_basic_class,class_ui):
	'''窗口类'''

	def __init__(self):
		super(Window,self).__init__()
		self.setupUi(self) # 加载

		# 初始化
		background = Ticket(40)
		self.TicketList = background.ticket
		self.CityList = background.city
		self.PriceList = background.price
		self.FrequencyList = background.frequency
		self.TimeList = background.time
		self.TitleList = background.title

		# 按照objectName加载控件
		self.textEdit.append("%s %s %s %s" %(self.TitleList[0],self.TitleList[1],self.TitleList[2],self.TitleList[3])) 
		for i in range(len(self.CityList)):
			self.textEdit.append("%s %s  %s  %s" %(self.FrequencyList[i],self.TimeList[i],self.TicketList[0][i],self.PriceList[i]))
		for i in self.CityList:
			self.comboBox.addItem(i)
		for i in self.FrequencyList:
			self.comboBox_2.addItem(i)
			self.comboBox_3.addItem(i)

		# 逻辑代码
		self.pushButton.clicked.connect(lambda:self.searchTicket())
		self.pushButton_2.clicked.connect(lambda:self.buyTicket(self.comboBox_2,self.lineEdit))
		self.pushButton_3.clicked.connect(lambda:self.buyTicket(self.comboBox_3,self.lineEdit_2))


	def searchTicket(self):
		'''设置文本框内容'''
		city = self.comboBox.currentIndex() 
		self.textEdit.setText("") # 清空文本框内容
		self.textEdit.append("%s %s %s %s" %(self.TitleList[0],self.TitleList[1],self.TitleList[2],self.TitleList[3])) 
		for i in range(len(self.CityList)):
			self.textEdit.append("%s %s  %s  %s" %(self.FrequencyList[i],self.TimeList[i],self.TicketList[city][i],self.PriceList[i]))

	def buyTicket(self,freq,button):
		'''买票操作'''
		choice = freq.currentIndex()
		city = self.comboBox.currentIndex() 
		amount = int(button.text()) # 获得单行文本框内容

		if amount <= self.TicketList[city][choice]:
			self.TicketList[city][choice] -= amount
			QMessageBox.about(self,"购票提示","成功购票！")
			self.searchTicket()

		else:
			QMessageBox.warning(self,"购票提示","车票数量不够，请重新购票！")
		



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv) # 每个PyQt5应用都必须创建一个应用对象
    MainWindow = Window()
    MainWindow.show()
    sys.exit(app.exec_())
