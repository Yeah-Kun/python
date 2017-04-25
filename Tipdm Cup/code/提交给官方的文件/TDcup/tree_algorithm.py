from lxml import etree
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import collections
import math


# 构造队列，用于树的层序遍历
class Queue(object):
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


# 返回矩阵
def TagMatrix(tree, path):

    # 统计标签频数
    def List_Count_Tag(children):
        List_tag = []
        if 'a' in children:
            List_tag.append(children.count('a'))
        else:
            List_tag.append(0)
        if 'div' in children:
            List_tag.append(children.count('div'))
        else:
            List_tag.append(0)
        if 'p' in children:
            List_tag.append(children.count('p'))
        else:
            List_tag.append(0)
        if 'span' in children:
            List_tag.append(children.count('span'))
        else:
            List_tag.append(0)
        if 'img' in children:
            List_tag.append(children.count('img'))
        else:
            List_tag.append(0)
        if 'td' in children:
            List_tag.append(children.count('td'))
        else:
            List_tag.append(0)
        if 'dd' in children:
            List_tag.append(children.count('dd'))
        else:
            List_tag.append(0)
        return List_tag
    tag_save = []
    child_Node = tree.xpath(path + '//*')
    for child in child_Node:
        tag_save.append(child.tag)
    return List_Count_Tag(tag_save)


# 选出标准值
def StandardMatrix(tag_pack, matrix_pack):

        # 标准值的第一个元素，用于选出标准值
    def CountKey(matrix_pack):
        temp = 0
        temp_list = []
        for one in matrix_pack:
            temp_list.append(one[0])
        result_list = collections.Counter(temp_list)
        dict(result_list)
        return max(result_list.items(), key=lambda x: x[1])[0]

    if(len(tag_pack) > 1):
        first_key = CountKey(matrix_pack)
        for i in matrix_pack:
            if(i[0] == first_key):
                standar_matrix = i
                return standar_matrix


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
        down_left_count = down_left_count + hinsA[i] ** 2
        i = i + 1
    i = 0
    while i < len(hinsB):
        down_right_count = down_right_count + hinsB[i] ** 2
        i = i + 1
    return up_count / (math.sqrt(down_left_count) * math.sqrt(down_right_count))

'''
# 目标文件夹路径
path = "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\"


# 读取文件源代码，由于'r'遇到错误，用'rb'就可以成功读取，原因之后再找
file_keep = open(path + "one_url_data.txt", 'rb')
bs0bj = file_keep.read().decode('gb18030') # 解码读取，不然会出现乱码
file_keep.close()
'''

# 算法


def TreeAlgotithm(bs0bj, standard_value):
    tree = etree.HTML(bs0bj)  # 用HTML方法解析文件
    t = tree.getroottree()  # 获得一个节点对应的树,用于使用getpath()函数获得绝对路径，tag_path = t.getpath(body1)
    root = t.getroot()  # 用于存储当前根节点，即爸爸节点
    save_children_tag = Queue()  # 队列，用于存储子节点
    if(root[0].getnext()):
        save_children_tag.enqueue(root[1])
    else:
        return None

    # 初始化
    similar_tag = 0  # 用于计算有多少个相似的儿子对象
    matrix_pack = []  # 矩阵容器，用于存放未进行相似度计算的矩阵
    tag_pack = []  # 标签容器，用于存放未进行相似度计算的标签
    one_path = []  # 用于临时存放某节点的绝对路径
    new_matrix_pack = []  # 矩阵容器，用于存放已经进行相似度计算的矩阵
    new_tag_pack = []  # 标签容器，用于存放相似度高的标签
    test = []  # 观察数据进度

    while(similar_tag > standard_value + 2 or similar_tag < standard_value - 2):

        similar_tag = 0  # 相似节点数初始化
        if (save_children_tag.isEmpty()):
            #           print("栈为空")
            return None
        else:
            root = save_children_tag.dequeue()  # 队列弹栈
        test.append(root.tag)
#       print(root.tag)
#       print(one_path)
        matrix_pack = []  # 矩阵容器，用于存放未进行相似度计算的矩阵
        tag_pack = []  # 标签容器，用于存放未进行相似度计算的标签
        new_matrix_pack = []  # 矩阵容器，用于存放已经进行相似度计算的矩阵
        new_tag_pack = []  # 标签容器，用于存放相似度高的标签

        # 父节点遍历
        for child in root:
            save_children_tag.enqueue(child)
            one_path = t.getpath(child)
            one_matrix = TagMatrix(tree, one_path)  # 获得儿子节点的矩阵

            if(one_matrix[0] < 2 or one_matrix[1] < 2):  # 筛选没可能是楼层的元素
                continue

            # 存储没有进行相似度计算的矩阵和标签
            matrix_pack.append(one_matrix)
            tag_pack.append(child)
        # 选择标准值矩阵
        standar_matrix = StandardMatrix(tag_pack, matrix_pack) 
        print(standar_matrix)
        if(standar_matrix != None):
            i = 0
            for new_one_matrix in matrix_pack:
                Cos_key = CosSimilarity(new_one_matrix, standar_matrix)
                if(Cos_key > 0.90):
                    print(new_one_matrix)
                    print(Cos_key)
                    print(i)
                    new_tag_pack.append(tag_pack[i])
                    new_matrix_pack.append(matrix_pack[i])
                i = i + 1

        similar_tag = len(new_tag_pack)
        print(similar_tag)
        if(similar_tag > standard_value + 2 or similar_tag < standard_value - 2):
            del(matrix_pack)
            del(tag_pack)
            del(new_tag_pack)
            del(new_matrix_pack)
    tag_path = []
    for tag in new_tag_pack:
        tag_path.append(t.getpath(tag))
    return tag_path

#tag_path = TreeAlgotithm(bs0bj)
# print(tag_path)
