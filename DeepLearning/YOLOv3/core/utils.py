import cv2
import random
import colorsys
import numpy as np
import tensorflow as tf
from core.config import cfg


def read_class_names(class_file_name):
    """
    loads class name from a file
    加载id和类别名称映射关系，文件中是每行一个类别名称
    :param class_file_name:
    :return:
    """
    names = {}
    with open(class_file_name, 'r') as data:
        for ID, name in enumerate(data):
            names[ID] = name.strip('\n')
    return names


def get_anchors(anchors_path):
    """
    loads the anchors from a file
    加载Anchor Box尺度信息
    :param anchors_path:
    :return:
    """
    with open(anchors_path) as f:
        anchors = f.readline()
    anchors = np.array(anchors.split(','), dtype=np.float32)
    return anchors.reshape(3, 3, 2)


def image_preporcess(image, target_size, gt_boxes=None):
    """
    图像预处理相关操作(Resize&Padding操作)
    :param image:
    :param target_size:
    :param gt_boxes: [[x,y,w,h], [x,y,w,h], ...]
    :return:
    """
    # 1. 图像转换为RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)

    # 2. 获取图像的原始大小以及目标大小
    ih, iw = target_size
    h, w, _ = image.shape

    # 3. 计算缩放比例以及按照该比例缩放后的图像大小
    # 按照宽度、高度的最小比例缩放
    scale = min(iw / w, ih / h)
    nw, nh = int(scale * w), int(scale * h)

    # 4. 图像大小缩放
    image_resized = cv2.resize(image, (nw, nh))

    # 5. 图像填充(因为是按照最小比例缩放的，所有某个方向是大小不达标的)
    # a. 构建一个目标大小的图像(灰度)
    image_paded = np.full(shape=[ih, iw, 3], fill_value=128.0)
    # b. 计算宽度和高度上需要填充的像素点数目(分为两部分)
    dw, dh = (iw - nw) // 2, (ih - nh) // 2
    # c. 数据赋值
    image_paded[dh:nh + dh, dw:nw + dw, :] = image_resized
    # d. 范围转换
    image_paded = image_paded / 255.

    # 6. 对真实边框的位置信息做相同转换操作
    if gt_boxes is None:
        return image_paded
    else:
        # 坐标相同转换方式
        gt_boxes[:, [0, 2]] = gt_boxes[:, [0, 2]] * scale + dw
        gt_boxes[:, [1, 3]] = gt_boxes[:, [1, 3]] * scale + dh
        gt_boxes[:, [-1]] = gt_boxes[:, [-1]]
        return image_paded, gt_boxes


