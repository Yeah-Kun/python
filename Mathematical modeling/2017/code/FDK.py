'''FDK算法模型的实现
    made by Ian in 2017-9-16 22:34:59
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from PIL import Image, ImageChops
from scipy.fftpack import fft, fftshift, ifft
import xlrd

def dummyImg(size0, size1):
    """this just creates a silly 8-bit image consisting of a solid rectangle
    inputs: size0, size1 - dimensions of image in pixels
    output: dumImg - PIL image object
    这只是创建一个由实心矩形组成的愚蠢的8位图像
    输入：size0，size1 - 以像素为单位的图像尺寸
    输出：dumImg - PIL图像对象"""
    M = np.zeros((size0, size1))
    a = round(size0/4)
    b = round(size1/4)
    M[a:size0-a,b:size1-b] = 255 #insert centered rectangle with dimensions 1/2 the size of the image
    dumImg = Image.fromarray(M.astype('uint8'))  #create image object
    return dumImg

def padImage(img):
    """pad images with zeros such that new image is a square with sides equal to
    the diagonal of the original in size. Return padded image as well as coordinates
    of upper-left coordinates where original image is implanted
    用零填充图像，使得新图像是具有边等于的正方形
    原尺寸的对角线。返回填充图像以及坐标
    植入原始图像的左上坐标系"""
    N0, N1 = img.size
    lenDiag = int(np.ceil(np.sqrt(N0**2+N1**2))) # 返回输入的上限，以元素为单位
    imgPad = Image.new('L',(lenDiag, lenDiag))
    c0, c1 = int(round((lenDiag-N0)/2)), int(round((lenDiag-N1)/2)) #coordinates of top-left corner in which to paste image
    imgPad.paste(img, (c0,c1)) 
    return imgPad, c0, c1

def getProj(img, theta):
    """this rotates an image by an array of angles and takes projections.
    Note that we pad the image beforehand rather than allow the rotate method 
    to expand the image because the image expands to different sizes depending
    on the angle of rotation. We need to expand every rotated image to the 
    same size so that we can collect the contributions into the same vector.
    inputs:  img - PIL image object
             theta - 1D numpy array of angles over which to compute projections
    output: sinogram - projections of img over theta (effectively the radon transform)
    这样通过一系列角度旋转图像并进行投影。
    请注意，我们预先填充图像，而不是允许旋转方法
    以扩大图像，因为图像根据不同的尺寸扩大到不同的大小
    在旋转角度。我们需要将每个旋转的图像扩展到
    相同的大小，以便我们可以收集到同一个向量的贡献。
    输入：img - PIL图像对象
             theta-1D numpy数组，用于计算投影
    输出：正弦图 - img超过theta的投影（实际上是氡变换）"""

    numAngles = len(theta) # 获得旋转角度的数量
    sinogram = np.zeros((img.size[0],numAngles)) # 建立2D零矩阵

    #set up plotting
    plt.ion() # 打开交互模式
    fig1, (ax1, ax2) = plt.subplots(1,2) # 画两个字图
    im1 = ax1.imshow(img, cmap='gray') # 展示原始图片
    ax1.set_title('<-- Sum')
    im2 = ax2.imshow(sinogram, extent=[theta[0],theta[-1], img.size[0]-1, 0], # extent设置右边子图的x，y轴 0,178,724,0
                     cmap='gray', aspect='auto')
    ax2.set_xlabel('Angle (deg)')
    ax2.set_title('Sinogram')
    plt.show()

    #get projections an dplot 绘制点预测
    for n in range(numAngles):
        rotImgObj = img.rotate(90-theta[n], resample=Image.BICUBIC) #返回一个按照给定角度顺时钟围绕图像中心旋转后的图像拷贝
        #print(rotImgObj)
        #im1.set_data(rotImgObj)
        sinogram[:,n] = np.sum(rotImgObj, axis=0) # 计算总值，做成一列给sinogram ,axis=0：轴为0，将同一列的值相加
        im2.set_data(Image.fromarray((sinogram-np.min(sinogram))/np.ptp(sinogram)*255)) # 给右边子图描点，ptp：返回最大和最小值之差，fromarray从导出数组接口的对象（使用缓冲区协议）创建映像内存
        fig1.canvas.draw()
    plt.ioff() # 关闭交互模式
    return sinogram


def arange2(start, stop=None, step=1):
    """#Modified version of numpy.arange which corrects error associated with non-integer step size
    Modified版本的numpy.arange，它纠正与非整数步长相关联的错误"""
    if stop == None:
        a = np.arange(start)
    else: 
        a = np.arange(start, stop, step)
        if a[-1] > stop-step:   
            a = np.delete(a, -1)
    return a

def projFilter(sino):
    """filter projections. Normally a ramp filter multiplied by a window function is used in filtered
    backprojection. The filter function here can be adjusted by a single parameter 'a' to either approximate
    a pure ramp filter (a ~ 0)  or one that is multiplied by a sinc window with increasing cutoff frequency (a ~ 1).
    Credit goes to Wakas Aqram. 
    inputs: sino - [n x m] numpy array where n is the number of projections and m is the number of angles used.
    outputs: filtSino - [n x m] filtered sinogram array
    滤波器投影。通常在滤波器中使用与窗函数相乘的斜坡滤波器
    反投影。这里的滤波器功能可以通过单个参数“a”进行调整以进行近似
    一个纯粹的斜坡滤波器（a〜0），或者一个随着截止频率增加（a〜1）的sinc窗口相乘的斜坡滤波器。
    信用到Wakas Aqram。
    输入：sino - [n x m] numpy数组，其中n是投影的数量，m是使用的角度数。
    输出：filtSino - [n x m]过滤的正弦图数组"""
    
    a = 0.1;
    projLen, numAngles = sino.shape # 获得附件二的x，y坐标值，x：180，y：725
    step = 2*np.pi/projLen # np.pi:3.1415925
    w = arange2(-np.pi, np.pi, step) # 生成从-3.14159265 -3.13292619~3.124259  3.132926的列表
    if len(w) < projLen: # 统计w列表的元素个数是否少于725
        w = np.concatenate([w, [w[-1]+step]]) #depending on image size, it might be that len(w) =  取决于图片的大小
                                              #projLen - 1. Another element is added to w in this case 长度-1，另一个元素被增加到w中
    rn1 = abs(2/a*np.sin(a*w/2));  #approximation of ramp filter abs(w) with a funciton abs(sin(w)) #获得abs(sin(w))的近似值
    rn2 = np.sin(a*w/2)/(a*w/2);   #sinc window with 'a' modifying the cutoff freqs # 修改截止频率
    r = rn1*(rn2)**2;              #modulation of ramp filter with sinc window # sinc窗口的渐变滤波器调制
    
    filt = fftshift(r)   # 正弦信号的频谱绘制
    filtSino = np.zeros((projLen, numAngles)) # 生成y行，x列的零矩阵，x：180，y：725
    for i in range(numAngles):
        projfft = fft(sino[:,i]) # 频谱绘制
        filtProj = projfft*filt  # filt：正弦信号的频谱
        filtSino[:,i] = np.real(ifft(filtProj)) # ifft：计算一维离散傅里叶逆变换，real：返回实数
    print(filtSino)
    return filtSino
        
def backproject(sinogram, theta):
    """Backprojection function. 
    inputs:  sinogram - [n x m] numpy array where n is the number of projections and m the number of angles
             theta - vector of length m denoting the angles represented in the sinogram
    output: backprojArray - [n x n] backprojected 2-D numpy array
    反投影功能。
    输入：正弦图 - [n x m] numpy数组，其中n是投影的数量，m是角度数
             长度为m的theta矢量表示正弦图中所表示的角度
    输出：backprojArray - [n x n] backprojected 2-D numpy数组"""
    imageLen = sinogram.shape[0] # 725
    print(imageLen)
    reconMatrix = np.zeros((imageLen, imageLen)) # 建立一个imageLen x imageLen的零矩阵
    
    x = np.arange(imageLen)-imageLen/2 - 33 #create coordinate system centered at (x,y = 0,0) 创建以(x，y=0,0)为中心的坐标系统
    y = x.copy()                            # -33是为了修正坐标系
    X, Y = np.meshgrid(x, y)

    plt.ion()
    fig2, ax = plt.subplots()
    im = plt.imshow(reconMatrix, cmap='gray') # 铺网格

    theta = theta*np.pi/180 # 弧度转角度
    numAngles = len(theta)

    for n in range(numAngles):
        Xrot = X*np.sin(theta[n])-Y*np.cos(theta[n]) #determine rotated x-coordinate about origin in mesh grid form 确定网格的原点旋转的x坐标
        XrotCor = np.round(Xrot+imageLen/2) #shift back to original image coordinates, round values to make indices 回到原来的图像坐标，圆的值来做索引
        XrotCor = XrotCor.astype('int')
        projMatrix = np.zeros((imageLen, imageLen))
        m0, m1 = np.where((XrotCor >= 0) & (XrotCor <= (imageLen-1))) #after rotating, you'll inevitably have new coordinates that exceed the size of the original
        s = sinogram[:,n] #get projection 获得投影                     # 旋转后，不可避免地会有超过原始尺寸的新坐标
        projMatrix[m0, m1] = s[XrotCor[m0, m1]]  #backproject in-bounds data 从幕后投影在一个合理的数据
        reconMatrix += projMatrix # 往零矩阵上添加元素
        im.set_data(Image.fromarray((reconMatrix-np.min(reconMatrix))/np.ptp(reconMatrix)*255))
        ax.set_title('Theta = %.2f degrees' % (theta[n]*180/np.pi))
        fig2.canvas.draw()
         
    plt.close()
    plt.ioff()
    backprojArray = np.flipud(reconMatrix) # 在上下方向上翻转数组
    return backprojArray


def mydata():
    path = "D:/code/python/Mathematical modeling/CUMCM2017Problems/A/"
    data = xlrd.open_workbook(path + 'A题附件.xls')
    table = data.sheets()[2]
    nrows = table.nrows # 获取行数
    ncols = table.ncols # 获取列数
    y = [table.row_values(i) for i in range(1,nrows)] # 获取其每行的值
    y = np.array(y)
    return y

#def main():
if __name__ == '__main__':

    #myImg = dummyImg(500,700)
    myImg = Image.open('SheppLogan.png').convert('L') # 对于灰度图像,其模式为“L”
    print(myImg.size)
    myImgPad, c0, c1 = padImage(myImg)  #PIL image object
    print(myImgPad)
    dTheta = 1
    theta = np.arange(0,179,dTheta)
    print('Getting projections\n')
    mySino = mydata()
    #mySino = getProj(myImgPad, theta)  #numpy array
    print(mySino.shape)
    print('Filtering\n')
    
    filtSino = projFilter(mySino)  #numpy array
    print('Performing backprojection') 

    recon = backproject(filtSino, theta)
    
    recon2 = np.round((recon-np.min(recon))/np.ptp(recon)*255) #convert values to integers 0-255 将值转换为0~255 round:将数组舍入到给定的小数位数（类似归一化？）

    reconImg = Image.fromarray(recon2.astype('uint8'))
    n0, n1 = myImg.size
    print(c0, c1, n0, n1)
    reconImg = reconImg.crop((c0, c1, n0+c0, n1+c1)) # 从图像中提取出某个矩形大小的图像

    #fig = plt.figure(figsize=(10,10))
    #ax2 = fig.gca()
    fig3, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(12,4))
    ax1.imshow(myImg, cmap='gray')
    ax1.set_title('Original Image')
    ax2.imshow(reconImg, cmap='gray')
    ax2.set_title('Backprojected Image')
    ax3.imshow(ImageChops.difference(myImg, reconImg), cmap='gray') #note this currently doesn't work for imported images 注意，当前对导入的图像不适用
    ax3.set_title('Error')
    
    plt.show()



