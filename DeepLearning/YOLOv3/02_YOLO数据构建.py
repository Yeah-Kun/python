# -- encoding:utf-8 --
"""
Create by ibf on 2019/7/30
"""

import os
import glob
from xml.etree import ElementTree as ET
import numpy as np


def transform_xml_to_own_dataset(output_train_dataset_path, input_images_dir, input_xml_dir, classes_file):
    """
        数据转换
    """
    def filter_fun(line):
        line = line.replace("\n", "")
        if(line != ""):
            return True
        else:
            return False

    if not os.path.exists(output_train_dataset_path):
        raise ValueError("file not found: " + output_train_dataset_path)
    if not os.path.exists(input_xml_dir):
        raise ValueError("file not found: " + input_xml_dir)
    if not os.path.exists(classes_file):
        raise ValueError("file not found: " + classes_file)
    
    # 获得xml
    xml_files = glob.glob( os.path.join(input_xml_dir, "*.xml") )
    print("numbers of xml files:", len(xml_files))

    # 获得类别
    classes = {}
    with open(classes_file, "r") as f:
        info = f.readlines()

    info = filter(filter_fun, info)
    for i, line in enumerate(info):
        c = line.replace("\n", "")
        classes[c] = i

    with open(output_train_dataset_path, "w") as writer:
        # 构建own dataset
        for xml_file in xml_files:
            # 1. 构建数据读取
            tree = ET.parse(xml_file)

            # 2. 得到xml的根节点
            root = tree.getroot()

            # 3. 获取路径信息
            filename = root.find("filename").text

            # 4. 构建路径
            image_file_path = os.path.join(input_images_dir, filename)
            writer.writelines(image_file_path)

            # 5. 加载目标
            for obj in root.findall('object'):
                # a. 得到标签
                label = obj.find('name').text
                label_index = classes[label]

                # b. 获取坐标信息
                bbox = obj.find("bndbox")
                xmin = bbox.find("xmin").text
                ymin = bbox.find("ymin").text
                xmax = bbox.find("xmax").text
                ymax = bbox.find("ymax").text
                # 这里只所以为零，是因为只有一个类需要检测
                writer.writelines(" {},{},{},{},{}".format(xmin, ymin, xmax, ymax, label_index))
            writer.writelines('\n')


# 拆分训练集和测试集
def devide_dataset(output_train_dataset_path, output_test_dataset_path, prop = 0.05):
    """
        划分数据集
    """
    if not os.path.exists(output_train_dataset_path):
        raise ValueError("file not found: " + output_train_dataset_path)

    # 计算关键数据
    num_dataset = len(output_test_dataset_path)
    num_test_set = int(num_dataset * 0.05)
    print("numbers of dataset: {}, numbers of test set:{}".format(num_dataset, num_test_set))

    # 读数据
    data = []
    with open(output_test_dataset_path, "r") as f:
        data = f.readlines()

    # 将数据放到test set


    # 


def main():
    # output
    output_train_dataset_path = "data/dataset/edge_train.txt"
    output_test_dataset_path = "data/dataset/edge_test.txt"

    # input
    input_images_dir = "data/images"
    input_xml_dir = "data/images/datas"
    classes_file = "data/classes/8_edge.names"

    transform_xml_to_own_dataset(output_train_dataset_path, input_images_dir, input_xml_dir, classes_file)

    # devide_dataset(output_train_dataset_path, output_test_dataset_path, 0.05)

if __name__ == "__main__":
    main()
