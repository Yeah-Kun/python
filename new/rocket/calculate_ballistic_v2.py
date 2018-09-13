"""
	弹道预测2.0程序
	create by Ian in 2018-6-10 16:13:14

	输入：
		T：发动机工作时间
		launch_angle：发射方位角，箭体坐标系的X坐标
		azimuth：风向方位角，以正北为0°
		V_w_ang：发射角与风向角的夹角
		V_w：实测风速
		tar_S：目标距离
		C_D：阻力系数
		C_Y：升力系数
		S_M：火箭特征横截面积
		m：火箭质量
		m_low：火箭燃尽燃料质量
		g：重力系数
		lacher：发射架长度
		J：转动惯量
		C_M：俯仰力矩系数

	参数：
		pitch：俯仰角
		yaw：偏航角
		roll：滚转角
		v_wx：风速V_w在地面坐标系x上的分量
		alpha：冲角
		V：地面坐标系速度
		X：地面坐标系位移
		X_dot：地面坐标系X速度
		Y_dot：地面坐标系Y速度
		f_l：发射架静摩擦力，默认值为0.1
		t：实时时间
		P_pram：推力变化曲线参数
		m_pram：质量变化曲线参数
		pitch_dot：旋转角速度的X分量
		w_X1：火箭绕质心转动的角速度
		rou：空气密度

	输出：
		pitch：俯仰角
"""
		
		
from sympy import solve,Symbol,integrate
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rou = 1.293
g = 9.79

def angle2radian(method, angle, prec=5):
	"""角度转数值

		method：方法，sin or cos or tan
		angle：角度
		prec：精度
	"""
	if method == "sin":
		return round(math.sin(math.radians(angle)), prec)
	elif method == "cos":
		return round(math.cos(math.radians(angle)), prec)
	elif method == "tan":
		return round(math.tan(math.radians(angle)), prec)
	else:
		raise "转换失败"


def radian2angle(method, radian, prec=3):
	"""数值转角度

		method：方法，arcsin、arccos、
		angle：角度
		prec：精度
	"""
	def r2a(r):
		return 180./math.pi * r

	if method == "arcsin":
		return round(r2a(math.asin(radian)), prec)
	elif method == "arccos":
		return round(r2a(math.acos(radian)), prec)
	elif method == "arctan":
		return r2a(math.atan(radian))
	else:
		raise "转换失败"


