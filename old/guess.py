import random
secret=random.randint(1,6)
times=3
while times:
    temp=input("输入一个数：")
    num=int(temp)
    if(num==secret):
        print("你好棒哦，这也能猜中！")
        break
    else:
        print("猜错了哦，再猜一次吧~")
    times-=1
