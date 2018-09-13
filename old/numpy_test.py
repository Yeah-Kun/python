'''
    用于测试numpy
'''
import numpy as np


# 矩阵计算
def Column(arr, x, rat_sh, count_line, count_list):
    # 矩阵第一列
    def FirstColumn(arr, x, rat_sh, count_line, count_list):
        for i in range(0, count_line):
            if x[i] <= rat_sh[0]:
                arr[i][0] = 1
            elif x[i] > rat_sh[0] and x[i] < rat_sh[1]:
                arr[i][0] = (rat_sh[1] - x[i]) / (rat_sh[1] - rat_sh[0])
            else:
                arr[i][0] = 0
        return arr

    # 矩阵2~4列
    def SecondColumn(arr, x, rat_sh, count_line, count_list):
        for i in range(0, count_line):
            for j in range(1, count_list - 1):
                if x[i] > rat_sh[j - 1] and x[i] <= rat_sh[j]:
                    arr[i][j] = (x[i] - rat_sh[j - 1]) / \
                        (rat_sh[j] - rat_sh[j - 1])

                elif x[i] > rat_sh[j] and x[i] <= rat_sh[j + 1]:
                    arr[i][j] = (rat_sh[j + 1] - x[i]) / \
                        (rat_sh[j + 1] - rat_sh[j])

                else:
                    arr[i][j] = 0

        return arr

    # 矩阵最后一列
    def LastColumn(arr, x, rat_sh, count_line, count_list):
        last_list = count_list - 1
        for i in range(0, count_line):
            print(x[i], rat_sh[last_list])
            if x[i] >= rat_sh[last_list]:
                arr[i][last_list] = 1
                print(x[i])

            elif x[i] > rat_sh[last_list - 1] and x[i] < rat_sh[last_list]:
                arr[i][last_list] = (
                    x[i] - rat_sh[last_list - 1]) / (rat_sh[last_list] - rat_sh[last_list - 1])
            else:
                arr[i][last_list] = 0

        return arr

    arr = FirstColumn(arr, x, rat_sh, count_line, count_list)
    arr = SecondColumn(arr, x, rat_sh, count_line, count_list)
    arr = LastColumn(arr, x, rat_sh, count_line, count_list)
    return arr


def CalculateB1(arr):
    w1 = [0.3228, 0.2379, 0.4393]
    w1 = min(w1)
    B1 = []
    temp = 0  # 临时存放矩阵最小值
    for i in range(0, 3):
        temp = min(arr[i])
        B1.append(max(w1, temp))
    return B1

rat_sh = [10, 30, 50, 70, 90]  # 评级阈值

# 将评价值放进去，它就可以自动计算出矩阵，放几个评价值就计算几个
xu_zhou = [40, 54, 97]
su_qian = [70.1, 34, 98, 91, 85, 84, 61]

rule_arr = np.zeros((len(xu_zhou), 5))
rule_arr = Column(rule_arr, xu_zhou, rat_sh, len(xu_zhou), 5)
B1 = CalculateB1(rule_arr)
print(B1)
'''
print(rule_arr)
w1 = [0.3228, 0.2379, 0.4393, 0.4022, 0.5978, 0.4510, 0.5490]

B  = np.dot(w1,rule_arr)
print(B)
'''
