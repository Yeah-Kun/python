"""
	火箭系统截面模块
	create by Ian in 2018-6-10 17:33:05
"""

import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtGui import QDoubleValidator
from Calculate_ballistic import Rocket
from PyQt5.QtCore import QThread, pyqtSignal
import time

(form_main_class, qtbase_main_class) = uic.loadUiType('main.ui')
(form_b_class, qtbase_b_class) = uic.loadUiType('ballistic.ui')


class RocketMainWindow(form_main_class, qtbase_main_class):
    """docstring for RocketMainWindow
            火箭计算系统主界面
    """

    def __init__(self):
        super(RocketMainWindow, self).__init__()
        self.setupUi(self)
        self.ballAction.triggered.connect(self.new_ballistic)

    def new_ballistic(self):
        """创建弹道计算窗口
        """
        self.ball = BallisticWindow()
        self.ball.show()


class BallisticWindow(form_b_class, qtbase_b_class):
    """docstring for BallisticWindow
            弹道计算窗口
    """

    def __init__(self):
        super(BallisticWindow, self).__init__()
        self.setupUi(self)
        self.cal_obj = None  # 初始化设弹道计算类为None
        self.save_parm_switch = False

        self.check_parm_btn.clicked.connect(self.onclick_check_parm)
        self.save_parm_btn.clicked.connect(self.onclick_save_parm)
        self.simulation_btn.clicked.connect(self.onclick_simulation)
        self.predict_btn.clicked.connect(self.onclick_predict)
        self.load_parm_btn.clicked.connect(self.onclick_load_parm)

        # 设置文本框验证器
        line_type = QDoubleValidator(self)
        self.T_line.setValidator(line_type)
        self.m_line.setValidator(line_type)
        self.m_low_line.setValidator(line_type)
        self.launch_ang_line.setValidator(line_type)
        self.lacher_line.setValidator(line_type)
        self.V_w_line.setValidator(line_type)
        self.V_w_ang_line.setValidator(line_type)
        self.LM_line.setValidator(line_type)

    def onclick_check_parm(self):
        """检查参数，并进行相对应的模拟运算
        """
        T = self.T_line.text()
        m = self.m_line.text()
        m_low = self.m_low_line.text()
        lacher = self.lacher_line.text()
        launch_ang = self.launch_ang_line.text()
        V_w_ang = self.V_w_ang_line.text()
        V_w = self.V_w_line.text()
        L_M = self.LM_line.text()

        if len(T) and len(m) and len(m_low) and len(lacher) and len(launch_ang) and len(V_w_ang) and len(V_w) and len(L_M) == 0:
            print(len(T), len(m), len(m_low), len(lacher), len(
                launch_ang), len(V_w_ang), len(V_w), len(L_M))
            QMessageBox.warning(self, "警告", "有参数未填写！", QMessageBox.Ok)

        else:
            QMessageBox.information(self, "成功", "所有参数都没有问题！", QMessageBox.Ok)
            T = float(T)
            m = float(m)
            m_low = float(m_low)
            lacher = float(lacher)
            launch_ang = float(launch_ang)
            V_w_ang = float(V_w_ang)
            V_w = float(V_w)
            L_M = float(L_M)
            V_w_ang -= launch_ang  # 求风向角和发射角的夹角，顺时针为正

            self.ball_thread = BallisticThread(m, T, m_low, lacher, V_w_ang, V_w, L_M)
            
            self.save_parm_switch = True  # 设置开关


    def onclick_simulation(self):
        """模拟运行，获得0~90°俯仰角对应的落点参数
        """
        def simulation(signals):
            self.max_x = signals[0]
            self.min_x = signals[1]
            self.x_map = signals[2]
            self.max_x = round(self.max_x, 4)
            self.min_x = round(self.min_x, 4)
            s = str(self.min_x) + "~" + str(self.max_x)
            self.reach_line.setText(s)

        self.ball_thread.sinout.connect(simulation)
        self.ball_thread.start()


    def onclick_predict(self):
        """预测
        """
        x = float(self.tar_s.text())
        if x > self.max_x or x < self.min_x:
            QMessageBox.warning(self, "警告", "超出预测范围，无法预测",
                                QMessageBox.Yes | QMessageBox.No)
        else:
            temp = 10  # 预设落点值和预测值相差10
            index = 0
            for i in range(len(self.x_map)):
                if abs(self.x_map[i] - x) <= temp:
                    temp = abs(self.x_map[i] - x)
                    index = i

            self.pitch_line.setText(str(index))

    def onclick_save_parm(self):
        filename, filetypes = QFileDialog.getSaveFileName(
            self, "保存模型", "./", "All Files (*)")
        if filename != "":
            with open(filename, "w") as f:
                f.write(self.T_line.text())
                f.write("\n")
                f.write(self.m_line.text())
                f.write("\n")
                f.write(self.m_low_line.text())
                f.write("\n")
                f.write(self.lacher_line.text())
                f.write("\n")
                f.write(self.launch_ang_line.text())
                f.write("\n")
                f.write(self.V_w_ang_line.text())
                f.write("\n")
                f.write(self.V_w_line.text())
                f.write("\n")
                f.write(self.LM_line.text())


    def onclick_load_parm(self):
        """打开文件操作"""
        filename, filetypes = QFileDialog.getOpenFileName(
            self, "选取文件", "./", "Text Files (*.txt)")
        print(filename)

        if filename != None:
            if filetypes == "Text Files (*.txt)":
                with open(filename, "r") as f:
                    parm = f.read().splitlines()            
                    self.T_line.setText(parm[0])
                    self.m_line.setText(parm[1])
                    self.m_low_line.setText(parm[2])
                    self.lacher_line.setText(parm[3])
                    self.launch_ang_line.setText(parm[4])
                    self.V_w_ang_line.setText(parm[5])
                    self.V_w_line.setText(parm[6])
                    self.LM_line.setText(parm[7])
            else:
                print(filetypes)
                print("暂时无法读取这种格式的数据")
        return filename


class BallisticThread(QThread):
    """弹道计算的工作线程
    	多线程，分离UI线程和工作线程
    """
    sinout = pyqtSignal(object) # 信号

    def __init__(self, m, T, m_low, lacher, 
    	V_w_ang, V_w, L_M):

        super(BallisticThread, self).__init__()
        # 初始化火箭弹道参数
        self.cal_obj = Rocket(m=m, T=T, m_low=m_low, lacher=lacher,
        	V_w_ang=V_w_ang, V_w=V_w, L_M=L_M)
        self.cal_obj.normal() # 初始化设置


    def __del__(self):
        self.wait()


    def run(self):
    	"""业务逻辑
    	"""
    	max_x, min_x, x_map = self.cal_obj.stimulate()
    	self.sinout.emit([max_x, min_x, x_map])



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = RocketMainWindow()
    ui.show()
    sys.exit(app.exec_())
