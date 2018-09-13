import time

print("start")
start_time = time.time()
temp = 0
for i in range(10000000):
	temp += i
print(temp)
end_time = time.time()
print(end_time - start_time)
