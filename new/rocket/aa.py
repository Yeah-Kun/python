import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

reader = pd.read_csv(r'liju.csv',names=['t','P']) 
	
t = reader['t']
P = reader['P']

P_curve = np.polyfit(t,P,100)
y = np.polyval(P_curve, t)
print(np.polyval(P_curve, 0.8))
plt.plot(t,P)
plt.plot(t,y)
plt.show()