a = 5

print(id(a))


b = a

print(id(a))
print(id(b))


a += 2

print(id(a))
print(id(7))

print(id(b))

list2 = [1,2,3]


list1 = list2
list1[0] = 10
print(id(list2))
print(id(list1))