class Rocket(object):
	"""	火箭类，含有火箭的固有属性
	"""

	def __init__(self, m = 0.06441, m_low = 0.061112,g=9.79, T = 0.71519, lacher = 1.3, L_M = 0.005, roc_lenth = 0.005, V_w=0, V_w_ang=0, azimuth=0, launch_angle=0):
		self.T = None
		self.f_l = 0.1
		self.m = m # 初始质量（kg)
		self.m_low = m_low # 燃尽质量（kg）
		self.g = g # 重力加速度
		self.T = T # 发动机工作时间
		self.L_M = L_M # 火箭底部直径
		self.S_M = math.pi*(L_M/2)**2 # 横截面积
		self.roc_lenth = roc_lenth # 火箭长度
		self.lacher = lacher # 发射架长度
		self.V_w = V_w # 风速
		self.azimuth = azimuth # 风向角
		self.launch_angle = launch_angle # 发射角
		self.V_w_ang = azimuth - launch_angle # 发射角与风向角的夹角


	def normal(self):
		"""必要的参数计算
		"""
		self.V_wx = -1 * self.V_w * angle2radian("cos", self.V_w_ang) # 风速在地面坐标系X上的分量
		print(self.V_w, self.V_wx)

		reader = pd.read_csv('data.csv',names=['t','P','m','C_Y', 'C_D', 'C_M', 'J']) 
		# 计算推力P的曲线
		t = reader['t'][:62]
		P = reader['P'][:62]
		self.P_curve = np.polyfit(t,P,200)
		# 计算质量m的曲线
		m = reader['m'][:62]
		self.m_curve = np.polyfit(t,m,50)
		# 升力系数
		t = reader['t'][27:149]
		C_Y = reader['C_Y'][27:149]
		self.C_Y_curve = np.polyfit(t,C_Y,100)
		# 阻力系数
		t = reader['t'][:145]
		C_D = reader['C_D'][:145]
		self.C_D_curve = np.polyfit(t,C_D,100)
		# 俯仰力矩系数
		t = reader['t'][27:149]
		C_M = reader['C_M'][27:149]
		self.C_M_curve = np.polyfit(t,C_M,200)
		# 绕z轴转动惯量
		t = reader['t'][:149]
		J = reader['J'][:149]
		self.J_curve = np.polyfit(t,J,50)


	def C_D(self, t):
		"""返回阻力系数
		"""
		C_D = np.polyval(self.C_D_curve, t)
		if C_D < 0 or C_D > 1:
			return 0.
		else:
			return C_D


	def C_Y(self, t):
		"""返回升力系数
		"""
		C_Y = np.polyval(self.C_Y_curve, t)
		if C_Y < 0 or C_Y > 15:
			return 0.
		else:
			return C_Y


	def C_M(self, t):
		"""获得火箭的力矩系数
		"""
		C_M = np.polyval(self.C_M_curve, t)
		if C_M < 5 and C_M > -5:
			return C_M
		else:
			return 0.

	def J(self,t):
		"""获得火箭的转动惯量
		"""
		J = np.polyval(self.J_curve, t)
		if J < 0.002 and J >0.00001:
			return J
		else:
			return 0.

	def getm(self, t):
		"""获得火箭实时质量
		"""
		if t <= self.T:
			return np.polyval(self.m_curve, t)*0.001 # 由于csv里面的单位是g，所以要×0.01换算回来
		else:
			return self.m_low


	def getP(self, t):
		"""获得火箭实时推力
			y = a * x**2 + b*x
		"""
		P = np.polyval(self.P_curve, t)
		if P < 0:
			return 0
		elif t <= self.T and P < 20:
			return P
		else:
			return 0.			
		

	def getv(self, t0, ti, pitch, launch=False):
		"""获得实时的速度v
			launch：是否脱离发射架
		"""
		t = Symbol('t')
		v = 0.
		for ti in np.arange(t0, ti+0.01, 0.01):
			ti = round(ti, 2) #取小数点后两位
			p = self.getP(ti)
			m = self.getm(ti)
			f = m * self.g * angle2radian("cos", pitch, 2)
			v += integrate(((p-f-0.15)/m),(t,ti-0.01,ti))

		return v


	def V_apo(self, u_w, v_w):
		"""返回箭体坐标系合速度
		"""
		return math.sqrt(u_w**2 + v_w**2)


	def q_apo(self, V_apo):
		"""动压头
		"""
		return 1/2 * rou * V_apo**2


	def alpha(self, u_w, v_w):
		"""攻角
		"""
		return math.atan(v_w/u_w)


	def Xdot_Ydot(self, V, pitch):
		"""速度在坐标系上的分量
		"""
		X_dot = angle2radian("cos", pitch)*V
		Y_dot = angle2radian("sin", pitch)*V
		return X_dot, Y_dot

	def X_Y_dot2uv(self, X_dot, Y_dot, pitch):
		"""地面坐标系转换为箭体坐标系
		"""
		u = X_dot * angle2radian("cos", pitch) + Y_dot*angle2radian("sin", pitch)
		v = -1*X_dot * angle2radian("sin", pitch) + Y_dot*angle2radian("cos", pitch)
		return u, v


	def t_0(self, m, f_l, pitch):
		"""火箭获得速度的时间t0
		"""
		for ti in np.arange(0, 1, 0.01):
			f = self.getm(ti) * self.g * angle2radian("sin", pitch) # 重力的分量
			P = self.getP(ti)
			if P >= f + self.f_l:
				return ti
				
	def t_1(self, t0, lacher, pitch):
		"""起飞到离开发射架的时间
		"""
		t = Symbol('t')
		x = 0.
		for ti in np.arange(t0, 1, 0.01):
			v = self.getv(t0, ti, pitch)
			x += integrate((v),(t,ti,ti+0.01))
			#print("ti",ti, "v", v, x)
			if x >= lacher:
				return ti, v-4


	def t_2(self, t0, t1, pitch, V):
		"""从离开发射架到燃料用尽
		"""
		X = self.lacher * angle2radian("cos", pitch)
		Y = self.lacher * angle2radian("sin", pitch)
		theta = pitch
		for ti in np.arange(t0+t1, self.T, 0.01):
			m = self.getm(ti) # 质量
			P = self.getP(ti) # 推力
			F_x = self.C_D(ti) * 0.5 * rou * self.S_M * (V - self.V_wx)**2 # 阻力
			F_y = self.C_Y(ti) * 0.5 * rou * self.S_M * V**2 # 升力
			q_apo = self.q_apo(V-self.V_wx) # 动压头
			V_dot = (P*angle2radian("cos", theta) - F_x - m*g*angle2radian("sin", theta)) / m # 切向加速度
			V_theta = (P*angle2radian("sin", theta) + F_y - m*g*angle2radian("cos", theta)) / m # 法向加速度
			V += math.sqrt(V_dot**2+V_theta**2)*0.01
			theta_dot = -1 * m *g*angle2radian("cos", theta)/(m*V)
			theta += theta_dot*0.01
			X_dot, Y_dot = self.Xdot_Ydot(V, theta)
			X += X_dot*0.01
			Y += Y_dot*0.01
			print("t:", ti, "V:", V, "V_dot", V_dot, "X:", X, "Y", Y, "Y_dot", Y_dot, "theta", theta)
			print("X_dot：", X_dot, "Y_dot：", Y_dot)
		return X, Y, V, theta

	def t_3(self, t_before, X, Y, V, theta):
		"""燃料用尽到高度为0
		"""
		X = X
		Y = Y
		plotY = []
		plott = []
		# gamma = 0.7198
		# A = 0.02985
		# theta_dot = 0
		# Cy = math.pi*gamma/(1+math.sqrt(1+(gamma/2)**2))
		for ti in np.arange(t_before, 30, 0.01):
			m = self.getm(ti) # 质量

			# F_y = Cy*(-theta_dot)*0.5 * rou * V**2 *A
			# theta_dot = radian2angle("arcsin", (F_y/m-g)/V)
			# theta += theta_dot*0.01

			F_x = self.C_D(ti) * 0.5 * rou * self.S_M * (V - self.V_wx)**2 # 阻力
			F_y = self.C_Y(ti) * 0.5 * rou * self.S_M * V**2 # 升力
			V_dot =(-F_x - m*g*angle2radian("sin", theta)) / m # 切向加速度
			V_theta = (F_y - m*g*angle2radian("cos", theta)) / m # 法向加速度
			V += (V_dot + V_theta)*0.01
			theta_dot = F_y/(m*V) - g*angle2radian("cos", theta)/V
			theta += theta_dot*0.01
			X_dot, Y_dot = self.Xdot_Ydot(V, theta)
			# X += X_dot*0.01
			# Y += Y_dot*0.01

			q_apo = self.q_apo(V-self.V_wx) # 动压头
			X_dot_dot = 1/m*(-1*self.C_D(ti)*q_apo*self.S_M)*X_dot/V
			Y_dot_dot = 1/m*(-1*self.C_D(ti)*q_apo*self.S_M)*Y_dot/V-g
			X_dot += X_dot_dot*0.01
			Y_dot += Y_dot_dot*0.01
			X += X_dot*0.01
			Y += Y_dot*0.01

			print("t:", ti, "V:", V, "X:", X, "Y:", Y, "V_dot:", V_dot, theta)
			print("X_dot：", X_dot, "Y_dot：", Y_dot, "Y_dot_dot：", Y_dot_dot)
			plott.append(X)
			plotY.append(Y)
			if Y <= 0:
				plt.plot(plott, plotY)
				plt.show()
				return X, ti, V

		raise "计算错误"

	def process(self, pitch):
		"""弹道过程
		"""
		self.t0 = self.t_0(self.m, self.f_l, pitch)
		self.t1, v = self.t_1(self.t0, self.lacher, pitch)
		self.t1 -= self.t0
		self.t2 = self.T - self.t0 - self.t1
		X, Y, V, theta = self.t_2(self.t0, self.t1, pitch, v)
		X, self.total_t, V = self.t_3(self.T, X, Y, V, theta)
		print("各个时间段：", self.t0, self.t1, self.t2, self.total_t-self.T, "总时间：", self.total_t)
		return X, self.total_t

	def stimulate(self, ang_min=0, ang_max=90):
		"""模拟所有角度
		"""
		X_map = []
		t_map = []
		for pitch in np.arange(ang_min, ang_max, 1):
			X, t = self.process(pitch)
			X_map.append(X)
			t_map.append(t)

		print(X_map)
		max_X = max(X_map)
		min_X = min(X_map)
		return max_X, min_X, X_map

if __name__ == '__main__':
	r = Rocket(T=1.8551, m=0.06441, m_low=0.061112, L_M=0.025, V_w_ang=90, V_w=2, roc_lenth=0.425, lacher=1)
	r.normal() # 进行一系列初始化运算
	r.process(45)
	#r.stimulate()