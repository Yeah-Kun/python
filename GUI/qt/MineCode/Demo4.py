'''根据select.ui重新设置ui
    made by Ian in 2017-10-7 22:36:46

'''
import sys
from PyQt5 import uic, QtWidgets

(form_class, qtbase_class) = uic.loadUiType('select.ui')

class MainWindow(qtbase_class, form_class):
    def __init__(self):
        super(MainWindow, self).__init__() # 重载父类的方法
        self.setupUi(self)
        strings = self.randomalpha()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(len(strings))
        self.checkboxs = [self._addcheckbox(alpha, i) for i, alpha in enumerate(strings)]
        self.pushButton.clicked.connect(self._printchecked)

    def randomalpha(self):
        import random, string
        return [random.choice(string.ascii_lowercase) for i in range(10)]

    def _addcheckbox(self, alpha, i):
        checkbox = QtWidgets.QCheckBox(self.centralwidget)
        checkbox.setObjectName(alpha)
        checkbox.setText(alpha)
        self.tableWidget.setCellWidget(i,0, checkbox)
        return checkbox

    def _printchecked(self):
        printalpha = [cb.objectName() for cb in self.checkboxs if cb.isChecked() == True]
        [self.textBrowser.append(alpha) for alpha in printalpha]

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())