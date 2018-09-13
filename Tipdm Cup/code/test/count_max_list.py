import collections

bs0bj = [[10, 8, 113, 82, 17, 0, 0], [10, 4, 4, 5, 3, 0, 2], [10, 4, 3, 5, 4, 0, 2], [10, 4, 1, 5, 1, 0, 2], [8, 4, 1, 5, 2, 0, 2], [10, 4, 4, 5, 1, 0, 2], [7, 4, 1, 5, 1, 0, 2], [10, 4, 1, 5, 1, 0, 2], [10, 4, 1, 5, 1, 0, 2], [10, 4, 1, 5, 1, 0, 2], [10, 4, 1, 5, 1, 0, 2], [10, 4, 1, 5, 1, 0, 2], [10, 4, 2, 5, 1, 0, 2], [7, 4, 1, 5, 1, 0, 2], [7, 4, 1, 5, 1, 0, 2], [7, 4, 4, 5, 1, 0, 2], [7, 4, 1, 5, 1, 0, 2], [7, 4, 2, 5, 1, 0, 2], [7, 4, 1, 5, 1, 0, 2], [7, 4, 1, 5, 1, 0, 2], [7, 4, 1, 5, 1, 0, 2]]

# 标准值的第一个元素，用于选出标准值
def CountKey(matrix_pack):
	temp = 0
	temp_list = []
	for one in bs0bj:
		temp_list.append(one[0])
	result_list = collections.Counter(temp_list)
	dict(result_list)
	return max(result_list.items(),key = lambda x:x[1])[0]

print(CountKey(bs0bj))