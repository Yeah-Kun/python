from easydict import EasyDict as edict

__C = edict()
# Consumers can get config by: from config import cfg


# YOLO options
__C.YOLO = edict()

# Set the class name
__C.YOLO.CLASSES = "./data/classes/plate.names"
# __C.YOLO.CLASSES = "data/classes/8_edge.names"
# __C.YOLO.ANCHORS = "./data/anchors/basline_anchors.txt"
__C.YOLO.ANCHORS = "./data/anchors/floor_edge_anchors.txt"
__C.YOLO.MOVING_AVE_DECAY = 0.9995
__C.YOLO.STRIDES = [8, 16, 32]
__C.YOLO.ANCHOR_PER_SCALE = 3 # 每个尺度下的anchor数
__C.YOLO.IOU_LOSS_THRESH = 0.5
__C.YOLO.UPSAMPLE_METHOD = "resize"
__C.YOLO.ORIGINAL_WEIGHT = "./checkpoint/yolov3_coco.ckpt"
__C.YOLO.DEMO_WEIGHT = "./checkpoint/yolov3_coco_demo.ckpt"

# Train options
__C.TRAIN = edict()

# __C.TRAIN.ANNOT_PATH = "./data/dataset/voc_train.txt"
# __C.TRAIN.ANNOT_PATH = "./data/dataset/plate_train.txt"
__C.TRAIN.ANNOT_PATH = "./data/dataset/edge_train.txt"
__C.TRAIN.BATCH_SIZE = 16
__C.TRAIN.INPUT_SIZE = [320, 352, 384, 416, 448, 480, 512, 544, 576, 608]
__C.TRAIN.DATA_AUG = True
__C.TRAIN.LEARN_RATE_INIT = 1e-5
__C.TRAIN.LEARN_RATE_END = 1e-7
__C.TRAIN.WARMUP_EPOCHS = 2
__C.TRAIN.FISRT_STAGE_EPOCHS = 0
__C.TRAIN.SECOND_STAGE_EPOCHS = 500
# __C.TRAIN.INITIAL_WEIGHT = "./checkpoint/yolov3_coco_demo.ckpt"
__C.TRAIN.INITIAL_WEIGHT = "./checkpoint/yolov3_test_loss=4.4321.ckpt-71"
__C.TRAIN.WITH_ANGLE = False

# TEST options
__C.TEST = edict()

# __C.TEST.ANNOT_PATH = "./data/dataset/voc_test.txt"
__C.TEST.ANNOT_PATH = "./data/dataset/edge_test.txt"
# __C.TEST.ANNOT_PATH = "./data/dataset/plate_test.txt"
__C.TEST.BATCH_SIZE = 1
__C.TEST.INPUT_SIZE = 544
__C.TEST.DATA_AUG = False
__C.TEST.WRITE_IMAGE = True
__C.TEST.WRITE_IMAGE_PATH = "./data/detection/"
__C.TEST.WRITE_IMAGE_SHOW_LABEL = True
# __C.TEST.WEIGHT_FILE = "./checkpoint/yolov3_test_loss=1.3356.ckpt-42"
# __C.TEST.WEIGHT_FILE = "./checkpoint/yolov3_test_loss=1.2124.ckpt-818"
__C.TEST.WEIGHT_FILE = "./checkpoint/yolov3_coco_demo.ckpt"
__C.TEST.SHOW_LABEL = True
__C.TEST.SCORE_THRESHOLD = 0.23
__C.TEST.IOU_THRESHOLD = 0.45

cfg = __C
