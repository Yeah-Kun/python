class SuperList(list):
	def __sub__(self,b):
		a = self[:]
		b = b[:]

		while len(b) > 0:
			element_b = b.pop()
			if element_b in a:
				a.remove(element_b)

		return a

print(SuperList([1,2,3]) - SuperList([1,2]))

a = SuperList([1,2,3])
b = SuperList([1,2])
print(b - a)