#-*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QCheckBox, QPushButton, QHeaderView
from PyQt5.QtGui import QPixmap
import PyQt5.uic

ui_file = 'Demo5.ui'
(class_ui, class_basic_class) = PyQt5.uic.loadUiType(ui_file)


class Mzitu():

    def __init__(self, url):
        self.url = url
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                   'Host': 'www.mzitu.com'}
        response = requests.get(self.url, headers=headers)
        content = BeautifulSoup(response.text, 'lxml')
        linkblock = content.find('div', class_="postlist")
        self.linklist = linkblock.find_all('li')

    def printli(self):
        linklist = self.linklist
        linksum = list()

        for link in linklist:
            url = link.a.get('href')
            picurl = link.img.get('data-original')
            linkid = re.search(r'(\d+)', url).group()
            firstspan = link.span
            titleword = firstspan.get_text()
            secondspan = firstspan.find_next_sibling('span')
            uploadtime = secondspan.get_text()
            thirdspan = secondspan.find_next_sibling('span')
            viewcount = thirdspan.get_text()
            linksum.append((linkid, titleword, uploadtime, viewcount, picurl))
        return linksum


class Window(class_basic_class, class_ui):
    '''窗口类'''
    def __init__(self):
        super(Window, self).__init__() 
        self.url = "http://www.mzitu.com/"
        self.setupUi(self)
        totlist = Mzitu(self.url).printli() # 创建Mzitu类，打印出列表
        
        self.tableWidget.setRowCount(len(totlist))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setColumnWidth(0, 435)
        verticalHeader = self.tableWidget.verticalHeader()
        verticalHeader.setSectionResizeMode(QHeaderView.Fixed)
        verticalHeader.setDefaultSectionSize(30)
        self.textBrowser.setOpenExternalLinks(True)  ##隐藏列表头
        self.page = 1  ##设定初始的页面数，为后面做翻页器做准备
        self.label_pagenum.setNum(self.page)  
        self.checkBoxs = [self._addCheckbox(index, item[0], item[1]) for index, item in enumerate(totlist)]
        self.pushButtons = [self._addpushButtonpic(index, item[0], item[4]) for index, item in enumerate(totlist)]
        self.pushButton.clicked.connect(self.getSelList)
        self.pushButton.setObjectName("显示网址")
        self.pushButton_nextpage.clicked.connect(lambda: self._nextPage(1))
        self.pushButton_uppage.clicked.connect(lambda: self._nextPage(-1))

    def _addCheckbox(self, index, idd, boxtitle):
        '''生成相应的位置'''
        checkBox = QCheckBox()
        checkBox.setObjectName(idd)
        checkBox.setText(boxtitle)
        self.tableWidget.setCellWidget(index, 0, checkBox) ##setCellWidget前面两个数字分别代表行和列，最后是需要关联的元素
        return checkBox

    def getSelList(self):
        selList = [(item.objectName(), item.text()) for item in self.checkBoxs if item.isChecked() == True]
        for item in selList:
            url = 'http://www.mzitu.com/'+item[0]
            self.textBrowser.append(item[1])
            self.textBrowser.append('<a href = %s>%s</a>' % (url, url))  ##此处输出超级链接
        return selList

    def _addpushButtonpic(self, index, idd, href):
            pushButton = QPushButton()
            pushButton.setObjectName(idd)
            pushButton.setText(idd)
            self.tableWidget.setCellWidget(index, 1, pushButton)
            pushButton.clicked.connect(lambda: self._showpic(idd, href))
            return pushButton

    def _showpic(self, idd, href):
        pic = requests.get(href).content
        pixmap = QPixmap()
        pixmap.loadFromData(pic)
        self.label.setPixmap(pixmap)

    def _nextPage(self, page):
        self.page += page
        self.label_pagenum.setNum(self.page)
        url = self.url + '/page/' + str(self.page)
        totlist = Mzitu(url).printli()
        newcheckBoxs = []
        newpushButtons = []
        for index, item in enumerate(totlist):
            newcheckbox = self._addCheckbox(index, item[0], item[1])
            newpushbutton = self._addpushButtonpic(index, item[0], item[4])
            newcheckBoxs.append(newcheckbox)
            newpushButtons.append(newpushbutton)
        self.checkBoxs = newcheckBoxs
        self.pushButtons = newpushButtons

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    MainWindow = Window()
    MainWindow.show()
    sys.exit(app.exec_())
