temp=input("请输入年份：")
num=int(temp)
if((num%4==0 and num%100!=0)or num%400==0):
    print("这是闰年")
else:
    print("这是平年")
    
