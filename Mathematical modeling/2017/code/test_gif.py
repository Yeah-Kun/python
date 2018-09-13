import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
import math
    
plt.close()  #clf() # 清图  cla() # 清坐标轴 close() # 关窗口
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.axis("equal") #设置图像显示的时候XY轴比例
plt.grid(True) #添加网格
plt.ion()  #interactive mode on
IniObsX=0000
IniObsY=4000
IniObsAngle=135
IniObsSpeed=10*math.sqrt(2)   #米/秒
print('开始仿真')
try:
    for t in range(180):
        #障碍物船只轨迹
        obsX=IniObsX+IniObsSpeed*math.sin(IniObsAngle/180*math.pi)*t
        obsY=IniObsY+IniObsSpeed*math.cos(IniObsAngle/180*math.pi)*t
        ax.scatter(obsX,obsY,c='b',marker='.')  #散点图
        #ax.lines.pop(1)  删除轨迹
        #下面的图,两船的距离
        plt.pause(0.001)
except Exception as err:
    print(err)