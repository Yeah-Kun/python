"""
	弹道预测程序
	create by Ian in 2018-6-10 16:13:14

	输入：
		T：发动机工作时间
		launch_angle：发射角，箭体坐标系的X坐标
		V_w_ang：发射角与风向角的夹角
		azimuth：方位角，以正北为0°
		V_w：实测风速
		tar_S：目标距离
		C_D：阻力系数
		C_Y：升力系数
		q_apo：动压头，1/2 * dens * V_apo**2
		S_M：火箭特征横截面积
		m：火箭质量
		m_low：燃尽燃料后的火箭质量
		g：重力系数
		P_max：最大推力
		lacher：发射架长度

	参数：
		pitch：俯仰角
		yaw：偏航角
		roll：滚转角
		v_wx：风速V_w在地面坐标系x上的分量
		v_wz：风速V_w在地面坐标系z上的分量
		v_w：风速
		alpha：冲角
		V_hat：箭体坐标系速度
		V：地面坐标系速度
		X：地面坐标系位移
		X_dot：地面坐标系X速度
		Y_dot：地面坐标系Y速度
		u：箭体坐标系X上的分量
		v：箭体坐标系Y上的分量
		u_dot：箭体X坐标的实时速度
		v_dot：箭体Y坐标的实时速度
		V_apo：箭体坐标系合速度
		f_l：发射架静摩擦力，默认值为0.1
		t：实时时间
		P_pram：推力变化曲线参数
		m_pram：质量变化曲线参数
		pitch_apo：φ'，气流入射角，Y1O1Z1平面的投影与O1Y1的夹角
		pitch_dot：旋转角速度的X分量
		w_X1：火箭绕质心转动的角速度
		w_Y1：
		w_Z1：

	输出：
		pitch：俯仰角
		yaw：偏航角
"""
		
		
from sympy import solve,Symbol,integrate
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def test_P_curve(x,a,b,c,d):
	return a*x**3 + b*x**2 + c*x + d

def readdata():
	reader = pd.read_csv('data.csv',names=['t','P','m','C_Y', 'C_D', 'pitch_dot']) 
	t = reader['t'][27:147]
	P = reader['C_Y'][27:147]
	
	
	P_curve = np.polyfit(t,P,100)
	y = np.polyval(P_curve, t)
	print(np.polyval(P_curve, 4.5))
	plt.plot(t,P)
	plt.plot(t,y)
	plt.show()
	#fita,fitb=optimize.curve_fit(test_P_curve,x,ymax,[1,1,1])


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


def radian2angle(method, radian, prec=1):
	def r2a(r):
		return 180./math.pi *r

	if method == "arcsin":
		return round(r2a(math.asin(radian)), prec)
	elif method == "arccos":
		return round(r2a(math.acos(radian)), prec)
	elif method == "arctan":
		return round(r2a(math.atan(radian)), prec)
	else:
		raise "转换失败"


