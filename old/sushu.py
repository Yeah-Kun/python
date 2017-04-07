from math import sqrt
n = input("请输入一个数：")
for i in sqrt(n):
	if(n%i == 0):
		print("这个数不是素数")