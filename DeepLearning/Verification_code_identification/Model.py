"""
	验证码识别模型
	create by Ian in 2018-4-13 16:57:10
"""
from save_image_into_h5py import TransImg
import h5py
import numpy as np
import tensorflow as tf
from tensorflow.python.framework import ops
from tensorflow.python import debug as tf_debug
from cnn_utils import *
import matplotlib.pyplot as plt
import scipy
from PIL import Image
from scipy import ndimage
import math
from tensorflow.python import debug as tfdbg

class CaptchaRecognition(object):
	"""docstring for CaptchaRecognition
	"""
	def __init__(self, text_len, char_set):
		super(CaptchaRecognition, self).__init__()
		self.train_path = None
		self.test_path = None
		self.X_train = None
		self.Y_train = None
		self.X_test = None
		self.Y_test = None
		self.text_len = text_len
		self.char_set = char_set
		self.char_set_len = len(char_set)
	


	def text2vec(self, text):
		"""字符串文本转向量
		"""
		vector = np.zeros(self.text_len * self.char_set_len) # 字符串向量，也是输出层向量

		def char2pos(c):
			"""字符转成字符集相应的序号"""
			for i in range(self.char_set_len):
				if c == self.char_set[i]:
					return i

			raise ValueError('No Map')

		for i, c in enumerate(text):
			idx = i * self.char_set_len + char2pos(c) # 为1的向量序号
			vector[idx] = 1

		return vector

	def vec2text(self, vec):
		"""向量转字符串文本
		"""
		char_pos = vec.nonzero()[0] #nonzero是numpy的函数，返回数组中非零元素索引值的数组
		text = []
		for i, c in enumerate(char_pos):
			text.append(self.char_set[c])

		return "".join(text)


	def load_datasets(self, train_path, test_path):
		"""加载训练集和测试集，并进行预处理
		"""
		self.train_path = train_path
		self.test_path = test_path
		train_dataset = h5py.File(train_path, 'r')
		train_set_x_orig = np.array(train_dataset["train_set"][:])
		train_set_y_orig = np.array(train_dataset["train_setlabels"][:])


		test_dataset = h5py.File(test_path, 'r')
		test_set_x_orig = np.array(test_dataset["test_set"][:])
		test_set_y_orig = np.array(test_dataset["test_setlabels"][:])

		#数据归一化和重塑形状
		self.X_train = train_set_x_orig/255.
		self.X_test = test_set_x_orig/255.
		train_set_y_orig = train_set_y_orig.T
		test_set_y_orig = test_set_y_orig.T
		self.Y_train = np.zeros((len(train_set_y_orig), 144))
		self.Y_test = np.zeros((len(test_set_y_orig), 144))

		#将数据集字符串转换为相对应的向量
		for i in range(len(train_set_y_orig)):
			self.Y_train[i][0] = i
			self.Y_train[i] = self.text2vec(train_set_y_orig[i])

		for i in range(len(test_set_y_orig)):
			self.Y_test[i][0] = i
			self.Y_test[i] = self.text2vec(test_set_y_orig[i])

		print("X_train shape: " + str(self.X_train.shape))
		print("Y_train shape: " + str(self.Y_train.shape))
		print("X_test shape: " + str(self.X_test.shape))
		print("Y_test shape: " + str(self.Y_test.shape)) 


	def create_placeholders(self, n_H0, n_W0, n_C0, n_y):
		"""创建占位符，存储x和y的输入值
		"""
		X = tf.placeholder(tf.float32, name = 'X',shape=(None, n_H0, n_W0, n_C0))
		Y = tf.placeholder(tf.float32, name = 'Y', shape=(None, n_y))
		return X, Y


	def init_parameters(self):
		W1 = tf.get_variable("W1", [11,11,3,48], initializer = tf.contrib.layers.xavier_initializer(seed = 1))  
		b1 = tf.get_variable("b1", [48], initializer = tf.zeros_initializer())  
		W2 = tf.get_variable("W2", [5,5,48,96], initializer = tf.contrib.layers.xavier_initializer(seed = 1))  
		b2 = tf.get_variable("b2", [96], initializer = tf.zeros_initializer())
		W3 = tf.get_variable("W3", [3,3,96,128], initializer = tf.contrib.layers.xavier_initializer(seed = 1))  
		b3 = tf.get_variable("b3", [128], initializer = tf.zeros_initializer()) 

		parameters = {"W1":W1, "W2":W2, "b1":b1, "b2":b2, "W3":W3, "b3":b3}
		return parameters



	def forward_propagation(self, X, parameters):
		"""定义模型，使用LeNet-5，不过卷积层改用AlexNet的参数
		"""
		#keep_prob = 0.8
		# 两个卷积层
		W1 = parameters['W1']
		b1 = parameters['b1']
		W2 = parameters['W2']
		b2 = parameters['b2']
		W3 = parameters['W3']
		b3 = parameters['b3']
		with tf.name_scope("conv"):
			conv1 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(X, W1, strides=[1, 4, 4, 1], padding = 'VALID'), b1))
			conv1 = tf.nn.max_pool(conv1, ksize=[1, 3, 3, 1], strides=[1, 1, 1, 1], padding='SAME')

			conv2 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv1, W2, strides=[1, 1, 1, 1], padding='SAME'), b2))
			conv2 = tf.nn.max_pool(conv2, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')

			conv3 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv2, W3, strides=[1, 1, 1, 1], padding='SAME'), b3))
			conv3 = tf.nn.max_pool(conv3, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')
			conv3 = tf.contrib.layers.flatten(conv3)

		with tf.name_scope("output"):
			w_out = tf.Variable(0.01*tf.random_normal([3*3*128*self.text_len, self.text_len*self.char_set_len]))
			b_out = tf.Variable(0.1*tf.random_normal([self.text_len*self.char_set_len]))
			out = tf.add(tf.matmul(conv3, w_out), b_out)

		tf.summary.histogram("W1", W1)
		tf.summary.histogram("b1", b1)
		tf.summary.histogram("W2", W2)
		tf.summary.histogram("b2", b2)
		tf.summary.histogram("W3", W3)
		tf.summary.histogram("b3", b3)
		tf.summary.histogram("w_out", w_out)
		tf.summary.histogram("b_out", b_out)
		return out



	def crack_captcha_cnn(self, X, w_alpha=0.01, b_alpha=0.1):
	 
		# 3 conv layer
		with tf.name_scope("conv"):
			w_c1 = tf.Variable(w_alpha*tf.random_normal([3, 3, 3, 32]))
			b_c1 = tf.Variable(b_alpha*tf.random_normal([32]))
			conv1 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(X, w_c1, strides=[1, 1, 1, 1], padding='SAME'), b_c1))
			conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

			
			w_c2 = tf.Variable(w_alpha*tf.random_normal([3, 3, 32, 64]))
			b_c2 = tf.Variable(b_alpha*tf.random_normal([64]))
			conv2 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv1, w_c2, strides=[1, 1, 1, 1], padding='SAME'), b_c2))
			conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

			
			w_c3 = tf.Variable(w_alpha*tf.random_normal([3, 3, 64, 64]))
			b_c3 = tf.Variable(b_alpha*tf.random_normal([64]))
			conv3 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv2, w_c3, strides=[1, 1, 1, 1], padding='SAME'), b_c3))
			conv3 = tf.nn.max_pool(conv3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
	 
		with tf.name_scope("Fully_connected"):
			w_d = tf.Variable(w_alpha*tf.random_normal([8*18*64, 1024]))
			b_d = tf.Variable(b_alpha*tf.random_normal([1024]))
			dense = tf.contrib.layers.flatten(conv3)
			dense = tf.nn.relu(tf.add(tf.matmul(dense, w_d), b_d))

	 
		with tf.name_scope("output"):
			w_out = tf.Variable(w_alpha*tf.random_normal([1024, self.text_len*self.char_set_len]))
			b_out = tf.Variable(b_alpha*tf.random_normal([self.text_len*self.char_set_len]))
			out = tf.add(tf.matmul(dense, w_out), b_out)
			print(out)
		tf.summary.histogram("w_out", w_out)
		tf.summary.histogram("b_out", b_out)
		#out = tf.nn.softmax(out)

		return out



	def compute_cost(self, Y_hat, Y):
		"""损失函数计算
		"""
		with tf.name_scope("cost"):
			#cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits = Y_hat, labels = Y))
			cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits = Y_hat, labels = Y))
			#cost = tf.reduce_mean(tf.square(Y-Y_hat))
		tf.summary.scalar("cost", cost)
		return cost


	def tensorflow_model(self, learning_rate = 0.009, num_epochs = 4, minibatch_size = 128, print_cost = True):
		"""整合各个步骤
		"""
		ops.reset_default_graph()
		(m, n_H0, n_W0, n_C0) = self.X_train.shape # 读取训练集的宽高和channels
		n_y = self.Y_train.shape[1] # 读取标签预测值
		seed = 3 # 用于随机数
		costs = []

		with tf.device('/gpu:0'):
			X, Y = self.create_placeholders(n_H0, n_W0, n_C0, n_y)
			parameters = self.init_parameters()
			Y_hat = self.forward_propagation(X, parameters)
			#Y_hat = self.crack_captcha_cnn(X)
			cost = self.compute_cost(Y_hat, Y)
			optimizer = tf.train.AdamOptimizer(learning_rate = learning_rate).minimize(cost)
			init = tf.global_variables_initializer()

		saver = tf.train.Saver(parameters) # 保存模型
		
		with tf.Session() as sess:
			sess = tfdbg.LocalCLIDebugWrapperSession(sess) # 被调试器封装的会话
			sess.add_tensor_filter("has_inf_or_nan", tfdbg.has_inf_or_nan)  # 调试器添加过滤规则
			writer = tf.summary.FileWriter(r'D:\code\python\DeepLearning\tmp', tf.get_default_graph()) # 将运行概要写入硬盘
			merged_summary = tf.summary.merge_all() # 将所有的概要打包
			sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)) #log_device_placement：将设备信息展示在控制台
			sess.run(init)
			for epoch in range(num_epochs):
				minibatch_cost = 0
				num_minibatches = int(m / minibatch_size) # 计算一共有多少mini-batch
				#seed = seed + 1
				minibatches = random_mini_batches(self.X_train, self.Y_train, minibatch_size, seed) # 随机混淆数据

				# 从数据集中抽取数据，并进行迭代
				for minibatch in minibatches:
					(minibatch_X, minibatch_Y) = minibatch
					_ , temp_cost, summary, Y_hat_result = sess.run([optimizer, cost, merged_summary, Y_hat], feed_dict={X: minibatch_X, Y: minibatch_Y})
					writer.add_summary(summary, epoch) # 将数据填入tensorboard

					minibatch_cost += temp_cost / num_minibatches

					print(Y_hat_result)
					sess.run(tf.Print(Y_hat_result, [Y_hat_result], message="输出层："))
				
					#print(Y_hat.eval())


				#debugtext = sess.run(tf.Print(cost, [cost], message="输出层：")) # 调试语句
				#print(debugtext[0] ,debugtext.shape)

				if print_cost == True and epoch % 1 == 0:
					costs.append(minibatch_cost)
					if print_cost == True and epoch % 1 == 0:  
						print ("Cost after epoch %i: %f" % (epoch, minibatch_cost))
						if  epoch % 50 == 0:
							saver.save(sess, './model/model.ckpt', global_step=epoch) # 保存模型


		plt.plot(np.squeeze(costs))
		plt.ylabel('cost')  
		plt.xlabel('iterations (per tens)')  
		plt.title("Learning rate =" + str(learning_rate))  
		plt.show()

		parameters = sess.run(parameters)  
		print ("Parameters have been trained!")

		correct_prediction = tf.equal(Y_hat, Y) # equal:判断矩阵是否一致
		accuracy = tf.reduce_mean(tf.cast(correct_prediction, bool))
		print ("Train Accuracy:", accuracy.eval(session=sess, feed_dict={X: self.X_train[:300], Y: self.Y_train[:300]}))
		print ("Test Accuracy:", accuracy.eval(session=sess, feed_dict={X: self.X_test, Y: self.Y_test}))
		return parameters



	def predict(self):
		"""
		"""
		n_y = self.Y_test.shape[1] # 读取标签预测值
		
		with tf.Session() as sess:
			(m, n_H0, n_W0, n_C0) = self.X_test.shape # 读取训练集的宽高和channels
			print(self.X_test.shape)
			X, Y = self.create_placeholders(n_H0, n_W0, n_C0, n_y)
			parameters = self.init_parameters()
			Y_hat = self.forward_propagation(X, parameters)

		tf.reset_default_graph()
		saver = tf.train.import_meta_graph('./model/model.ckpt-2100.meta')
		with tf.Session() as sess:
			# 加载模型
			saver.restore(sess, tf.train.latest_checkpoint("./model")) 
			text_list = sess.run(Y_hat, feed_dict={X: self.X_test})
			print(type(text_list))
			print(text_list)
			print(text_list.shape)

			




if __name__ == '__main__':
	train_path = "./datasets/train_vcode.h5"
	test_path = "./datasets/test_vcode.h5"
	char_set = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z']
	c = CaptchaRecognition(4, char_set)
	c.load_datasets(train_path, test_path)
	#c.tensorflow_model(learning_rate = 0.001, num_epochs= 50, minibatch_size=128)
	c.predict()