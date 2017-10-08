import sys, requests
from PyQt5 import QtGui, uic, QtWidgets

(form_class, qtbase_class) = uic.loadUiType('Demo3.ui')

class MainWindow(qtbase_class, form_class):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self._showpic)

    def _showpic(self):
        url = 'http://i.meizitu.net/thumbs/2017/04/90448_18b47_236.jpg'   ##图片链接
        pic = requests.get(url).content  ##获取图片链接的数据
        pixmap = QtGui.QPixmap()  ##新建一个QPixmap的类
        pixmap.loadFromData(pic)  ##pixmap加载图片数据
        self.label.setPixmap(pixmap)  ##最终在label上显示

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())