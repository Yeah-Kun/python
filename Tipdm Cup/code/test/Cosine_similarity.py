import math

hinsA = [15, 2, 46, 45, 2, 0, 0]
hinsB = [7, 4, 1, 5, 1, 0, 2]

# 两个矩阵余弦相似度计算


def CosSimilarity(hinsA, hinsB):
    up_count = 0
    down_left_count = 0
    down_right_count = 0
    result_count = 0
    i = 0
    # 计算两个向量的点积
    while i < len(hinsA):
        up_count = up_count + hinsA[i] * hinsB[i]
        i = i + 1
    i = 0

    # 计算两个向量的模
    while i < len(hinsA):
        down_left_count = down_left_count + hinsA[i] **2
        i = i + 1
    i = 0
    while i < len(hinsB):
        down_right_count = down_right_count + hinsB[i] **2
        i = i + 1
    print(up_count)
    print(down_left_count)
    print(down_right_count)
    result_count = up_count / (math.sqrt(down_left_count)*math.sqrt(down_right_count)) 

    return result_count

print(CosSimilarity(hinsA,hinsB))