class Rocket(object):
	"""	火箭类，含有火箭的固有属性
	"""

	def __init__(self, m = 0.055714, m_low = 0.052416, g=9.79, T = 0.7428, lacher = 1.3, L_M = None, V_w=0, V_w_ang=0, azimuth=0, P_max=10):
		self.T = None
		self.f_l = 0.1
		self.m = m # 初始质量（kg）
		self.m_low = m_low # 火箭燃尽质量（kg）
		self.g = g # 重力加速度
		self.T = T # 发动机工作时间
		self.S_M = math.pi*(L_M/2)**2 # 横截面积
		self.lacher = lacher # 发射架长度
		self.V_w = V_w # 风速
		self.V_w_ang = V_w_ang # 发射角与风向角的夹角
		self.azimuth = azimuth # 方向角
		self.u = 0 # 箭体坐标系的X
		self.v = 0 # 箭体坐标系的Y
		self.P_max = P_max # 最大推力

	def normal(self):
		"""必要的参数计算
		"""
		self.v_wx = -1 * self.V_w * angle2radian("cos", self.V_w_ang)
		print(self.V_w, self.v_wx)
		self.v_wz = -1 * self.V_w * angle2radian("sin", self.V_w_ang)
		reader = pd.read_csv('data.csv',names=['t','P','m','C_Y', 'C_D', 'pitch_dot', 'f_m']) 
		# 计算推力P的曲线
		t = reader['t'][:64]
		P = reader['P'][:64]
		self.P_curve = np.polyfit(t,P,200)
		# 计算质量m的曲线
		m = reader['m'][:64]
		self.m_curve = np.polyfit(t,m,30)
		# 升力系数
		t = reader['t'][27:147]
		C_Y = reader['C_Y'][27:147]
		self.C_Y_curve = np.polyfit(t,C_Y,100)
		# 阻力系数
		t = reader['t'][:145]
		C_D = reader['C_D'][:145]
		self.C_D_curve = np.polyfit(t,C_D,100)
		# 俯仰角速度
		t = reader['t'][28:145]
		pitch_dot = reader['pitch_dot'][28:145]
		self.pitch_dot_curve = np.polyfit(t, pitch_dot, 100)

		t = reader['t'][56:]
		f_m = reader['f_m'][56:]
		self.f_m_curve = np.polyfit(t, f_m, 100)
		# a = []
		# for ti in t:
		# 	x = np.polyval(self.f_m_curve, ti)
		# 	a.append(x)
		# plt.plot(t,a)
		# plt.show()


	def q_apo(self, V_apo):
		"""动压头
		"""
		return 1/2 * 1.1691 * V_apo**2

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

	def pitch_dot(self, t):
		"""返回升力系数
		"""
		pitch_dot = np.polyval(self.pitch_dot_curve, t)
		if pitch_dot < -50 or pitch_dot > 50:
			return 0.
		else:
			return pitch_dot


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
		if P <0:
			return 0.
		else:
			return P

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


	def CA_CN(self, C_D, C_Y, alpha):
		"""
		"""
		C_A = C_D * angle2radian("cos", alpha) - C_Y * angle2radian("sin", alpha)
		C_N = C_D * angle2radian("sin", alpha) - C_Y * angle2radian("cos", alpha)
		return C_A, C_N


	def uw_vw(self, u, v, pitch):
		"""计算风速u_w和v_w
		"""
		u_w = u - self.v_wx * angle2radian("cos", pitch)
		v_w = v + self.v_wx * angle2radian("sin", pitch)
		#print("v_w计算:", self.v_wz, angle2radian("sin", pitch))
		return u_w, v_w

	
	def cos_pitch_apo(self, v_w):
		"""气流入射角的cos值
		"""
		if v_w < 0:
			return -1.
		else:
			return 1.


	def udot_vdot(self, t, m, P, C_A, C_N, S_M, q_apo, pitch, pitch_dot, cos_pitch_apo, u, v=0.):
		"""计算实时的u和v
			u：箭体坐标系X的速度
			v：Y的速度
		"""
		if v==0.:
			return u, v
		else:
			u_dot = 1/m * (P - m*self.g*angle2radian("sin", pitch) - C_A*S_M*q_apo) + v * self.pitch_dot(t)
			v_dot = -1/m * (m*self.g*angle2radian("cos", pitch) + C_N*S_M*q_apo* cos_pitch_apo)  - u* self.pitch_dot(t)
			return u_dot, v_dot

	def u_v(self, u, v, u_dot, v_dot):
		"""箭体坐标系u和v的实时速度
		"""
		u += 0.01* u_dot
		v += 0.01*v_dot
		return u, v

	def V_apo(self, u_w, v_w):
		"""返回箭体坐标系合速度
		"""
		return math.sqrt(u_w**2 + v_w**2)

	def alpha(self, u_w, v_w):
		"""攻角
		"""
		return math.atan(v_w/u_w)


	def Xdot_Ydot(self, u, v, pitch):
		X_dot = u * angle2radian("cos", pitch) - v*angle2radian("sin", pitch)
		Y_dot = u * angle2radian("sin", pitch) + v*angle2radian("cos", pitch)
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
			f = self.getm(ti) * self.g * angle2radian("cos", pitch) # 重力的分量
			P = self.getP(ti)
			#print(ti, P, f, self.getm(ti))
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
			if x >= lacher:
				return ti, v


	def t_2(self, t0, t1, pitch, u, v=0.):
		"""从离开发射架到燃料用尽
		"""
		X = self.lacher * angle2radian("cos", pitch)
		Y = self.lacher * angle2radian("sin", pitch)
		for ti in np.arange(t0+t1, self.T+0.01, 0.01):
			u_w, v_w = self.uw_vw(u, v, pitch)

			pitch_dot = self.pitch_dot(ti)
			pitch += pitch_dot*0.01 # 计算俯仰角
			u, v = self.u_v(u, v, u_w, v_w)
			X_dot, Y_dot = self.Xdot_Ydot(u, v, pitch)
			X += X_dot*0.01 - 0.01*0.07#地面坐标系位移
			Y += Y_dot*0.01 - 0.01*0.07 # 人工给它加风阻系数

		return u, v, X, Y, pitch

	def t_3(self, t_before, pitch, u, v, X, Y):
		"""燃料用尽到高度为0
		"""
		def getf(t):
			if t <= 14:
				f_m = np.polyval(self.f_m_curve, t) 
			else:
				f_m = 0.2
			return f_m
		def rect_system(X_dot, Y_dot, t):
			V_apo = self.V_apo(X_dot, Y_dot)
			vf = getf(t) / self.getm(t) * 0.01
			cos_theta = X_dot/ V_apo
			sin_theta = Y_dot/ V_apo
			X_dot = V_apo * cos_theta - cos_theta * vf
			Y_dot = V_apo * sin_theta - 0.01 * self.g - sin_theta * vf
			return X_dot, Y_dot

		X_dot, Y_dot = self.Xdot_Ydot(u, v, pitch) # 计算地面坐标系速度

		# tshow = []
		# Yshow = []
		#Xshow = []
		# V_aposhow = []
		for ti in np.arange(t_before, 16, 0.01):
			X_dot, Y_dot = rect_system(X_dot, Y_dot, ti)
			X += X_dot*0.01 #地面坐标系位移
			Y += Y_dot*0.01
			V_apo = self.V_apo(X_dot, Y_dot)

			# tshow.append(ti)
			# Yshow.append(Y)
			#Xshow.append(X)
			# V_aposhow.append(V_apo)
			
			if Y <= 0:
				# plt.plot(tshow, Yshow)
				# #plt.plot(tshow, Xshow)
				# plt.show()
				# print(ti, Y, V_apo)
				return ti, u, v, X
		raise "计算错误"

	def process(self, pitch):
		"""弹道过程
		"""
		self.t0 = self.t_0(self.m, self.f_l, pitch)
		self.t1, u = self.t_1(self.t0, self.lacher, pitch)
		self.t1 -= self.t0
		self.t2 = self.T - self.t0 - self.t1
		u, v, X, Y, pitch = self.t_2(self.t0, self.t1, pitch, u)
		self.total_t, u, v, X = self.t_3(self.T, pitch, u, v, X, Y)
		print("各个时间段：", self.t0, self.t1, self.t2, self.total_t-self.T)
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
	r = Rocket(T=0.73535, m=0.06441, m_low=0.061112, L_M=0.077, V_w_ang=90, V_w=2)
	r.normal() # 进行一系列初始化运算
	r.stimulate()