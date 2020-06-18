import os
import sys

class DataGenerator(object):
    """
        文件夹:
            main/class_1
                /class_2
                /class_3
                ...
    """
    def __init__(self, main_dir, num_classes):
        self.__main_dir = main_dir
        self.__num_classes = num_classes




    def load_images_set(self):
        """
            return: [class_1, class_2, class_3, ...]
        """

    def get_classes(self, classes = ""):
        if classes == "":
            folders = os.listdir(self.__main_dir)
            if(len(folders) != self.__num_classes):
                print("Warning:{}".format("folders number is not equal to classes number."))
        else:
            return classes


    def generate(self,file_name, save_dir=""):
        # 输入判断
        if save_dir == "":
            save_dir = self.__main_dir


        # 获得类别


        # 获得文件夹中所有图片路径

        # 生成txt





if __name__ == "__main__":
    pass
