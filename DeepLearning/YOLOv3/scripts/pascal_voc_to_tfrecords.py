
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import hashlib
import random
from pathlib import Path

import cv2 as cv
import tensorflow.compat.v1 as tf
from absl import app
import glob

"""

"""

flags = tf.app.flags
flags.DEFINE_string("root_dir", "", "Root directory to raw PASCAL VOC dataset.")
flags.DEFINE_string("set", "train", 'Convert training set, validation set or '
                    'test set.')
flags.DEFINE_string('annotations_dir', 'Annotations',
                    '(Relative) path to annotations directory.')
flags.DEFINE_string('images_dir', 'JPEGImages',
                    '(Relative) path to images directory.')
flags.DEFINE_string('label_path', 'ImageSets/Main', 
                    '(not Relative!) path to labels.txt, label.txt contains all the label name.')
flags.DEFINE_string('label_dir', 'labels', 
                    '(Relative) path to labels directory.')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('class_path', 'class.names', 
                    '(Relative) Path to class file')
flags.DEFINE_string('h', '', 
                    'example: python pascal_voc_to_tfrecords.py \
                    --root_dir=D:/Company/DeepLearningFloorTile/class_1/biaoqian/point_label/VOC2018 \
                    --class_path=point.names')
FLAGS = flags.FLAGS

SETS = ['train', 'val', 'trainval', 'test']
CLASS = {} # 格式：{ "0":class1, "1":class2, "2":class3, ...}

def bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def bytes_list_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=value))


def float_list_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))


def int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def int64_list_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))




def get_tf_example(label_list, image_path):
    """构造tfrecords数据
        label_list：标注信息，<line, line, line, ...>
            line：标注数据，<class xmin ymin xmax ymax>
        image_path：图像路径
    """
    # 变量初始化
    class_text = []
    labels = []
    xmin = []
    ymin = []
    xmax = []
    ymax = []
    global CLASS


    # 读取图像
    with tf.io.gfile.GFile(image_path, 'rb') as fib:
        image_encoded = fib.read()
    try:
        image = cv.imread(image_path)
        image_format = image_path.split(".")[-1]
        h, w, _ = cv.imread(image_path).shape
        key = hashlib.sha256(image_encoded).hexdigest()
    except Exception as e:
        print(e)
        return None

    # 读参数
    for line in label_list:
        item = line.replace("\n", "").split(' ')
        class_text.append(CLASS[item[0]].encode('utf8'))
        labels.append(int(item[0]))

        xmin.append(float(item[1]))
        ymin.append(float(item[2]))
        xmax.append(float(item[3]))
        ymax.append(float(item[4]))

    # 构造example
    example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': int64_feature(h),
        'image/width': int64_feature(w),
        'image/filename': bytes_feature(image_path.encode('utf8')),
        'image/source_id': bytes_feature(image_path.encode('utf8')),
        'image/key/sha256': bytes_feature(key.encode('utf8')),
        'image/encoded': bytes_feature(image_encoded),
        'image/format': bytes_feature(image_format.encode('utf8')),
        'image/object/bbox/xmin': float_list_feature(xmin),
        'image/object/bbox/xmax': float_list_feature(xmax),
        'image/object/bbox/ymin': float_list_feature(ymin),
        'image/object/bbox/ymax': float_list_feature(ymax),
        'image/object/class/text': bytes_list_feature(class_text),
        'image/object/class/label': int64_list_feature(labels),
    }))

    return example


def DirNotExist(path):
    return not os.path.exists(path)

def FileNotExist(path):
    return not os.path.isfile(path)


def get_class(class_path):
    dict_class = {}
    with open(class_path, "r") as f:
        all_class_name = f.readlines()
    for i, class_name in enumerate(all_class_name):
        class_name = class_name.replace("\n", "")
        if(class_name != ""):
            dict_class.update({str(i): class_name})
    
    return dict_class


def dict_label_and_image(labels_name, labels_txt, images_path):
    """
        labels_name：main目录下txt文件
        labels_txt：列表，标注数据的绝对路径
        iamges_path：列表，图像数据的绝对路径

        return: {label_name: [label_txt_path, image_path], ...}
    """
    dict_label_image = {}
    for name in labels_name:
        for label_txt_path in labels_txt:
            if(name in label_txt_path):
                dict_label_image.update({name:[label_txt_path]})
                break

        
        for image_path in images_path:
            if(name in image_path):
                dict_label_image[name].append(image_path)
                break

    return dict_label_image


def main(_):
    """

    """
    # 获得路径
    root_dir = FLAGS.root_dir
    set_name = FLAGS.set
    annotations_dir = os.path.join(root_dir, FLAGS.annotations_dir)
    images_dir = os.path.join(root_dir, FLAGS.images_dir)
    label_dir = os.path.join(root_dir, FLAGS.label_dir)
    class_path = os.path.join(root_dir, FLAGS.class_path)
    
    if ".txt" not in  FLAGS.label_path:
        label_path = os.path.join(root_dir, FLAGS.label_path, set_name + ".txt")
    else:
        label_path = FLAGS.label_path

    if FLAGS.output_path == "":
        output_path = set_name + ".tfrecord"
    else:
        output_path = FLAGS.output_path
    
    # 输入判断
    if DirNotExist(root_dir):
        raise ValueError("root dir not found.")
    elif DirNotExist(annotations_dir):
        raise ValueError("annotations dir not found.")
    elif DirNotExist(images_dir):
        raise ValueError("images dir not found.")
    elif DirNotExist(label_dir):
        raise ValueError("label dir not found.")
    elif FileNotExist(class_path):
        raise ValueError("class file not exist, path:", class_path)
    elif FileNotExist(label_path):
        raise ValueError("label file not exist, path:", label_path)

    

    # 创建TFRecordWriter对象
    writer = tf.python_io.TFRecordWriter(output_path)

    # 读class类别
    global CLASS
    CLASS = get_class(class_path)

    # 读ImageSets/Main中的txt（etc train.txt）
    labels_name = []
    with open(label_path, "r") as f:
        labels_name = f.readlines()
    labels_name = [name.replace("\n", "") for name in labels_name ]


    # 读JPEGImages的图像path
    dataset_images_path = glob.glob(images_dir + "/*.jpg")


    # 读标签数据
    labels_txt = glob.glob(label_dir + "/*.txt")


    # 构造label和image的对应关系
    dict_dataset = dict_label_and_image(labels_name, labels_txt, dataset_images_path)
    print("numbers of dict_dataset:", len(dict_dataset))

    # 构造数据
    data_num = 0
    for key in dict_dataset:
        if ( len(dict_dataset[key]) == 2):
            label_txt_path, image_path = dict_dataset[key]

            with open(label_txt_path, "r") as f:
                labels = f.readlines()
                tf_example = get_tf_example(labels, image_path)
                if(tf_example != None):
                    writer.write(tf_example.SerializeToString())
                    data_num += 1

    writer.close()
    print("data number: ", data_num)

if __name__ == '__main__':
  tf.app.run()


