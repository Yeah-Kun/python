"""
	缓存修改代码模块
"""
def t_3(self, t_before, pitch, u, v, X, Y):
	"""燃料用尽到高度为0
	"""
	def rect_system(X_dot, Y_dot):
		V_apo = self.V_apo(X_dot, Y_dot)
		cos_theta = X_dot/ V_apo
		sin_theta = Y_dot/ V_apo
		X_dot = V_apo * cos_theta
		Y_dot = V_apo * sin_theta - 0.01 * self.g
		return X_dot, Y_dot

	X_dot, Y_dot = self.Xdot_Ydot(u, v, pitch) # 计算地面坐标系速度
	tshow = []
	Yshow = []
	V_aposhow = []
	for ti in np.arange(t_before, 20, 0.01):
		X_dot, Y_dot = rect_system(X_dot, Y_dot)
		X += X_dot*0.01 #地面坐标系位移
		Y += Y_dot*0.01
		V_apo = self.V_apo(X_dot, Y_dot)
		print(ti, Y, V_apo)

		tshow.append(ti)
		Yshow.append(Y)
		V_aposhow.append(V_apo)
		
		if Y <= 0:
			plt.plot(tshow, Yshow)
			plt.show()
			return ti, u, v, X
	raise "计算错误"



def t_2(self, t0, t1, pitch, u, v=0.):
	"""从离开发射架到燃料用尽
	"""
	X = self.Lacher * angle2radian("cos", pitch)
	Y = self.Lacher * angle2radian("sin", pitch)
	for ti in np.arange(t0+t1, self.T+0.01, 0.01):
		u_w, v_w = self.uw_vw(u, v, pitch)
		C_D = self.C_D(ti)
		C_Y = self.C_Y(ti)
		alpha = self.alpha(u_w, v_w)
		C_A, C_N = self.CA_CN(C_D, C_Y, alpha)
		V_apo = self.V_apo(u_w, v_w)
		q_apo = self.q_apo(V_apo)
		cos_pitch_apo = self.cos_pitch_apo(v_w)
		pitch_dot = self.pitch_dot(ti)
		pitch += pitch_dot*0.01 # 计算俯仰角
		#u_dot, v_dot = self.udot_vdot(ti, self.getm(ti), self.getP(ti), C_A, C_N, self.S_M, q_apo, pitch, pitch_dot, cos_pitch_apo, u, v=0.001)
		#u, v = self.u_v(u, v, u_dot, v_dot) # 箭体坐标系位移
		u, v = self.u_v(u, v, u_w, v_w)
		X_dot, Y_dot = self.Xdot_Ydot(u, v, pitch)
		X += X_dot*0.01 #地面坐标系位移
		Y += Y_dot*0.01

	return u, v, X, Y, pitch