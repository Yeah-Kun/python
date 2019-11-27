import tensorflow as tf


def convolutional(input_data, filters_shape, trainable, name, downsample=False, activate=True, bn=True):
    """
    通用的卷积操作
    :param input_data:
    :param filters_shape:
    :param trainable:
    :param name:
    :param downsample:
    :param activate:
    :param bn:
    :return:
    """
    with tf.variable_scope(name):
        # 1. 判断是否需要进行下采样操作，如果需要，计算padding的大小值
        if downsample:
            # a. 计算需要填充的高度和宽度信息
            pad_h, pad_w = (filters_shape[0] - 2) // 2 + 1, (filters_shape[1] - 2) // 2 + 1
            # b. 构建需要填充的各个维度的大小（仅在H和W上进行填充）
            paddings = tf.constant([[0, 0], [pad_h, pad_h], [pad_w, pad_w], [0, 0]])
            # c. 进行常数0填充
            input_data = tf.pad(input_data, paddings, 'CONSTANT')
            # d. 定义卷积的步长
            strides = (1, 2, 2, 1)
            # e. 定义填充方式
            padding = 'VALID'
        else:
            # a. 定义卷积的步长
            strides = (1, 1, 1, 1)
            # b. 定义填充方式
            padding = "SAME"

        # 2. 定义变量
        weight = tf.get_variable(name='weight', dtype=tf.float32, trainable=True,
                                 shape=filters_shape, initializer=tf.random_normal_initializer(stddev=0.01))

        # 3. 进行卷积操作
        conv = tf.nn.conv2d(input=input_data, filter=weight, strides=strides, padding=padding)

        # 4. 判断是否需要进行批归一化
        if bn:
            # 批归一化处理
            conv = tf.layers.batch_normalization(conv, beta_initializer=tf.zeros_initializer(),
                                                 gamma_initializer=tf.ones_initializer(),
                                                 moving_mean_initializer=tf.zeros_initializer(),
                                                 moving_variance_initializer=tf.ones_initializer(), training=trainable)
        else:
            # 填充偏置项
            bias = tf.get_variable(name='bias', shape=filters_shape[-1], trainable=True,
                                   dtype=tf.float32, initializer=tf.constant_initializer(0.0))
            conv = tf.nn.bias_add(conv, bias)

        # 5. 判断是否需要进行激活函数
        if activate:
            conv = tf.nn.leaky_relu(conv, alpha=0.1)

    # 结果返回
    return conv


def residual_block(input_data, input_channel, filter_num1, filter_num2, trainable, name):
    """
    残差结构
    :param input_data:
    :param input_channel:
    :param filter_num1:
    :param filter_num2:
    :param trainable:
    :param name:
    :return:
    """
    # a. 原始的卷积对象
    short_cut = input_data

    # b. 遍历残差结构
    with tf.variable_scope(name):
        # 1. 第一个卷积
        input_data = convolutional(input_data, filters_shape=(1, 1, input_channel, filter_num1),
                                   trainable=trainable, name='conv1')

        # 2. 第二个卷积
        input_data = convolutional(input_data, filters_shape=(3, 3, filter_num1, filter_num2),
                                   trainable=trainable, name='conv2')

        # 3. 残差结构
        residual_output = input_data + short_cut

    # c. 结果返回
    return residual_output


def route(name, previous_output, current_output):
    with tf.variable_scope(name):
        output = tf.concat([current_output, previous_output], axis=-1)
    return output


def upsample(input_data, name, method="deconv"):
    """
    数据上采样
    :param input_data:
    :param name:
    :param method:
    :return:
    """
    assert method in ["resize", "deconv"]

    if method == "resize":
        with tf.variable_scope(name):
            # 使用Resize的方式上采样成两倍的大小(基于近邻的方式产生)
            input_shape = tf.shape(input_data)
            output = tf.image.resize_nearest_neighbor(input_data, (input_shape[1] * 2, input_shape[2] * 2))

    if method == "deconv":
        # replace resize_nearest_neighbor with conv2d_transpose To support TensorRT optimization
        # 使用反卷积的操作来实现上采样的过程
        numm_filter = input_data.shape.as_list()[-1]
        output = tf.layers.conv2d_transpose(input_data, numm_filter, kernel_size=2, padding='same',
                                            strides=(2, 2), kernel_initializer=tf.random_normal_initializer())

    return output
