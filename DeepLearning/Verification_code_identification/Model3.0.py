"""
	验证码识别模块3.0
	create by Ian in 2018-8-6 17:46:32
"""

import os
import tensorflow as tf 
from PIL import Image
from nets import nets_factory
import numpy as np


# 不同字符数量
CHAR_SET_LEN = 36
# 图片高度
IMAGE_HEIGHT = 60 
# 图片宽度
IMAGE_WIDTH = 140  
# 批次
BATCH_SIZE = 128
# tfrecord文件存放路径
TFRECORD_FILE = "./tmp/train.tfrecords"

keep_prob = 0.5

# placeholder
x = tf.placeholder(tf.float32, [None, 224, 224])  
y0 = tf.placeholder(tf.float32, [None]) 
y1 = tf.placeholder(tf.float32, [None]) 
y2 = tf.placeholder(tf.float32, [None]) 
y3 = tf.placeholder(tf.float32, [None])


# 学习率
lr = tf.Variable(0.003, dtype=tf.float32)


# 从tfrecord读出数据
def read_and_decode(filename):
    # 根据文件名生成一个队列
    filename_queue = tf.train.string_input_producer([filename])
    reader = tf.TFRecordReader()
    # 返回文件名和文件
    _, serialized_example = reader.read(filename_queue)   
    features = tf.parse_single_example(serialized_example,
                                       features={
                                           'image' : tf.FixedLenFeature([], tf.string),
                                           'label0': tf.FixedLenFeature([], tf.int64),
                                           'label1': tf.FixedLenFeature([], tf.int64),
                                           'label2': tf.FixedLenFeature([], tf.int64),
                                           'label3': tf.FixedLenFeature([], tf.int64),
                                       })
    # 获取图片数据
    image = tf.decode_raw(features['image'], tf.uint8)
    # tf.train.shuffle_batch必须确定shape
    image = tf.reshape(image, [224, 224])
    # 图片预处理
    image = tf.cast(image, tf.float32) / 255.0
    image = tf.subtract(image, 0.5) # 为什么要先减再乘，暂时不理解
    image = tf.multiply(image, 2.0)
    # 获取label
    label0 = tf.cast(features['label0'], tf.int32)
    label1 = tf.cast(features['label1'], tf.int32)
    label2 = tf.cast(features['label2'], tf.int32)
    label3 = tf.cast(features['label3'], tf.int32)

    return image, label0, label1, label2, label3


