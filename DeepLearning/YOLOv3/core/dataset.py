import os
import cv2
import random
import numpy as np
import tensorflow as tf
import core.utils as utils
from core.config import cfg


class Dataset(object):
    """implement Dataset here"""
    def __init__(self, dataset_type):
        self.annot_path = cfg.TRAIN.ANNOT_PATH if dataset_type == 'train' else cfg.TEST.ANNOT_PATH # 通过这个找到annotation的文件
        self.input_sizes = cfg.TRAIN.INPUT_SIZE if dataset_type == 'train' else cfg.TEST.INPUT_SIZE
        self.batch_size = cfg.TRAIN.BATCH_SIZE if dataset_type == 'train' else cfg.TEST.BATCH_SIZE
        self.data_aug = cfg.TRAIN.DATA_AUG if dataset_type == 'train' else cfg.TEST.DATA_AUG

        self.train_input_sizes = cfg.TRAIN.INPUT_SIZE
        self.strides = np.array(cfg.YOLO.STRIDES)
        self.classes = utils.read_class_names(cfg.YOLO.CLASSES)
        self.num_classes = len(self.classes)
        self.anchors = np.array(utils.get_anchors(cfg.YOLO.ANCHORS))
        self.anchor_per_scale = cfg.YOLO.ANCHOR_PER_SCALE
        self.max_bbox_per_scale = 150 # 每个尺度最多允许的边框数目

        self.annotations = self.load_annotations(dataset_type)
        self.num_samples = len(self.annotations)
        self.num_batchs = int(np.ceil(self.num_samples / self.batch_size))
        self.batch_count = 0

    def load_annotations(self, dataset_type):
        with open(self.annot_path, 'r') as f:
            txt = f.readlines()
            annotations = [line.strip() for line in txt if len(line.strip().split()[1:]) != 0]
        np.random.shuffle(annotations)
        return annotations

    def __iter__(self):
        return self

    def __next__(self):
        with tf.device('/cpu:0'):
            self.train_input_size = random.choice(self.train_input_sizes)
            self.train_output_sizes = self.train_input_size // self.strides

            batch_image = np.zeros((self.batch_size, self.train_input_size, self.train_input_size, 3))

            batch_label_sbbox = np.zeros((self.batch_size, self.train_output_sizes[0], self.train_output_sizes[0],
                                          self.anchor_per_scale, 5 + self.num_classes))
            batch_label_mbbox = np.zeros((self.batch_size, self.train_output_sizes[1], self.train_output_sizes[1],
                                          self.anchor_per_scale, 5 + self.num_classes))
            batch_label_lbbox = np.zeros((self.batch_size, self.train_output_sizes[2], self.train_output_sizes[2],
                                          self.anchor_per_scale, 5 + self.num_classes))

            batch_sbboxes = np.zeros((self.batch_size, self.max_bbox_per_scale, 4)) # 4是xywh ？
            batch_mbboxes = np.zeros((self.batch_size, self.max_bbox_per_scale, 4))
            batch_lbboxes = np.zeros((self.batch_size, self.max_bbox_per_scale, 4))

            num = 0
            if self.batch_count < self.num_batchs:
                while num < self.batch_size:
                    index = self.batch_count * self.batch_size + num
                    if index >= self.num_samples:
                        index -= self.num_samples
                    annotation = self.annotations[index]
                    image, bboxes = self.parse_annotation(annotation) # 提取一整行的标注数据（除文件名外）
                    label_sbbox, label_mbbox, label_lbbox, sbboxes, mbboxes, lbboxes = self.preprocess_true_boxes(
                        bboxes)
                    # 将每张的图像标注信息提取出来，放到batch的容器里面
                    batch_image[num, :, :, :] = image
                    batch_label_sbbox[num, :, :, :, :] = label_sbbox
                    batch_label_mbbox[num, :, :, :, :] = label_mbbox
                    batch_label_lbbox[num, :, :, :, :] = label_lbbox
                    batch_sbboxes[num, :, :] = sbboxes # shape = (150, 4)
                    batch_mbboxes[num, :, :] = mbboxes # shape = (150, 4)
                    batch_lbboxes[num, :, :] = lbboxes # shape = (150, 4)
                    num += 1
                self.batch_count += 1
                return batch_image, batch_label_sbbox, batch_label_mbbox, batch_label_lbbox, \
                       batch_sbboxes, batch_mbboxes, batch_lbboxes
            else:
                self.batch_count = 0
                np.random.shuffle(self.annotations)
                raise StopIteration

    def random_horizontal_flip(self, image, bboxes):

        if random.random() < 0.5:
            _, w, _ = image.shape
            image = image[:, ::-1, :]
            bboxes[:, [0, 2]] = w - bboxes[:, [2, 0]]

        return image, bboxes

    def random_crop(self, image, bboxes):

        if random.random() < 0.5:
            h, w, _ = image.shape
            max_bbox = np.concatenate([np.min(bboxes[:, 0:2], axis=0), np.max(bboxes[:, 2:4], axis=0)], axis=-1)

            max_l_trans = max_bbox[0]
            max_u_trans = max_bbox[1]
            max_r_trans = w - max_bbox[2]
            max_d_trans = h - max_bbox[3]

            crop_xmin = max(0, int(max_bbox[0] - random.uniform(0, max_l_trans)))
            crop_ymin = max(0, int(max_bbox[1] - random.uniform(0, max_u_trans)))
            crop_xmax = max(w, int(max_bbox[2] + random.uniform(0, max_r_trans)))
            crop_ymax = max(h, int(max_bbox[3] + random.uniform(0, max_d_trans)))

            image = image[crop_ymin: crop_ymax, crop_xmin: crop_xmax]

            bboxes[:, [0, 2]] = bboxes[:, [0, 2]] - crop_xmin
            bboxes[:, [1, 3]] = bboxes[:, [1, 3]] - crop_ymin

        return image, bboxes

    def random_translate(self, image, bboxes):

        if random.random() < 0.5:
            h, w, _ = image.shape
            max_bbox = np.concatenate([np.min(bboxes[:, 0:2], axis=0), np.max(bboxes[:, 2:4], axis=0)], axis=-1)

            max_l_trans = max_bbox[0]
            max_u_trans = max_bbox[1]
            max_r_trans = w - max_bbox[2]
            max_d_trans = h - max_bbox[3]

            tx = random.uniform(-(max_l_trans - 1), (max_r_trans - 1))
            ty = random.uniform(-(max_u_trans - 1), (max_d_trans - 1))

            M = np.array([[1, 0, tx], [0, 1, ty]])
            image = cv2.warpAffine(image, M, (w, h))

            bboxes[:, [0, 2]] = bboxes[:, [0, 2]] + tx
            bboxes[:, [1, 3]] = bboxes[:, [1, 3]] + ty

        return image, bboxes

    def parse_annotation(self, annotation):

        line = annotation.split()
        image_path = line[0]
        if not os.path.exists(image_path):
            raise KeyError("%s does not exist ... " % image_path)
        image = np.array(cv2.imread(image_path))
        bboxes = np.array([list(map(int, box.split(','))) for box in line[1:]])# [xmin, ymin, xmax, ymax, label]

        #数据增强
        if self.data_aug:
            # image, bboxes = self.random_horizontal_flip(np.copy(image), np.copy(bboxes)) # 水平翻转
            image, bboxes = self.random_crop(np.copy(image), np.copy(bboxes)) # 裁剪
            image, bboxes = self.random_translate(np.copy(image), np.copy(bboxes)) # 平移

        image, bboxes = utils.image_preporcess(np.copy(image), [self.train_input_size, self.train_input_size],
                                               np.copy(bboxes))
        return image, bboxes

    def bbox_iou(self, boxes1, boxes2):
        """
            boxes1: 标注框，[cx, cy, w, h]，其中w,h经过某个尺度stride的处理
            boxes2: 先验框（同一尺度下，多个）[[cx, cy, w, h], [...], [...]]
        """
        boxes1 = np.array(boxes1)
        boxes2 = np.array(boxes2)

        boxes1_area = boxes1[..., 2] * boxes1[..., 3]
        boxes2_area = boxes2[..., 2] * boxes2[..., 3]

        # 还原成[xmin, ymin, xmax, ymax]
        boxes1 = np.concatenate([boxes1[..., :2] - boxes1[..., 2:] * 0.5,
                                 boxes1[..., :2] + boxes1[..., 2:] * 0.5], axis=-1)
        boxes2 = np.concatenate([boxes2[..., :2] - boxes2[..., 2:] * 0.5,
                                 boxes2[..., :2] + boxes2[..., 2:] * 0.5], axis=-1)

        left_up = np.maximum(boxes1[..., :2], boxes2[..., :2])
        right_down = np.minimum(boxes1[..., 2:], boxes2[..., 2:])

        inter_section = np.maximum(right_down - left_up, 0.0)
        inter_area = inter_section[..., 0] * inter_section[..., 1]
        union_area = boxes1_area + boxes2_area - inter_area

        return inter_area / union_area
    

    def preprocess_true_boxes(self, bboxes):
        """
            input:
                bboxes: bounding box的数据, 
                    [[xmin, ymin, xmax, ymax, classes], [xmin, ymin, xmax, ymax, classes], ..]

            将标注信息提取出来，并分配合适的Anchors
            如果anchor和Ground-truth Bounding Boxes的 IOU相差过大，则直接使用最大的anchor作为Ground-truth Bounding Boxes 的 anchor
        """
        label = [np.zeros((self.train_output_sizes[i], self.train_output_sizes[i], self.anchor_per_scale,
                           5 + self.num_classes)) for i in range(3)] # 初始化3个尺度的label
        bboxes_xywh = [np.zeros((self.max_bbox_per_scale, 4)) for _ in range(3)] # 初始化3个尺度的xywh
        bbox_count = np.zeros((3,))

        for bbox in bboxes:
            bbox_coor = bbox[:4] # 获得bbox的xywh
            bbox_class_ind = bbox[4] # 获得类别的index

            onehot = np.zeros(self.num_classes, dtype=np.float) # onehot表示类别
            onehot[bbox_class_ind-1] = 1.0 # onehot对应类别置为1，其余为0
            uniform_distribution = np.full(self.num_classes, 1.0 / self.num_classes) # 根据类别数量生成正态分布图
            deta = 0.01 
            smooth_onehot = onehot * (1 - deta) + deta * uniform_distribution # 平滑一下onehot

            bbox_xywh = np.concatenate([(bbox_coor[2:] + bbox_coor[:2]) * 0.5, bbox_coor[2:] - bbox_coor[:2]], axis=-1) # 左上角右下角点转换成xywh
            bbox_xywh_scaled = 1.0 * bbox_xywh[np.newaxis, :] / self.strides[:, np.newaxis] # 经过3个不同尺度的缩放

            iou = []
            exist_positive = False
            for i in range(3): # 3个不同尺度（从大到小），选择合适的anchors（iou > 0.3）
                anchors_xywh = np.zeros((self.anchor_per_scale, 4)) # 单一尺度下，多个anchor的xywh
                anchors_xywh[:, 0:2] = np.floor(bbox_xywh_scaled[i, 0:2]).astype(np.int32) + 0.5 # 因为anchors只保留wh，所以这里采用bbox的xy
                anchors_xywh[:, 2:4] = self.anchors[i] # 直接采用anchors的wh

                iou_scale = self.bbox_iou(bbox_xywh_scaled[i][np.newaxis, :], anchors_xywh)
                iou.append(iou_scale)
                iou_mask = iou_scale > 0.3

                if np.any(iou_mask): # 如何判断这个类是否是正样本？ 只要 Ground-truth Bounding Boxes 和 Anchors的IOU > 0.3，则认为是正样本
                    # 根据真实框的坐标信息来计算所属网格左上角的位置
                    xind, yind = np.floor(bbox_xywh_scaled[i, 0:2]).astype(np.int32)

                    label[i][yind, xind, iou_mask, :] = 0
                    # 填充真实框的中心位置和宽高
                    label[i][yind, xind, iou_mask, 0:4] = bbox_xywh
                    # 设定置信度为 1.0，表明该网格包含物体
                    label[i][yind, xind, iou_mask, 4:5] = 1.0
                    # 设置网格内 anchor 框的类别概率，做平滑处理
                    label[i][yind, xind, iou_mask, 5:] = smooth_onehot

                    bbox_ind = int(bbox_count[i] % self.max_bbox_per_scale) # ?
                    bboxes_xywh[i][bbox_ind, :4] = bbox_xywh # ？
                    bbox_count[i] += 1

                    exist_positive = True

            if not exist_positive: # 规则 2: 所有 iou 都不大于0.3， 那么只能选择 iou 最大的
                best_anchor_ind = np.argmax(np.array(iou).reshape(-1), axis=-1) # 找到iou最大的框的index
                best_detect = int(best_anchor_ind / self.anchor_per_scale) # 最大的iou属于哪个尺度
                best_anchor = int(best_anchor_ind % self.anchor_per_scale) # 哪一个尺度的第几个
                xind, yind = np.floor(bbox_xywh_scaled[best_detect, 0:2]).astype(np.int32) # 获得iou最大的

                # 将bbox的信息填入label，其他都为0
                label[best_detect][yind, xind, best_anchor, :] = 0
                label[best_detect][yind, xind, best_anchor, 0:4] = bbox_xywh
                label[best_detect][yind, xind, best_anchor, 4:5] = 1.0
                label[best_detect][yind, xind, best_anchor, 5:] = smooth_onehot

                bbox_ind = int(bbox_count[best_detect] % self.max_bbox_per_scale)
                bboxes_xywh[best_detect][bbox_ind, :4] = bbox_xywh
                bbox_count[best_detect] += 1

        label_sbbox, label_mbbox, label_lbbox = label
        sbboxes, mbboxes, lbboxes = bboxes_xywh  # 这个有什么用？

        return label_sbbox, label_mbbox, label_lbbox, sbboxes, mbboxes, lbboxes

    def __len__(self):
        return self.num_batchs



