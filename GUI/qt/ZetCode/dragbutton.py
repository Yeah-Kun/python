#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this program, we can press on a button with a left mouse
click or drag and drop the button with  the right mouse click. 

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

from PyQt5.QtWidgets import QPushButton, QWidget, QApplication
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
import sys

class Button(QPushButton):
    '''按钮类，重构鼠标移动和鼠标点击事件'''

    def __init__(self, title, parent):
        super().__init__(title, parent)


    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.RightButton: # 只操作右键事件
            return

        mimeData = QMimeData()

        drag = QDrag(self)  # 创建一个QDrag对象，用来传输MIME-based数据
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)


    def mousePressEvent(self, e):

        super().mousePressEvent(e)

        if e.button() == Qt.LeftButton:
            print('press')


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.setAcceptDrops(True)

        self.button = Button('Button', self)
        self.button.move(100, 65)

        self.setWindowTitle('Click or Move')
        self.setGeometry(300, 300, 280, 150)


    def dragEnterEvent(self, e):

        e.accept()


    def dropEvent(self, e):

        position = e.pos()
        self.button.move(position)

        e.setDropAction(Qt.MoveAction)
        e.accept()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()