def forward_propagation(X):
    """
    	定义模型，使用AlexNet
    """
    W1 = tf.get_variable("W1", [11,11,1,64], initializer = tf.contrib.layers.xavier_initializer(seed = 1))  
    b1 = tf.get_variable("b1", [64], initializer = tf.zeros_initializer())  
    W2 = tf.get_variable("W2", [5,5,64,192], initializer = tf.contrib.layers.xavier_initializer(seed = 1))  
    b2 = tf.get_variable("b2", [192], initializer = tf.zeros_initializer())
    W3 = tf.get_variable("W3", [3,3,192,384], initializer = tf.contrib.layers.xavier_initializer(seed = 1))  
    b3 = tf.get_variable("b3", [384], initializer = tf.zeros_initializer())
    W4 = tf.get_variable("W4", [3,3,384,384], initializer = tf.contrib.layers.xavier_initializer(seed = 1))  
    b4 = tf.get_variable("b4", [384], initializer = tf.zeros_initializer())
    W5 = tf.get_variable("W5", [3,3,384,256], initializer = tf.contrib.layers.xavier_initializer(seed = 1))  
    b5 = tf.get_variable("b5", [256], initializer = tf.zeros_initializer())



    with tf.name_scope("conv"):
    	conv1 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(X, W1, strides=[1, 4, 4, 1], padding = 'VALID'), b1))
    	max_pool1 = tf.nn.max_pool(conv1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')
    	#max_pool1 = tf.nn.batch_normalization(max_pool1)

    	conv2 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(max_pool1, W2, strides=[1, 1, 1, 1], padding='SAME'), b2))
    	max_pool2 = tf.nn.max_pool(conv2, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')

    	conv3 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(max_pool2, W3, strides=[1, 1, 1, 1], padding='SAME'), b3))

    	conv4 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv3, W4, strides=[1, 1, 1, 1], padding='SAME'), b4))
    	
    	conv5 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv4, W5, strides=[1, 1, 1, 1], padding='SAME'), b5))
    	max_pool3 = tf.nn.max_pool(conv5, ksize=[1, 3, 3, 1], strides=[1, 3, 3, 1], padding='SAME')

    	# tf.summary.scalar("W1", W1)
    	# tf.summary.scalar("W2", W2)
    	# tf.summary.scalar("W3", W3)
    	# tf.summary.scalar("W4", W4)
    	# tf.summary.scalar("W5", W5)
    	# tf.summary.scalar("b1", b1)
    	# tf.summary.scalar("b2", b2)
    	# tf.summary.scalar("b3", b3)
    	# tf.summary.scalar("b4", b4)
    	# tf.summary.scalar("b5", b5)
    # with tf.name_scope("dense"):
    # 	dense1 = tf.layers.dense(max_pool3, 4096)
    # 	dense2 = tf.layers.dense(dense1, 1024)

    W6 = tf.get_variable("W6", [5,5,256,4096], initializer = tf.contrib.layers.xavier_initializer(seed = 1))  
    b6 = tf.get_variable("b6", [4096], initializer = tf.zeros_initializer())
    W7 = tf.get_variable("W7", [1,1,4096,3072], initializer = tf.contrib.layers.xavier_initializer(seed = 1))  
    b7 = tf.get_variable("b7", [3072], initializer = tf.zeros_initializer())
    # 运用卷积代替了全连接层
    with tf.name_scope("fully_connected"):
    	conv6 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(max_pool3, W6, strides=[1, 1, 1, 1], padding = 'VALID'), b6))
    	#conv6 = tf.nn.dropout(conv6, keep_prob)
    	conv7 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv6, W7, strides=[1, 1, 1, 1], padding='SAME'), b7))
    	#conv7 = tf.nn.dropout(conv7, keep_prob)


    out_W0 = tf.get_variable("out_W0", [1,1,3072,36], initializer = tf.contrib.layers.xavier_initializer(seed = 1))
    out_b0 = tf.get_variable("out_b0", [36], initializer = tf.zeros_initializer())
    out_W1 = tf.get_variable("out_W1", [1,1,3072,36], initializer = tf.contrib.layers.xavier_initializer(seed = 1))
    out_b1 = tf.get_variable("out_b1", [36], initializer = tf.zeros_initializer())
    out_W2 = tf.get_variable("out_W2", [1,1,3072,36], initializer = tf.contrib.layers.xavier_initializer(seed = 1))
    out_b2 = tf.get_variable("out_b2", [36], initializer = tf.zeros_initializer())
    out_W3 = tf.get_variable("out_W3", [1,1,3072,36], initializer = tf.contrib.layers.xavier_initializer(seed = 1))
    out_b3 = tf.get_variable("out_b3", [36], initializer = tf.zeros_initializer())

    # 输出层
    with tf.name_scope("output"):
    	output_0 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv7, out_W0, strides=[1, 1, 1, 1], padding = 'VALID'), out_b0))
    	output_1 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv7, out_W1, strides=[1, 1, 1, 1], padding = 'VALID'), out_b1))
    	output_2 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv7, out_W2, strides=[1, 1, 1, 1], padding = 'VALID'), out_b2))
    	output_3 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv7, out_W3, strides=[1, 1, 1, 1], padding = 'VALID'), out_b3))

    	output_0 = tf.squeeze(output_0, [1,2], name='fc8_0/squeezed')
    	output_1 = tf.squeeze(output_1, [1,2], name='fc8_1/squeezed')
    	output_2 = tf.squeeze(output_2, [1,2], name='fc8_2/squeezed')
    	output_3 = tf.squeeze(output_3, [1,2], name='fc8_3/squeezed')
    	

    return output_0, output_1, output_2, output_3





