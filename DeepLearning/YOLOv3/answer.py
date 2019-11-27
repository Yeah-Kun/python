# -*- coding: UTF-8 -*-
import tensorflow.compat.v1 as tf
import os, sys
import numpy as np
from PIL import Image
import cv2 as cv

def image_processing(image, height, width):
    # 解码图像数据
    image = tf.image.decode_jpeg(image, channels=3)
    # 归一化，归一化区间是[-1, 1]
    image = (tf.cast(image, dtype=tf.float32) - 127.0) / 128.0
    # Resize函数要求是对batch进行，所以先扩增一个维度
    image = tf.expand_dims(image, 0)
    # Resize到指定大小。
    image = tf.image.resize_bilinear(image, [height, width])
    image = tf.squeeze(image, [0])
    return image

def batch_inputs(feature_map, data_files, height=2048, width=2448,
                 batch_size=1, is_train=True, num_readers=1, num_preprocess_threads=4):
    # feature_map: 对应proto的数据映射。
    # data_files: list类型，存放的是tfrecord的文件列表。
    # batch_size: 一个批次batch的大小。
    # is_train: DataProvider在train和test节点的表现形式有所不同，主要test时并不需要一个循环队列。
    # num_reader: 每一个线程reader的个数。
    # num_preprocess_threads: 处理数据的线程的个数。
    with tf.name_scope('reader_defination'):
        # 创建文件队列，如果是训练，创建一个随机文件队列，如果是测试，创建一个顺序文件队列。
        if is_train:
            filename_queue = tf.train.string_input_producer(data_files, shuffle=True, capacity=16)
        else:
            filename_queue = tf.train.string_input_producer(data_files, shuffle=False, capacity=1)
        # reader的个数至少为1。
        num_readers = 1 if num_readers < 1 else num_readers
        
        if num_readers > 1:
            # 定义缓冲池的大小。
            examples_per_shard = 1024
            min_queue_examples = examples_per_shard * 16
            if is_train:
                examples_queue = tf.RandomShuffleQueue(capacity=min_queue_examples + 3 * batch_size,
                                                       min_after_dequeue=min_queue_examples,
                                                       dtypes=[tf.string])
            else:
                examples_queue = tf.FIFOQueue(capacity=examples_per_shard + 3 * batch_size, 
                                              dtypes=[tf.string])
            
            # 多个reader时对reader队列进行管理。
            enqueue_ops = []
            for _ in range(num_readers):
                reader = tf.TFRecordReader()
                _, value = reader.read(filename_queue)
                enqueue_ops.append(examples_queue.enqueue([value]))
            
            tf.train.queue_runner.add_queue_runner(tf.train.queue_runner.QueueRunner(examples_queue, enqueue_ops))
            example_serialized = examples_queue.dequeue()
        else:
            reader = tf.TFRecordReader()
            _, example_serialized = reader.read(filename_queue)
        
        samples = []
        for _ in range(num_preprocess_threads):
            features = tf.parse_single_example(example_serialized, feature_map)
            samples.append([image_processing(features['image/encoded'], height, width), features['image/format']])
            
        batch_data = tf.train.batch_join(samples, batch_size=batch_size,
                                         capacity=2 * num_preprocess_threads * batch_size)
                
        data = tf.reshape(batch_data[0], [batch_size, -1])
        label = tf.reshape(batch_data[1], [batch_size])
        return (data, label)





        
if __name__ == '__main__':
    data_files = [os.path.join(sys.argv[1], f) for f in os.listdir(sys.argv[1])]
    IMAGE_FEATURE_MAP_SUB = {
        'image/width': tf.io.FixedLenFeature([], tf.int64),
        'image/height': tf.io.FixedLenFeature([], tf.int64),
        'image/filename': tf.io.FixedLenFeature([], tf.string),
        'image/source_id': tf.io.FixedLenFeature([], tf.string),
        'image/key/sha256': tf.io.FixedLenFeature([], tf.string),
        'image/encoded': tf.io.FixedLenFeature([], tf.string),
        'image/format': tf.io.FixedLenFeature([], tf.string),
        'image/object/bbox/xmin': tf.io.VarLenFeature(tf.float32),
        'image/object/bbox/ymin': tf.io.VarLenFeature(tf.float32),
        'image/object/bbox/xmax': tf.io.VarLenFeature(tf.float32),
        'image/object/bbox/ymax': tf.io.VarLenFeature(tf.float32),
        'image/object/class/text': tf.io.VarLenFeature(tf.string),
        'image/object/class/label': tf.io.VarLenFeature(tf.int64),
    }

    feature_map = {'label':tf.FixedLenFeature([], dtype=tf.int64, default_value=-1), 
                   'data':tf.FixedLenFeature([], dtype=tf.string)}
    with tf.Graph().as_default(), \
        tf.Session(config=tf.ConfigProto(allow_soft_placement = True)) as session:        
        data, labels = batch_inputs(IMAGE_FEATURE_MAP_SUB, data_files, batch_size=1, is_train=True)
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=session, coord=coord)
        tf.train.start_queue_runners(sess=session)
        for i in range(100):
            data_numpy, labels_numpy = session.run([data, labels])
            for d, l in zip(data_numpy, labels_numpy):
                # 保存成对应的图像。
                d_pixel_vector = (d * 128 + 127).astype(np.uint8)
                d_pixel_2d = np.reshape(d_pixel_vector, [28, 28, -1])
                Image.fromarray(d_pixel_2d).convert('L').save('%d.jpg' %l)
        coord.request_stop()
        coord.join(threads)