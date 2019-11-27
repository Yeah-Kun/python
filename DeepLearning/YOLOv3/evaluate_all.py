import cv2
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"  
import shutil
import numpy as np
import tensorflow as tf
import core.utils as utils
from core.config import cfg
from core.yolov3 import YOLOV3
import glob


class YOLOTest(object):
    def __init__(self):
        self.input_size = cfg.TEST.INPUT_SIZE
        self.anchor_per_scale = cfg.YOLO.ANCHOR_PER_SCALE
        self.classes = utils.read_class_names(cfg.YOLO.CLASSES)
        self.num_classes = len(self.classes)
        self.anchors = np.array(utils.get_anchors(cfg.YOLO.ANCHORS))
        self.score_threshold = cfg.TEST.SCORE_THRESHOLD
        self.iou_threshold = cfg.TEST.IOU_THRESHOLD
        self.moving_ave_decay = cfg.YOLO.MOVING_AVE_DECAY
        self.annotation_path = cfg.TEST.ANNOT_PATH
        self.weight_file = cfg.TEST.WEIGHT_FILE
        self.write_image = cfg.TEST.WRITE_IMAGE
        self.write_image_path = cfg.TEST.WRITE_IMAGE_PATH
        self.show_label = cfg.TEST.SHOW_LABEL

        with tf.name_scope('input'):
            self.input_data = tf.placeholder(dtype=tf.float32, name='input_data')
            self.trainable = tf.placeholder(dtype=tf.bool, name='trainable')

        model = YOLOV3(self.input_data, self.trainable)
        self.pred_sbbox, self.pred_mbbox, self.pred_lbbox = model.pred_sbbox, model.pred_mbbox, model.pred_lbbox

        with tf.name_scope('ema'):
            ema_obj = tf.train.ExponentialMovingAverage(self.moving_ave_decay)

        self.sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
        self.saver = tf.train.Saver(ema_obj.variables_to_restore())
        self.saver.restore(self.sess, self.weight_file)

    def predict(self, image):

        org_image = np.copy(image)
        org_h, org_w, _ = org_image.shape

        image_data = utils.image_preporcess(image, [self.input_size, self.input_size])
        image_data = image_data[np.newaxis, ...]

        pred_sbbox, pred_mbbox, pred_lbbox = self.sess.run(
            [self.pred_sbbox, self.pred_mbbox, self.pred_lbbox],
            feed_dict={
                self.input_data: image_data,
                self.trainable: False
            }
        )

        pred_bbox = np.concatenate([np.reshape(pred_sbbox, (-1, 5 + self.num_classes)),
                                    np.reshape(pred_mbbox, (-1, 5 + self.num_classes)),
                                    np.reshape(pred_lbbox, (-1, 5 + self.num_classes))], axis=0)
        bboxes = utils.postprocess_boxes(pred_bbox, (org_h, org_w), self.input_size, self.score_threshold)
        bboxes = utils.nms(bboxes, self.iou_threshold)

        return bboxes


    def detect_dir(self, origin_dir, save_dir):
        """
            检测整个目录
        """
        if not os.path.exists(origin_dir):
            print("can not find the images dir, path:", origin_dir)
            raise ValueError
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        # 遍历
        images_path = glob.glob( os.path.join(origin_dir, "*.??g") )
        if(len(images_path) == 0):
            print("directory haven't images.")
            return

        for path in images_path:
            image = cv2.imread(path)
            # 检测
            if( image is not None and len(image.shape) == 3):
                bboxes_pr = self.predict(image)
            else:
                continue
            # 输出
            print(bboxes_pr)

            # 绘制
            image = utils.draw_bbox(image, bboxes_pr)

            # 保存
            path = os.path.basename(path)
            save_path = os.path.join(save_dir, path)
            cv2.imwrite(save_path, image)


    def detect_and_rotate_dir(self, origin_dir, save_dir):
        """
            检测整个目录的图像，并旋转
        """
        pass



if __name__ == '__main__':
    # origin path
    origin_dir = "C:/Users/BZL/Desktop/new/test_tile_191113_1"

    # save path
    save_dir = "C:/Users/BZL/Desktop/new/test_tile"
    
    yolo = YOLOTest()
    yolo.detect_dir(origin_dir, save_dir)


