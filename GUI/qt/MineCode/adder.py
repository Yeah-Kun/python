'''qt做的加法器
made by Ian in 2017-10-1 12:48:10
'''
import sys
from PyQt5 import uic, QtWidgets

(form_class, qtbase_class) = uic.loadUiType('adder.ui')


class MainWindow(form_class, qtbase_class):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.addfunction)

    def addfunction(self):
        a = float(self.textEdit.toPlainText())
        b = float(self.textEdit_2.toPlainText())
        c = a + b
        self.textEdit_3.setText(str(c))
        self.textBrowser.append("%.2f + %.2f = %.2f" % (a, b, c))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
