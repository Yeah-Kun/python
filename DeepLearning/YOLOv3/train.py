import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"    
import time
import shutil
import numpy as np

from tqdm import tqdm

import tensorflow as tf

import core.utils as utils
from core.dataset import Dataset
from core.yolov3 import YOLOV3
from core.config import cfg


class YoloTrain(object):
    def __init__(self):
        # 每一层上Anchor的数目
        self.anchor_per_scale = cfg.YOLO.ANCHOR_PER_SCALE
        # 类别
        self.classes = utils.read_class_names(cfg.YOLO.CLASSES)
        # 类别数目
        self.num_classes = len(self.classes)
        # 初始化学习率
        self.learn_rate_init = cfg.TRAIN.LEARN_RATE_INIT
        # 最小学习率
        self.learn_rate_end = cfg.TRAIN.LEARN_RATE_END
        # 第一阶段的阶段数
        self.first_stage_epochs = cfg.TRAIN.FISRT_STAGE_EPOCHS
        # 第二阶段的阶段数
        self.second_stage_epochs = cfg.TRAIN.SECOND_STAGE_EPOCHS
        # 学习率变化参数
        self.warmup_periods = cfg.TRAIN.WARMUP_EPOCHS
        # 模型训练持久化恢复对应的文件路径
        self.initial_weight = cfg.TRAIN.INITIAL_WEIGHT
        # 当前时间信息
        self.time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        # 滑动平均的系数值(用于训练数据对应的滑动平均系数)
        self.moving_ave_decay = cfg.YOLO.MOVING_AVE_DECAY
        # 每个尺度最多允许的边框数目
        self.max_bbox_per_scale = 150
        # 训练数据所在的文件路径
        self.train_logdir = "./data/log/train"
        # 加载训练数据
        # TODO： 修改为支持自己数据的形式
        self.trainset = Dataset('train')
        # 加载测试数据
        self.testset = Dataset('test')
        # 总训练数据
        self.steps_per_period = len(self.trainset)
        # 构建会话对象
        self.sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))

        # 定义网络输入
        # 注输出是置信度和边框，也就是一个输入对应两个输出，在这里就是6个输出
        with tf.name_scope('define_input'):
            self.input_data = tf.placeholder(dtype=tf.float32, name='input_data')
            self.label_sbbox = tf.placeholder(dtype=tf.float32, name='label_sbbox') # 候选框
            self.label_mbbox = tf.placeholder(dtype=tf.float32, name='label_mbbox')
            self.label_lbbox = tf.placeholder(dtype=tf.float32, name='label_lbbox')
            self.true_sbboxes = tf.placeholder(dtype=tf.float32, name='sbboxes') # 位置信息
            self.true_mbboxes = tf.placeholder(dtype=tf.float32, name='mbboxes')
            self.true_lbboxes = tf.placeholder(dtype=tf.float32, name='lbboxes')
            self.trainable = tf.placeholder(dtype=tf.bool, name='training')#是训练还是测试

        # 定义网络及损失函数
        with tf.name_scope("define_loss"):
            # 构建模型
            self.model = YOLOV3(self.input_data, self.trainable)

            # 获取网络中所有的模型变量
            self.net_var = tf.global_variables()

            # 构建计算位置、可信度以及概率损失函数
            self.giou_loss, self.conf_loss, self.prob_loss = self.model.compute_loss(
                self.label_sbbox, self.label_mbbox, self.label_lbbox,
                self.true_sbboxes, self.true_mbboxes, self.true_lbboxes)

            # 三个损失函数合并成一个损失函数
            self.loss = self.giou_loss + self.conf_loss + self.prob_loss

        with tf.name_scope('learn_rate'):
            # 构建一个全局变量对象
            self.global_step = tf.Variable(1.0, dtype=tf.float64, trainable=False, name='global_step')

            # 学习率变化阈值(默认两个批次之前)
            warmup_steps = tf.constant(self.warmup_periods * self.steps_per_period,
                                       dtype=tf.float64, name='warmup_steps')
            # 总训练步骤
            train_steps = tf.constant((self.first_stage_epochs + self.second_stage_epochs) * self.steps_per_period,
                                      dtype=tf.float64, name='train_steps')

            # 在两个批次之前，如果训练迭代次数小于阈值，那么设置为初始概率的一部分。
            # 当批次超过阈值之后，做一个学习率转换
            self.learn_rate = tf.cond(
                pred=self.global_step < warmup_steps,#刚开始学习率大，train_steps和warmup_steps为固定值
                true_fn=lambda: self.global_step / warmup_steps * self.learn_rate_init,
                false_fn=lambda: self.learn_rate_end + 0.5 * (self.learn_rate_init - self.learn_rate_end) *
                                 (1 + tf.cos(
                                     (self.global_step - warmup_steps) / (train_steps - warmup_steps) * np.pi))
            )

            # 定义全局步骤变量更新参数
            global_step_update = tf.assign_add(self.global_step, 1.0)

        # 定义模型参数滑动平均更新(目的：为了让模型参数更加平滑)
        with tf.name_scope("define_weight_decay"):
            moving_ave = tf.train.ExponentialMovingAverage(self.moving_ave_decay) \
                .apply(tf.trainable_variables())

        # 第一阶段的模型训练相关参数设置
        with tf.name_scope("define_first_stage_train"):
            # 获取第一阶段模型训练相关参数
            self.first_stage_trainable_var_list = []
            for var in tf.trainable_variables():
                var_name = var.op.name
                var_name_mess = str(var_name).split('/')
                if var_name_mess[0] in ['conv_sbbox', 'conv_mbbox', 'conv_lbbox']:
                    self.first_stage_trainable_var_list.append(var)

            # 第一阶段的模型优化器
            first_stage_optimizer = tf.train.AdamOptimizer(self.learn_rate) \
                .minimize(self.loss, var_list=self.first_stage_trainable_var_list)

            # 加入依赖控制
            # 先做BN的更新操作、在进行模型训练/步骤参数更新、最终更新模型参数值
            with tf.control_dependencies(tf.get_collection(tf.GraphKeys.UPDATE_OPS)):# 批归一化
                with tf.control_dependencies([first_stage_optimizer, global_step_update]):
                    with tf.control_dependencies([moving_ave]):
                        # 定义一个训练操作(实际上不做任何操作，仅仅触发所有操作)
                        self.train_op_with_frozen_variables = tf.no_op()

        # 第二阶段的模型训练相关参数设置
        with tf.name_scope("define_second_stage_train"):
            # 获取第二阶段的相关训练参数(所有训练参数)
            second_stage_trainable_var_list = tf.trainable_variables()

            # 构建第二阶段的优化器对象
            second_stage_optimizer = tf.train.AdamOptimizer(self.learn_rate) \
                .minimize(self.loss, var_list=second_stage_trainable_var_list)

            # 加入依赖控制
            # 先做BN的更新操作、在进行模型训练/步骤参数更新、最终更新模型参数值
            with tf.control_dependencies(tf.get_collection(tf.GraphKeys.UPDATE_OPS)):
                with tf.control_dependencies([second_stage_optimizer, global_step_update]):
                    with tf.control_dependencies([moving_ave]):
                        # 定义一个训练操作(实际上不做任何操作，仅仅触发所有操作)
                        self.train_op_with_all_variables = tf.no_op()

        with tf.name_scope('loader_and_saver'):
            # 定义模型加载对象以及模型持久化对象
            self.loader = tf.train.Saver(self.net_var) # 仅加载网络参数(也就是前向过程中的所有参数)
            self.saver = tf.train.Saver(tf.global_variables(), max_to_keep=3)

        with tf.name_scope('summary'):
            # 可视化相关内容
            tf.summary.scalar("learn_rate", self.learn_rate)
            tf.summary.scalar("giou_loss", self.giou_loss)
            tf.summary.scalar("conf_loss", self.conf_loss)
            tf.summary.scalar("prob_loss", self.prob_loss)
            tf.summary.scalar("total_loss", self.loss)

            # 可视化日志文件构建
            logdir = "./data/log2/"
            if os.path.exists(logdir):
                shutil.rmtree(logdir)
            os.mkdir(logdir)

            # 输出可视化对象
            self.write_op = tf.summary.merge_all()
            self.summary_writer = tf.summary.FileWriter(logdir, graph=self.sess.graph)

        print("初始化完成.....")

    def train(self):
        # 初始化变量
        self.sess.run(tf.global_variables_initializer())

        # 进行模型变量加载(当前代码仅支持加载网络结构对应的模型参数)
        try:
            # 加载模型变量
            print('=> Restoring weights from: %s ... ' % self.initial_weight)
            self.loader.restore(self.sess, self.initial_weight)
        except:
            # 加载模型变量失败(重新开始训练<没有第一阶段的快速逼近>)
            print('=> %s does not exist !!!' % self.initial_weight)
            print('=> Now it starts to train YOLOV3 from scratch ...')
            self.first_stage_epochs = 0

        # 迭代训练
        for epoch in range(1, 1 + self.first_stage_epochs + self.second_stage_epochs):
            # a. 加载训练对象
            if epoch <= self.first_stage_epochs:
                train_op = self.train_op_with_frozen_variables
            else:
                train_op = self.train_op_with_all_variables

            # b. 输出进度条对象构建(传入对象的迭代器对象<支持next和has_next方法>)
            pbar = tqdm(self.trainset)

            # c. 训练、测试各个阶段的损失函数列表
            train_epoch_loss, test_epoch_loss = [], []

            # d. 遍历输出变量
            for train_data in pbar:
                # 1. 训练模型
                _, summary, train_step_loss, global_step_val = self.sess.run(
                    [train_op, self.write_op, self.loss, self.global_step], feed_dict={
                        self.input_data: train_data[0],
                        self.label_sbbox: train_data[1],
                        self.label_mbbox: train_data[2],
                        self.label_lbbox: train_data[3],
                        self.true_sbboxes: train_data[4],
                        self.true_mbboxes: train_data[5],
                        self.true_lbboxes: train_data[6],
                        self.trainable: True,
                    })

                # 2. 加载可视化相关信息
                train_epoch_loss.append(train_step_loss)
                self.summary_writer.add_summary(summary, global_step_val)
                pbar.set_description("train loss: %.2f" % train_step_loss)

            # e. 测试数据效果评估
            for test_data in self.testset:
                # 1. 获取测试数据的损失函数
                test_step_loss = self.sess.run(self.loss, feed_dict={
                    self.input_data: test_data[0],
                    self.label_sbbox: test_data[1],
                    self.label_mbbox: test_data[2],
                    self.label_lbbox: test_data[3],
                    self.true_sbboxes: test_data[4],
                    self.true_mbboxes: test_data[5],
                    self.true_lbboxes: test_data[6],
                    self.trainable: False,
                })

                # 2. 测试数据效果保存
                test_epoch_loss.append(test_step_loss)

            # f. 求平均损失信息    
            train_epoch_loss, test_epoch_loss = np.mean(train_epoch_loss), np.mean(test_epoch_loss)

            # g. 模型持久化相关对象设置
            ckpt_file = "./checkpoint/yolov3_test_loss=%.4f.ckpt" % test_epoch_loss
            log_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print("=> Epoch: %2d Time: %s Train loss: %.2f Test loss: %.2f Saving %s ..."
                  % (epoch, log_time, train_epoch_loss, test_epoch_loss, ckpt_file))
            self.saver.save(self.sess, ckpt_file, global_step=epoch)


if __name__ == '__main__':
    YoloTrain().train()
