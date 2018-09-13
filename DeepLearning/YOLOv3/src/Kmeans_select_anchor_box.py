"""
	K-means聚类选出anchor box
	create by Ian in 2018-9-3 15:32:38

	x.shape[0]：样本数
"""
import glob
import h5py
import re
from lxml import etree
import numpy as np
import random


def read_XML(dir_path):
    """
            读取xml文件夹内所有xml文件的内容
    """
    xml_file_list = glob.glob(dir_path + "*.xml")
    if xml_file_list == []:
        raise "读取xml文件夹失败"
    else:
        # 读出所有xml文件的内容
        container = ""
        for path in xml_file_list:
            tree = etree.parse(path)
            tree = etree.tostring(tree)
            container += str(tree)
        return container


def get_coordinates(original_string):
    """
            从xml文件中获得xmin，ymin，xmax，ymax
    """
    xmin = re.findall('<xmin>(\d+)</xmin>', original_string)
    ymin = re.findall('<ymin>(\d+)</ymin>', original_string)
    xmax = re.findall('<xmax>(\d+)</xmax>', original_string)
    ymax = re.findall('<ymax>(\d+)</ymax>', original_string)
    try:
        assert(len(xmin) == len(ymin) and len(ymin) ==
               len(xmax) and len(xmax) == len(ymax))
    except:
        print(len(xmin), len(ymin), len(ymin), len(xmax), len(xmax), len(ymax))
        raise "数据有缺失"
    xmin = [int(i) for i in xmin]
    xmax = [int(i) for i in xmax]
    ymin = [int(i) for i in ymin]
    ymax = [int(i) for i in ymax]

    return np.array([xmin, ymin, xmax, ymax])


def IOU(x, anchorboxs):
    """
            样本x与每个anchor box进行IOU，再返回IOU列表
            x：w,h
            anchorboxs：np.array, [1, cluster_index]
    """
    similarities = []
    k = len(anchorboxs)  # 聚类数量
    for anchor in anchorboxs:
        a_w, a_h = anchor
        w, h = x
        if a_h > h and a_w > w:
            similarity = w * h / (a_w * a_h)
        elif a_w >= w and a_h <= h:
            similarity = w * a_h / (w * h + (a_w - w) * a_h)
        elif a_w <= w and a_h >= h:
            similarity = a_w * h / (w * h + a_w * (a_h - h))
        else:
            similarity = (a_w * a_h) / (w * h)
        similarities.append(similarity)
    return np.array(similarities)


def avg_IOU(x, anchorboxs):
    """
            计算平均IOU
            技术细节：选择最佳anchor进行计算
            x.array, [m, 2]
            anchorboxs：np.array, [1, cluster_index]
    """
    IOU_sum = 0.
    for i in range(x.shape[0]):
        similarity = IOU(x[i], anchorboxs)  # 计算IOU
        index = np.argmax(similarity)  # 计算出最合适簇序号
        IOU_sum += similarity[index]

    return IOU_sum / x.shape[0]


def get_box_wh(X):
    """
            获得数据集所有样本的长宽
            return：np.array, [m, 2]
            m：样本数
            2：w，h
    """
    w = X[2] - X[0]
    h = X[3] - X[1]
    return np.array([w, h]).T


def kmeans(x, cluster_index):
    """
            K-means聚类算法
            cluster_index：聚类数
            x：np.array, [m, 2]
            m：样本数
            2：w，h
    """
    # 随机数，选取cluster_index个样本
    random_number = np.random.randint(0, x.shape[0], size=cluster_index)
    cluster_mu = []  # 均值向量
    for i in random_number:
        cluster_mu.append([x[i][0], x[i][1]])

    cluster_mu_temp = cluster_mu.copy()  # 均值向量集的副本，用来判断是否停止更新
    # 计算距离(IOU)，并将样本划入相对应的簇（cluster）
    counter = 0
    while True:
        C = [[] for i in range(cluster_index)]  # 创建空的簇
        for j in range(x.shape[0]):
            similarity = 1 - IOU(x[j], cluster_mu)  # 计算IOU
            index = np.argmin(similarity)  # 将样本归属到某个簇
            C[index].append(x[j])  # 将样本添加到某个簇

        # 重塑数组,更新mu值
        for i in range(cluster_index):
            C[i] = np.array(C[i])
            cluster_mu[i] = np.mean(C[i], axis=0)  # 求当前均值向量
        counter += 1

        try:
        	if((cluster_mu == np.array(cluster_mu_temp)).all()):
        	    print("计算次数：", counter)
        	    break
        	else:
        	    cluster_mu_temp = cluster_mu.copy()  # 更新均值向量
        except Exception as e:
        	raise "分类失败，原因:" + e


    return cluster_mu


class GenerateLabel(object):
	"""生成数据集类
		根据照片和标签，生成数据集
		支持格式：h5， TFRecord
		
	"""
	def __init__(self, obj_path='./data/'):
		self.__obj_path = obj_path
		
	

	


	def write(self, cluster_result, center_list, k, grid, xmllist, dict_classes,num_true_box, classes=3):
	    """
	    :param cluster_result:  记载每个类的样本的序号
	    :param center_list:     记载每个类的中心点，即平均的宽高
	    :param classes:          我们要识别的类的数量
	    :param k:               每一个 gird cell 的 anchor box 的数量
	    :param grid:            一行(一列)， 有多少个 grid cell
	    :param xmllist:         xml 文件的文件名列表
	    :param dict_classes:    每个目标类及其对应的序号，组成的字典
	    num_true_box:           每张图片最多有多少个true_box
	    """

		f = h5py.File(self.__obj_path + 'train_data.h5', 'w')
		f.create_dataset('images', shape=[len(xmllist), self.height, self.width, 3], dtype=np.uint8)
		f.create_dataset('anchor_labels', shape=[len(xmllist), grid, grid, k, 5 + classes], dtype=np.float32)
		f.create_dataset('true_box_labels', shape=[len(xmllist), num_true_box, 5], dtype=np.float32)

		images = f["images"]
		anchor_labels = f["anchor_labels"]
		true_box_labels = f["true_box_labels"]
		anchor_labels[:] = np.zeros(shape=[len(xmllist), grid, grid, k, 5 + classes], dtype=np.float32)





if __name__ == '__main__':
    xml_dir_path = "../data/label_image/"
    xml_file = read_XML(xml_dir_path)
    data_xy = get_coordinates(xml_file)
    data_wh = get_box_wh(data_xy)
    cluster_mu = kmeans(data_wh, 6)
    print(cluster_mu)
    avg = avg_IOU(data_wh.copy(), cluster_mu)
    print(avg)