if __name__ == '__main__':
	# 获取图片数据和标签
	image, label0, label1, label2, label3 = read_and_decode(TFRECORD_FILE)


	#使用shuffle_batch可以随机打乱
	image_batch, label_batch0, label_batch1, label_batch2, label_batch3 = tf.train.shuffle_batch(
	        [image, label0, label1, label2, label3], batch_size = BATCH_SIZE,
	        capacity = 50000, min_after_dequeue=10000, num_threads=1)



	#定义网络结构
	# train_network_fn = nets_factory.get_network_fn(
	#     'alexnet_v2',
	#     num_classes=CHAR_SET_LEN,
	#     weight_decay=0.0005,
	#     is_training=True)
	
	
	with tf.Session() as sess:
	    config = tf.ConfigProto()
	    #config.gpu_options.per_process_gpu_memory_fraction = 0.9
	    config.gpu_options.allow_growth = True
	    sess = tf.Session(config = config)



	    # 数据输入网络得到输出值
	    #logits0,logits1,logits2,logits3,end_points = train_network_fn(X)
	    # inputs: a tensor of size [batch_size, height, width, channels]
	    X = tf.reshape(x, [BATCH_SIZE, 224, 224, 1])
	    logits0,logits1,logits2,logits3 = forward_propagation(X)
	    
	    # 把标签转成one_hot的形式
	    one_hot_labels0 = tf.one_hot(indices=tf.cast(y0, tf.int32), depth=CHAR_SET_LEN)
	    one_hot_labels1 = tf.one_hot(indices=tf.cast(y1, tf.int32), depth=CHAR_SET_LEN)
	    one_hot_labels2 = tf.one_hot(indices=tf.cast(y2, tf.int32), depth=CHAR_SET_LEN)
	    one_hot_labels3 = tf.one_hot(indices=tf.cast(y3, tf.int32), depth=CHAR_SET_LEN)
	    
	    # 计算loss
	    loss0 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=logits0,labels=one_hot_labels0)) 
	    loss1 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=logits1,labels=one_hot_labels1)) 
	    loss2 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=logits2,labels=one_hot_labels2)) 
	    loss3 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=logits3,labels=one_hot_labels3)) 
	    # 计算总的loss
	    total_loss = (loss0+loss1+loss2+loss3)/4.0
	    tf.summary.scalar("loss0", loss0)
	    tf.summary.scalar("loss1", loss1)
	    tf.summary.scalar("loss2", loss2)
	    tf.summary.scalar("loss3", loss3)
	    tf.summary.scalar("total_loss", total_loss)

	    # 优化total_loss
	    optimizer = tf.train.AdamOptimizer(learning_rate=lr).minimize(total_loss) 
	    
	    # 计算准确率
	    correct_prediction0 = tf.equal(tf.argmax(one_hot_labels0,1),tf.argmax(logits0,1))
	    accuracy0 = tf.reduce_mean(tf.cast(correct_prediction0,tf.float32))
	    
	    correct_prediction1 = tf.equal(tf.argmax(one_hot_labels1,1),tf.argmax(logits1,1))
	    accuracy1 = tf.reduce_mean(tf.cast(correct_prediction1,tf.float32))
	    
	    correct_prediction2 = tf.equal(tf.argmax(one_hot_labels2,1),tf.argmax(logits2,1))
	    accuracy2 = tf.reduce_mean(tf.cast(correct_prediction2,tf.float32))
	    
	    correct_prediction3 = tf.equal(tf.argmax(one_hot_labels3,1),tf.argmax(logits3,1))
	    accuracy3 = tf.reduce_mean(tf.cast(correct_prediction3,tf.float32)) 
	    tf.summary.scalar("accuracy0", accuracy0)
	    tf.summary.scalar("accuracy1", accuracy1)
	    tf.summary.scalar("accuracy2", accuracy2)
	    tf.summary.scalar("accuracy3", accuracy3)

	    # 用于保存模型
	    saver = tf.train.Saver()
	    # 初始化
	    sess.run(tf.global_variables_initializer())
	    
	    # 创建一个协调器，管理线程
	    coord = tf.train.Coordinator()
	    # 启动QueueRunner, 此时文件名队列已经进队
	    threads = tf.train.start_queue_runners(sess=sess, coord=coord)

	    merged = tf.summary.merge_all()
	    writer = tf.summary.FileWriter('./logs',sess.graph)
	    for i in range(50001):
	        # 获取一个批次的数据和标签
	        b_image, b_label0, b_label1 ,b_label2 ,b_label3 = sess.run([image_batch, label_batch0, label_batch1, label_batch2, label_batch3])
	        # 优化模型
	        sess.run(optimizer, feed_dict={x: b_image, y0:b_label0, y1: b_label1, y2: b_label2, y3: b_label3})  
	        
	        
	        # 每迭代10次计算一次loss和准确率  
	        if i % 20 == 0:  
	            # 每迭代2000次降低一次学习率
	            if i%5000 == 0:
	                sess.run(tf.assign(lr, lr/3))
	            summary, acc0,acc1,acc2,acc3,loss_ = sess.run([merged, accuracy0,accuracy1,accuracy2,accuracy3,total_loss],feed_dict={x: b_image,
	                                                                                                                y0: b_label0,
	                                                                                                                y1: b_label1,
	                                                                                                                y2: b_label2,
	                                                                                                                y3: b_label3})  
	            # 记录过程
	            writer.add_summary(summary,i)    
	            learning_rate = sess.run(lr)
	            print ("Iter:%d  Loss:%.3f  Accuracy:%.2f,%.2f,%.2f,%.2f  Learning_rate:%.4f" % (i,loss_,acc0,acc1,acc2,acc3,learning_rate))

	            # 保存模型
	            # if acc0 > 0.90 and acc1 > 0.90 and acc2 > 0.90 and acc3 > 0.90: 
	            if i==50000:
	                saver.save(sess, "./model/new_crack_captcha.model", global_step=i)
	                break
	                
	    # 通知其他线程关闭
	    coord.request_stop()
	    # 其他所有线程关闭之后，这一函数才能返回
	    coord.join(threads)