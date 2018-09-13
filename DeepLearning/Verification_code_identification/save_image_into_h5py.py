"""
    将数据集变成HDF5格式存储起来
    create by Ian in 2018-3-6 16:13:33
"""
import numpy as np
import cv2
import glob
import h5py
import re


class TransImg(object):
    """docstring for TransImg
            将图片转换成相对应的hdf5格式文件

            hdf5path：h5文件路径
            imgpath：图片路径
            shape：图片的形状（行数，列数，通道数），跟opencv的shape一致
    """

    def __init__(self, hdf5path="./", imgpath="./", header='img'):
        self._img_path = imgpath
        self._hdf5_path = hdf5path
        self.shape = None
        self.header = header

    def list_and_label_img(self):
        """将图片的路径变成列表，并提取标签"""
        self.addrs = glob.glob(self._img_path)
        self.labels = []
        for addr in self.addrs:
            self.labels.append(
                re.search(r"(?<=\\)\w+(?=\.)", addr).group(0).encode())


    def create_h5file(self, frame="tf"):
        """建立一个h5的数据集
            frame：框架名
            header：数据集表头名
        """
        img = cv2.imread(self.addrs[0]) # 加载一张图片

        if frame == 'tf':
            self.shape = (len(self.addrs),) + img.shape # 获得数据集的维度

        self.hdf5_file = h5py.File(self._hdf5_path, mode='w')
        self.hdf5_file.create_dataset(self.header, self.shape, np.int8) #建立数据集
        dt = h5py.special_dtype(vlen=str)  # 解决h5读入字符串问题
        self.hdf5_file.create_dataset(
            self.header + "labels", (len(self.labels), ), dtype=dt)

    def load_and_save(self, data_order="tf"):
        """加载图片并且将他们写进h5文件"""

        # 由于cv2加载图片会加载成BGR，所以要转换成RGB，转为灰度图则是GRAY
        for i in range(len(self.addrs)):
            addr = self.addrs[i]
            img = cv2.imread(addr)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # 因为图片轴顺序已经对了，所以一下语句废弃
            # if data_order == "th": # 使用tensorflow
            #     img = np.rollaxis(img, 2) # 使用rollaxis改变图片轴次序
            # 保存图片到数据集
            self.hdf5_file[self.header][i, ...] = img[None]
            #self.hdf5_file[self.header][i, ...] = img

        self.hdf5_file[self.header + "labels"][...] = self.labels
        self.hdf5_file.close()

    def open_and_read(self, path="", header="train_set"):
        """打开h5文件并读取其中的内容"""
        if path == "":
            path = self._hdf5_path
        file = h5py.File(path, "r")
        return file


if __name__ == '__main__':
    train_set_path = "./train_set/*.jpg"
    hdf5_path = './datasets/train_vcode.h5'
    header = "train_set"
    t = TransImg(hdf5_path, train_set_path, header)
    t.list_and_label_img()
    t.create_h5file()
    t.load_and_save()
