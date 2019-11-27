import core.common as common
import tensorflow as tf


def darknet53(input_data, trainable):
    """
    基于输入数据构建Darknet53的网络
    :param input_data:
    :param trainable:
    :return:
    """
    with tf.variable_scope('darknet'):
        # 1. 第一层卷积[3,3,3,32]/1
        input_data = common.convolutional(input_data, filters_shape=(3, 3, 3, 32),
                                          trainable=trainable, name='conv0')
        # 2. 第二层卷积[3,3,32,64]/2
        input_data = common.convolutional(input_data, filters_shape=(3, 3, 32, 64),
                                          trainable=trainable, name='conv1',
                                          downsample=True)
        # 3. 进入残差+卷积的结构
        # a. 第一个残差结构
        for i in range(1):
            # 残差结构，通道数变化情况: 64 -> 32 -> 64
            input_data = common.residual_block(input_data, 64, 32, 64,
                                               trainable=trainable,
                                               name='residual%d' % (i + 0))
        # b. 进入残差后的卷积结构(下采样), [3,3,64,128]/2
        input_data = common.convolutional(input_data, filters_shape=(3, 3, 64, 128),
                                          trainable=trainable, name='conv4', downsample=True)

        # c. 进入第二组残差结构
        for i in range(2):
            # 残差结构, 通道数变化情况: 128->64->128
            input_data = common.residual_block(input_data, 128, 64, 128, trainable=trainable,
                                               name='residual%d' % (i + 1))

        # d. 进入残差后的卷积结构(下采样), [3,3,128,256]/2
        input_data = common.convolutional(input_data, filters_shape=(3, 3, 128, 256),
                                          trainable=trainable, name='conv9', downsample=True)

        # e. 进入第三组残差结构
        for i in range(8):
            # 残差结构, 通道数变化情况: 256->128->256
            input_data = common.residual_block(input_data, 256, 128, 256, trainable=trainable,
                                               name='residual%d' % (i + 3))

        # f. 定义第一个输出分支
        route_1 = input_data

        # g. 进入残差后的卷积结构(下采样), [3,3,256,512]/2
        input_data = common.convolutional(input_data, filters_shape=(3, 3, 256, 512),
                                          trainable=trainable, name='conv26', downsample=True)

        # h. 进入第四组残差结构
        for i in range(8):
            # 残差结构, 通道数变化情况: 512->256->512
            input_data = common.residual_block(input_data, 512, 256, 512, trainable=trainable,
                                               name='residual%d' % (i + 11))

        # i. 定义第二个分支输出
        route_2 = input_data

        # j. 进入残差后的卷积结构(下采样), [3,3,512,1024]/2
        input_data = common.convolutional(input_data, filters_shape=(3, 3, 512, 1024),
                                          trainable=trainable, name='conv43', downsample=True)

        # k. 进入第五组残差结构
        for i in range(4):
            # 残差结构, 通道数变化情况: 1024->512->1024
            input_data = common.residual_block(input_data, 1024, 512, 1024, trainable=trainable,
                                               name='residual%d' % (i + 19))

        # 返回第一分支、第二分支以及最终的结构数据
        return route_1, route_2, input_data
