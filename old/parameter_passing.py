def f(x):
	print(id(x))
	x = 100
	print(id(x))

a = 1
print(id(a))

f(a)
print(id(a))