class DatasetAngle(Dataset):
    def __next__(self):
        with tf.device('/cpu:0'):
            self.train_input_size = random.choice(self.train_input_sizes)
            self.train_output_sizes = self.train_input_size // self.strides

            batch_image = np.zeros((self.batch_size, self.train_input_size, self.train_input_size, 3))

            batch_label_sbbox = np.zeros((self.batch_size, self.train_output_sizes[0], self.train_output_sizes[0],
                                          self.anchor_per_scale, 6 + self.num_classes))
            batch_label_mbbox = np.zeros((self.batch_size, self.train_output_sizes[1], self.train_output_sizes[1],
                                          self.anchor_per_scale, 6 + self.num_classes))
            batch_label_lbbox = np.zeros((self.batch_size, self.train_output_sizes[2], self.train_output_sizes[2],
                                          self.anchor_per_scale, 6 + self.num_classes))

            batch_sbboxes = np.zeros((self.batch_size, self.max_bbox_per_scale, 5)) # 5是xywh theta ？
            batch_mbboxes = np.zeros((self.batch_size, self.max_bbox_per_scale, 5))
            batch_lbboxes = np.zeros((self.batch_size, self.max_bbox_per_scale, 5))

            num = 0
            if self.batch_count < self.num_batchs:
                while num < self.batch_size:
                    index = self.batch_count * self.batch_size + num
                    if index >= self.num_samples:
                        index -= self.num_samples
                    annotation = self.annotations[index]
                    image, bboxes = self.parse_annotation(annotation) # 提取一整行的标注数据（除文件名外）
                    label_sbbox, label_mbbox, label_lbbox, sbboxes, mbboxes, lbboxes = self.preprocess_true_boxes(
                        bboxes)
                    # 将每张的图像标注信息提取出来，放到batch的容器里面
                    batch_image[num, :, :, :] = image
                    batch_label_sbbox[num, :, :, :, :] = label_sbbox
                    batch_label_mbbox[num, :, :, :, :] = label_mbbox
                    batch_label_lbbox[num, :, :, :, :] = label_lbbox
                    batch_sbboxes[num, :, :] = sbboxes # 这么说这是存储输出结果的容器？
                    batch_mbboxes[num, :, :] = mbboxes 
                    batch_lbboxes[num, :, :] = lbboxes 
                    num += 1
                self.batch_count += 1
                return batch_image, batch_label_sbbox, batch_label_mbbox, batch_label_lbbox, \
                       batch_sbboxes, batch_mbboxes, batch_lbboxes
            else:
                self.batch_count = 0
                np.random.shuffle(self.annotations)
                raise StopIteration


    def random_horizontal_flip(self, image, bboxes):

        if random.random() < 0.5:
            _, w, _ = image.shape
            image = image[:, ::-1, :]
            bboxes[:, [0, 2]] = w - bboxes[:, [2, 0]]

        return image, bboxes

    def random_crop(self, image, bboxes):

        if random.random() < 0.5:
            h, w, _ = image.shape
            max_bbox = np.concatenate([np.min(bboxes[:, 0:2], axis=0), np.max(bboxes[:, 2:4], axis=0)], axis=-1)

            max_l_trans = max_bbox[0]
            max_u_trans = max_bbox[1]
            max_r_trans = w - max_bbox[2]
            max_d_trans = h - max_bbox[3]


            crop_xmin = max(0, int(max_bbox[0] - random.uniform(0, max_l_trans)))
            crop_ymin = max(0, int(max_bbox[1] - random.uniform(0, max_u_trans)))
            crop_xmax = max(w, int(max_bbox[2] + random.uniform(0, max_r_trans)))
            crop_ymax = max(h, int(max_bbox[3] + random.uniform(0, max_d_trans)))

            image = image[crop_ymin: crop_ymax, crop_xmin: crop_xmax]

            bboxes[:, [0, 2]] = bboxes[:, [0, 2]] - crop_xmin
            bboxes[:, [1, 3]] = bboxes[:, [1, 3]] - crop_ymin

        return image, bboxes


    def random_translate(self, image, bboxes):

        if random.random() < 0.5:
            h, w, _ = image.shape
            max_bbox = np.concatenate([np.min(bboxes[:, 0:2], axis=0), np.max(bboxes[:, 2:4], axis=0)], axis=-1)

            max_l_trans = max_bbox[0]
            max_u_trans = max_bbox[1]
            max_r_trans = w - max_bbox[2]
            max_d_trans = h - max_bbox[3]

            tx = random.uniform(-(max_l_trans - 1), (max_r_trans - 1))
            ty = random.uniform(-(max_u_trans - 1), (max_d_trans - 1))

            M = np.array([[1, 0, tx], [0, 1, ty]])
            image = cv2.warpAffine(image, M, (w, h))

            bboxes[:, [0, 2]] = bboxes[:, [0, 2]] + tx
            bboxes[:, [1, 3]] = bboxes[:, [1, 3]] + ty

        return image, bboxes


    def parse_annotation(self, annotation):

        line = annotation.split()
        image_path = line[0]
        if not os.path.exists(image_path):
            raise KeyError("%s does not exist ... " % image_path)
        image = np.array(cv2.imread(image_path))
        # bboxes = np.array([list(map(int, box.split(','))) for box in line[1:]])# [xmin, ymin, xmax, ymax, label]
        bboxes = np.array([list(map(float, box.split(','))) for box in line[1:]])# [xmin, ymin, xmax, ymax, label]

        #数据增强
        # if self.data_aug:
            # image, bboxes = self.random_horizontal_flip(np.copy(image), np.copy(bboxes)) # 水平翻转
            # image, bboxes = self.random_crop(np.copy(image), np.copy(bboxes)) # 裁剪
            # image, bboxes = self.random_translate(np.copy(image), np.copy(bboxes)) # 平移

        image, bboxes = utils.image_preporcess(np.copy(image), [self.train_input_size, self.train_input_size],
                                               np.copy(bboxes))
        return image, bboxes


    def bbox_iou(self, boxes1, boxes2):
        """
            同一个尺度下，多个bbox计算（比如anchor在一个尺度下有3个，则同时计算3个iou）
        """
        boxes1 = np.array(boxes1)
        boxes2 = np.array(boxes2)

        boxes1_area = boxes1[..., 2] * boxes1[..., 3]
        boxes2_area = boxes2[..., 2] * boxes2[..., 3]

        boxes1 = np.concatenate([boxes1[..., :2] - boxes1[..., 2:] * 0.5,
                                 boxes1[..., :2] + boxes1[..., 2:] * 0.5], axis=-1)
        boxes2 = np.concatenate([boxes2[..., :2] - boxes2[..., 2:] * 0.5,
                                 boxes2[..., :2] + boxes2[..., 2:] * 0.5], axis=-1)

        left_up = np.maximum(boxes1[..., :2], boxes2[..., :2])
        right_down = np.minimum(boxes1[..., 2:], boxes2[..., 2:])

        inter_section = np.maximum(right_down - left_up, 0.0)
        inter_area = inter_section[..., 0] * inter_section[..., 1]
        union_area = boxes1_area + boxes2_area - inter_area

        return inter_area / union_area


    def preprocess_true_boxes(self, bboxes):
        """
            input:
                bboxes: bounding box的数据, 
                    [[xmin, ymin, xmax, ymax, angle, classes], [xmin, ymin, xmax, ymax, angle, classes], ..]

            1. 将标注信息提取出来，并分配合适的Anchors
            2. 构建存储预测结果的容器
            如果anchor和Ground-truth Bounding Boxes的 IOU相差过大，则直接使用最大的anchor作为Ground-truth Bounding Boxes 的 anchor
        """
        label = [np.zeros((self.train_output_sizes[i], self.train_output_sizes[i], self.anchor_per_scale,
                           6 + self.num_classes)) for i in range(3)] # 初始化3个尺度的label
        bboxes_xywh = [np.zeros((self.max_bbox_per_scale, 5)) for _ in range(3)] # 初始化3个尺度的xywh
        bbox_count = np.zeros((3,))

        for bbox in bboxes:
            bbox_coor = bbox[:4] # 获得bbox的xywh
            bbox_angle = bbox[4]
            bbox_class_ind = int(bbox[5]) # 获得类别的index

            onehot = np.zeros(self.num_classes, dtype=np.float)
            onehot[bbox_class_ind-1] = 1.0
            uniform_distribution = np.full(self.num_classes, 1.0 / self.num_classes)
            deta = 0.01
            smooth_onehot = onehot * (1 - deta) + deta * uniform_distribution # 平滑一下onehot

            bbox_xywh = np.concatenate([(bbox_coor[2:] + bbox_coor[:2]) * 0.5, bbox_coor[2:] - bbox_coor[:2]], axis=-1) # 左上角右下角点转换成xywh
            bbox_xywh_scaled = 1.0 * bbox_xywh[np.newaxis, :] / self.strides[:, np.newaxis]

            iou = []
            exist_positive = False
            for i in range(3): # 3个不同尺度（从大到小），选择合适的anchors（iou > 0.3）
                anchors_xywh = np.zeros((self.anchor_per_scale, 5))
                anchors_xywh[:, 0:2] = np.floor(bbox_xywh_scaled[i, 0:2]).astype(np.int32) + 0.5
                anchors_xywh[:, 2:4] = self.anchors[i]
                anchors_xywh
                # 1. anchors要加入聚类, 这里的设计与雅丹有出入

                iou_scale = self.bbox_iou(bbox_xywh_scaled[i][np.newaxis, :], anchors_xywh)
                iou.append(iou_scale)
                iou_mask = iou_scale > 0.3

                if np.any(iou_mask): # 如何判断这个类是否是正样本？ 只要 Ground-truth Bounding Boxes 和 Anchors的IOU > 0.3，则认为是正样本
                    # 根据真实框的坐标信息来计算所属网格左上角的位置
                    xind, yind = np.floor(bbox_xywh_scaled[i, 0:2]).astype(np.int32)

                    label[i][yind, xind, iou_mask, :] = 0
                    # 填充真实框的中心位置和宽高
                    label[i][yind, xind, iou_mask, 0:4] = bbox_xywh
                    # angle
                    label[i][yind, xind, iou_mask, 4:5] = bbox_angle # 2. 这里的设计与雅丹有出入
                    # 设定置信度为 1.0，表明该网格包含物体
                    label[i][yind, xind, iou_mask, 5:6] = 1.0
                    # 设置网格内 anchor 框的类别概率，做平滑处理
                    label[i][yind, xind, iou_mask, 6:] = smooth_onehot

                    bbox_ind = int(bbox_count[i] % self.max_bbox_per_scale) # ?
                    bboxes_xywh[i][bbox_ind, :4] = bbox_xywh # ？
                    bboxes_xywh[i][bbox_ind, 4:5] = bbox_angle 
                    bbox_count[i] += 1

                    exist_positive = True

            if not exist_positive: # 规则 2: 所有 iou 都不大于0.3， 那么只能选择 iou 最大的
                best_anchor_ind = np.argmax(np.array(iou).reshape(-1), axis=-1)
                best_detect = int(best_anchor_ind / self.anchor_per_scale)
                best_anchor = int(best_anchor_ind % self.anchor_per_scale)
                xind, yind = np.floor(bbox_xywh_scaled[best_detect, 0:2]).astype(np.int32)

                label[best_detect][yind, xind, best_anchor, :] = 0
                label[best_detect][yind, xind, best_anchor, 0:4] = bbox_xywh
                label[best_detect][yind, xind, best_anchor, 4:5] = bbox_angle
                label[best_detect][yind, xind, best_anchor, 5:6] = 1.0
                label[best_detect][yind, xind, best_anchor, 6:] = smooth_onehot

                bbox_ind = int(bbox_count[best_detect] % self.max_bbox_per_scale)
                bboxes_xywh[best_detect][bbox_ind, :4] = bbox_xywh
                
                bboxes_xywh[best_detect][bbox_ind, 4:5] = bbox_angle
                
                bbox_count[best_detect] += 1

        label_sbbox, label_mbbox, label_lbbox = label
        sbboxes, mbboxes, lbboxes = bboxes_xywh  # 这个有什么用？

        return label_sbbox, label_mbbox, label_lbbox, sbboxes, mbboxes, lbboxes