def draw_bbox(image, bboxes, classes=read_class_names(cfg.YOLO.CLASSES), show_label=True):
    """
    bboxes: [x_min, y_min, x_max, y_max, probability, cls_id] format coordinates.
    """

    num_classes = len(classes)
    image_h, image_w, _ = image.shape
    hsv_tuples = [(1.0 * x / num_classes, 1., 1.) for x in range(num_classes)]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))

    random.seed(0)
    random.shuffle(colors)
    random.seed(None)

    for i, bbox in enumerate(bboxes):
        coor = np.array(bbox[:4], dtype=np.int32)
        fontScale = 0.5
        score = bbox[4]
        class_ind = int(bbox[5])
        bbox_color = colors[class_ind]
        bbox_thick = int(0.6 * (image_h + image_w) / 600)
        c1, c2 = (coor[0], coor[1]), (coor[2], coor[3])
        cv2.rectangle(image, c1, c2, bbox_color, bbox_thick)

        if show_label:
            bbox_mess = '%s: %.2f' % (classes[class_ind], score)
            t_size = cv2.getTextSize(bbox_mess, 0, fontScale, thickness=bbox_thick // 2)[0]
            cv2.rectangle(image, c1, (c1[0] + t_size[0], c1[1] - t_size[1] - 3), bbox_color, -1)  # filled

            cv2.putText(image, bbox_mess, (c1[0], c1[1] - 2), cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale, (0, 0, 0), bbox_thick // 2, lineType=cv2.LINE_AA)

    return image


def bboxes_iou(boxes1, boxes2):
    """
    计算边框的IoU的值
    :param boxes1: 格式为[..., 4], 4这个值为: [x_left, y_top, x_right, y_bottom]
    :param boxes2: 格式为[..., 4], 4这个值为: [x_left, y_top, x_right, y_bottom]
    :return:
    """
    # 1. 数据转换
    boxes1 = np.array(boxes1)
    boxes2 = np.array(boxes2)

    # 2. 计算各个区域的面积
    boxes1_area = (boxes1[..., 2] - boxes1[..., 0]) * (boxes1[..., 3] - boxes1[..., 1])
    boxes2_area = (boxes2[..., 2] - boxes2[..., 0]) * (boxes2[..., 3] - boxes2[..., 1])

    # 3. 获取左上角的最大值坐标以及右小角的最小值坐标
    left_up = np.maximum(boxes1[..., :2], boxes2[..., :2])
    right_down = np.minimum(boxes1[..., 2:], boxes2[..., 2:])

    # 4. 当且仅当右下角的坐标值大于左上角的坐标值的时候，存在交叉区域，计算交叉区域面积
    inter_section = np.maximum(right_down - left_up, 0.0)
    inter_area = inter_section[..., 0] * inter_section[..., 1]

    # 5. 计算总面积
    union_area = boxes1_area + boxes2_area - inter_area

    # 6. 计算IoU的值(防止为零)，进行设置
    ious = np.maximum(1.0 * inter_area / union_area, np.finfo(np.float32).eps)

    return ious


def read_pb_return_tensors(graph, pb_file, return_elements):
    """
    pb格式的模型恢复(加载对应的Tensor值)
    :param graph:
    :param pb_file:
    :param return_elements:
    :return:
    """
    with tf.gfile.FastGFile(pb_file, 'rb') as f:
        frozen_graph_def = tf.GraphDef()
        frozen_graph_def.ParseFromString(f.read())

    with graph.as_default():
        return_elements = tf.import_graph_def(frozen_graph_def,
                                              return_elements=return_elements)
    return return_elements


def nms(bboxes, iou_threshold, sigma=0.3, method='nms'):
    """
    :param bboxes: (xmin, ymin, xmax, ymax, score, class)

    Note: soft-nms, https://arxiv.org/pdf/1704.04503.pdf
          https://github.com/bharatsingh430/soft-nms
    """
    # 1. 获取类别列表
    classes_in_img = list(set(bboxes[:, 5]))

    # 2. 定义最优边框列表
    best_bboxes = []

    # 3.遍历所有类别
    for cls in classes_in_img:
        # a. 获取对应类别的边框
        cls_mask = (bboxes[:, 5] == cls)
        cls_bboxes = bboxes[cls_mask]

        # b. 对当前类别的所有边框遍历处理
        while len(cls_bboxes) > 0:
            # 1. 获取概率值最大的边框，并添加到列表中
            max_ind = np.argmax(cls_bboxes[:, 4])
            best_bbox = cls_bboxes[max_ind]
            best_bboxes.append(best_bbox)

            # 2. 获取剩下的边框
            cls_bboxes = np.concatenate([cls_bboxes[: max_ind], cls_bboxes[max_ind + 1:]])

            # 3. 计算最有边框和剩下边框的IoU的值
            iou = bboxes_iou(best_bbox[np.newaxis, :4], cls_bboxes[:, :4])

            # 4. 计算权重系数向量
            weight = np.ones((len(iou),), dtype=np.float32)

            assert method in ['nms', 'soft-nms']

            if method == 'nms':
                # IoU低于阈值的，权重系数设置为0
                iou_mask = iou > iou_threshold
                weight[iou_mask] = 0.0

            if method == 'soft-nms':
                # 进行rbf权重系数更改操作
                weight = np.exp(-(1.0 * iou ** 2 / sigma))

            # 5. 更新边框置信度的值
            cls_bboxes[:, 4] = cls_bboxes[:, 4] * weight

            # 6.获取置信度大于0的边框，循环进行处理
            score_mask = cls_bboxes[:, 4] > 0.
            cls_bboxes = cls_bboxes[score_mask]

    return best_bboxes


def postprocess_boxes(pred_bbox, org_img_shape, input_size, score_threshold):
    valid_scale = [0, np.inf]
    pred_bbox = np.array(pred_bbox)

    pred_xywh = pred_bbox[:, 0:4]
    pred_conf = pred_bbox[:, 4]
    pred_prob = pred_bbox[:, 5:]

    # # (1) (x, y, w, h) --> (xmin, ymin, xmax, ymax)
    pred_coor = np.concatenate([pred_xywh[:, :2] - pred_xywh[:, 2:] * 0.5,
                                pred_xywh[:, :2] + pred_xywh[:, 2:] * 0.5], axis=-1)
    # # (2) (xmin, ymin, xmax, ymax) -> (xmin_org, ymin_org, xmax_org, ymax_org)
    org_h, org_w = org_img_shape
    resize_ratio = min(input_size / org_w, input_size / org_h)

    dw = (input_size - resize_ratio * org_w) / 2
    dh = (input_size - resize_ratio * org_h) / 2

    pred_coor[:, 0::2] = 1.0 * (pred_coor[:, 0::2] - dw) / resize_ratio
    pred_coor[:, 1::2] = 1.0 * (pred_coor[:, 1::2] - dh) / resize_ratio

    # # (3) clip some boxes those are out of range
    pred_coor = np.concatenate([np.maximum(pred_coor[:, :2], [0, 0]),
                                np.minimum(pred_coor[:, 2:], [org_w - 1, org_h - 1])], axis=-1)
    invalid_mask = np.logical_or((pred_coor[:, 0] > pred_coor[:, 2]), (pred_coor[:, 1] > pred_coor[:, 3]))
    pred_coor[invalid_mask] = 0

    # # (4) discard some invalid boxes
    bboxes_scale = np.sqrt(np.multiply.reduce(pred_coor[:, 2:4] - pred_coor[:, 0:2], axis=-1))
    scale_mask = np.logical_and((valid_scale[0] < bboxes_scale), (bboxes_scale < valid_scale[1]))

    # # (5) discard some boxes with low scores
    classes = np.argmax(pred_prob, axis=-1)
    scores = pred_conf * pred_prob[np.arange(len(pred_coor)), classes]
    print(np.max(scores))
    score_mask = scores >= score_threshold
    mask = np.logical_and(scale_mask, score_mask)
    coors, scores, classes = pred_coor[mask], scores[mask], classes[mask]

    return np.concatenate([coors, scores[:, np.newaxis], classes[:, np.newaxis]], axis=-1)


def reflect_xywh2rect_v1(bboxes):
    """
        input:
            bboxes: np.array(),[[x,y,w,h], [x,y,w,h], ...]
        
        return:
            rect: np.array(), [[p1, p2, p3, p4], ...], 顺时针
                p:[x,y]
    """
    rects = []
    for bbox in bboxes:
        left_up = bbox[:2] - bbox[2:] * 0.5
        right_bottom = bbox[:2] + bbox[2:] * 0.5
        p1 = left_up
        p2 = np.array([left_up[1], right_bottom[0]])
        p3 = right_bottom
        p4 = np.array([left_up[0], right_bottom[1]])
        rects.append(np.array([p1, p2, p3, p4]))
    
    return np.array(rects)

 
def rotate_rect(rects, rad_angle):
    """
        rects: np.array(), [[p1, p2, p3, p4], ...], 逆时针
                p:[x,y]
        rad_angle: 矩形框旋转角度，弧度制
    """
    rotate_matrix = np.matrix([[np.cos(rad_angle), -np.sin(rad_angle)], 
                              [np.sin(rad_angle), np.cos(rad_angle)]])
    
    rotate_rects = []
    for rect in rects:
        xy = np.matrix((rect[2] - rect[0]) * 0.5).T
        
        rotate_rect = []
        for p in rect:
            r_p = rotate_matrix.T * np.matrix(p - xy) + xy
            rotate_rect.append(np.array(r_p))
        rotate_rects.append(np.array(rotate_rect))

    return np.array(rotate_rects)


def calc_rotate_bbox_iou(bboxes1, bboxes2):
    """
        计算旋转框的iou，默认第一个为标注框，第二个为anchors
        
        input:
            bboxes1: np.array([[x,  y,  w ,  h, angle]])
            bboxes2: np.array([[x,  y,  w ,  h, angle],
                               [x,  y,  w ,  h, angle],
                               [x,  y,  w ,  h, angle]])
            
        
        return: np.array([iou_1, iou_2, iou_3, ...] ),
                例子：[0.13695256, 0.2936727 , 0.1788403 ]
            
    """
    def SutherlandHodgman(subjectPolygon, clipPolygon):
        """
            注意：输入的必须是顺时针
        """
        def inside(p):
            return (cp2[0] - cp1[0]) * (p[1] - cp1[1]) - (cp2[1] - cp1[1]) * (p[0] - cp1[0]) < -1e-10

        def computeIntersection():
            dc = [cp1[0] - cp2[0], cp1[1] - cp2[1]]
            dp = [s[0] - e[0], s[1] - e[1]]
            n1 = cp1[0] * cp2[1] - cp1[1] * cp2[0]
            n2 = s[0] * e[1] - s[1] * e[0]
            n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
            return [(n1 * dp[0] - n2 * dc[0]) * n3, (n1 * dp[1] - n2 * dc[1]) * n3]

        outputList = subjectPolygon
        cp1 = clipPolygon[-1]

        for clipVertex in clipPolygon:
            cp2 = clipVertex
            inputList = outputList
            outputList = []
            try:
                s = inputList[-1]
            except Exception as e:
                return []

            for subjectVertex in inputList:
                e = subjectVertex
                if inside(e):
                    if not inside(s):
                        outputList.append(computeIntersection())
                    outputList.append(e)
                elif inside(s):
                    outputList.append(computeIntersection())
                s = e
            cp1 = cp2

        # 去重
        only_output = []
        for p in outputList:
            if p not in only_output:
                only_output.append(p)
        return only_output

    def polygon_area(P):
        """
            多边形面积
        """
        n = len(P)
        P.append(P[0])
        S = 0
        for i in range(0, n):
            S = S + (P[i][0] + P[i + 1][0]) * (P[i + 1][1] - P[i][1])
        return 0.5 * abs(S)

    def reflect_xywht2rect(bboxes):
        """
            将带有[x,y,w,h,angle]的bboxes转换为[p1, p2, p3, p4, angle]
            
            input:
                bboxes: np.array([[x,y,w,h,angle], [x,y,w,h,angle], ...])
            
            return:
                rects: np.array([ rect, [p1, p2, p3, p4, angle], [p1, p2, p3, p4, angle], ...])
                        rect: list([p1, p2, p3, p4, angle])
                        p: np.array([x ,y])
                        angle: float
        """
        rects = []
        for bbox in bboxes:
            left_up = bbox[:2] - bbox[2:4] * 0.5
            right_bottom = bbox[:2] + bbox[2:4] * 0.5
            angle = bbox[-1]

            p1 = np.array([left_up[0], left_up[1]])
            p2 = np.array([left_up[0], right_bottom[1]])
            p3 = np.array([right_bottom[0], right_bottom[1]])
            p4 = np.array([right_bottom[0], left_up[1]])

            rects.append([p1, p2, p3, p4, angle])

        return np.array(rects)

    def rotate_rect(rects):
        """
            input:
                rects: np.array([[p1, p2, p3, p4, angle], ...])
            
            output:
                no angle rects: rects: list([[p1, p2, p3, p4], ...])，
                    点的顺序：在笛卡尔坐标系下顺时针
        """
        # 输入判断

        # 初始化
        rotate_rects = []

        # 获取角度

        # rect : [[x,y], [x,y], [x,y], [x,y], angle]
        for rect_with_angle in rects:
            rad_angle = rect_with_angle[-1]
            rect = rect_with_angle[:4]

            rotate_matrix = np.matrix([[np.cos(rad_angle), -np.sin(rad_angle)],
                                       [np.sin(rad_angle), np.cos(rad_angle)]])
            xy = np.matrix((rect[2] + rect[0]) * 0.5).T

            rotate_rect = []
            for p in rect:
                # rp = R * (p - xy) + xy
                r_p = rotate_matrix * np.matrix(np.matrix(p).T - xy) + xy
                rotate_rect.append(np.array(r_p).reshape(-1).tolist())
            rotate_rects.append(rotate_rect)

        return rotate_rects

    # 主程序
    iou = []

    # 计算面积
    rect_boxes1_area = list(bboxes1[..., 2] * bboxes1[..., 3])
    rect_boxes2_area = list(bboxes2[..., 2] * bboxes2[..., 3])

    # 计算矩形框
    rect_bboxes1 = reflect_xywht2rect(bboxes1)
    rect_bboxes2 = reflect_xywht2rect(bboxes2)
    print("rect_bboxes1:", rect_bboxes1)
    print("rect_bboxes2:", rect_bboxes2)

    # 旋转标注框
    rotate_bboxes1 = rotate_rect(rect_bboxes1)
    rotate_bboxes2 = rotate_rect(rect_bboxes2)

    for b1_index, box1 in enumerate(rotate_bboxes1):
        for b2_index, box2 in enumerate(rotate_bboxes2):
            # 计算重叠区域
            polygon = SutherlandHodgman(box1, box2)
            print("polygon:", polygon)

            # 计算重叠区域面积
            if(len(polygon) != 0):
                S = polygon_area(polygon)
            else:
                S = 0

            union_area = rect_boxes1_area[b1_index] + \
                rect_boxes2_area[b2_index] - S
            # 计算iou
            iou.append(S/union_area)

    return np.array(iou)


if __name__ == "__main__":
    b = np.array([[16.   ,  5.125, 17.5  ,  5.625]])
    c = reflect_xywh2rect_v1(b)
    d = rotate_rect(c, 0.5)
    print(d)