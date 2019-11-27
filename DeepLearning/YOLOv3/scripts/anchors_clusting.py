import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
import os, cv2
import glob
from lxml import etree
import tensorflow.compat.v1 as tf
from absl import app

flags = tf.app.flags
flags.DEFINE_string("annotation_dir", "", "Directory of annotation file(.xml).")
flags.DEFINE_string("image_dir", "", "Directory of images file(.jpg).")
flags.DEFINE_string("labels_file", "", " labels file.")
flags.DEFINE_integer("k", 9, "numbers of anchors.")
FLAGS = flags.FLAGS




def parse_annotation(ann_dir, img_dir, labels=[]):
    '''
    '''
    all_imgs = []
    seen_labels = {}
    counter = 0
    for ann in ann_dir:
        counter += 1
        if "xml" not in ann:
            continue
        img = {'object':[]}

        root = etree.parse(ann).getroot()
        
        for elem in root:
            obj = {}
            if 'filename' in elem.tag:
                path_to_image = os.path.join(img_dir, elem.text)
                img['filename'] = path_to_image
                ## make sure that the image exists:
                if not os.path.exists(path_to_image):
                    assert False, "file does not exist!\n{}".format(path_to_image)
            
            if "size" in elem.tag:
                for sub_elem in elem:
                    if 'width' in sub_elem.tag:
                        img['width'] = int(sub_elem.text)
                    if 'height' in sub_elem.tag:
                        img['height'] = int(sub_elem.text)


            if 'object' in elem.tag or 'part' in elem.tag:
                for sub_elem in elem:
                    if 'name' in sub_elem.tag:
                        obj['name'] = sub_elem.text

                    if 'bndbox' in sub_elem.tag:
                        for box_elem in sub_elem:
                            if 'xmin' in box_elem.tag:
                                obj['xmin'] = int(round(float(box_elem.text)))
                            if 'ymin' in box_elem.tag:
                                obj['ymin'] = int(round(float(box_elem.text)))
                            if 'xmax' in box_elem.tag:
                                obj['xmax'] = int(round(float(box_elem.text)))
                            if 'ymax' in box_elem.tag:
                                obj['ymax'] = int(round(float(box_elem.text)))
                                
            if(obj != {}):
                img['object'].append(obj)

        if len(img['object']) > 0:
            all_imgs += [img]
                        
    return all_imgs


def iou(box, clusters):
    '''
    :param box:      np.array of shape (2,) containing w and h
    :param clusters: np.array of shape (N cluster, 2) 
    '''
    x = np.minimum(clusters[:, 0], box[0]) 
    y = np.minimum(clusters[:, 1], box[1])

    intersection = x * y
    box_area = box[0] * box[1]
    cluster_area = clusters[:, 0] * clusters[:, 1]

    iou_ = intersection / (box_area + cluster_area - intersection)

    return iou_


def kmeans(boxes, k, dist=np.median,seed=1):
    """
    Calculates k-means clustering with the Intersection over Union (IoU) metric.
    :param boxes: numpy array of shape (r, 2), where r is the number of rows
    :param k: number of clusters
    :param dist: distance function
    :return: numpy array of shape (k, 2)
    """
    rows = boxes.shape[0]

    distances     = np.empty((rows, k)) ## N row x N cluster
    last_clusters = np.zeros((rows,))

    np.random.seed(seed)

    # initialize the cluster centers to be k items
    clusters = boxes[np.random.choice(rows, k, replace=False)]

    while True:
        # Step 1: allocate each item to the closest cluster centers
        for icluster in range(k): # I made change to lars76's code here to make the code faster
            distances[:,icluster] = 1 - iou(clusters[icluster], boxes)

        nearest_clusters = np.argmin(distances, axis=1)

        if (last_clusters == nearest_clusters).all():
            break
            
        # Step 2: calculate the cluster centers as mean (or median) of all the cases in the clusters.
        for cluster in range(k):
            clusters[cluster] = dist(boxes[nearest_clusters == cluster], axis=0)

        last_clusters = nearest_clusters

    return clusters,nearest_clusters,distances



def bbox2boxwh(bbox_information):
    """
        从 bounding box 中获得 bounding box的（width，height）
    """
    wh = []
    for anno in bbox_information:
        fw = float(anno["width"])
        fh = float(anno["height"])

        for obj in anno["object"]:
            w = (obj["xmax"] - obj["xmin"])/fw
            h = (obj["ymax"] - obj["ymin"])/fh
            wh.append([w,h])
        
    return np.array(wh)



def bbox_wh2anchors(bbox_wh, k):
    """
        bbox_wh：数据集中所有bounding box的宽和高
        k：kmeans分类的数量
    """
    clusters, nearest_clusters, distances = kmeans(bbox_wh, k, seed = 2,dist = np.mean)
    return clusters


def anchors_to_114_params(anchors, strides, width, height):
    """
        输出1.14版本的所需的anchors

        anchors : 
        strides : [num, num, num, ...]
        width   : 原始图像的宽度 
        height  : 原始图像的高度
    """
    # 获得每个stride的anchor数目
    num_anchors = len(anchors)
    num_strides = len(strides)
    if num_anchors % num_strides != 0:
        print("Error: strides number was not anchors number mutiple.")
        raise ValueError
    else:
        num_skip = num_anchors // num_strides

    # 复原并计算
    strides_counter = -1
    for i in range(0, num_anchors):
        if( i % num_skip == 0):
            strides_counter += 1
        
        anchors[i][0] = anchors[i][0] * width / strides[strides_counter]
        anchors[i][1] = anchors[i][1] * height / strides[strides_counter]

    # 输出
    new_anchors = []
    for anchor in anchors[::-1]:
        new_anchors.append(anchor[0])
        new_anchors.append(anchor[1])
    return new_anchors



def test():
    # anno dir
    train_annot_dir = "data/images/datas"
        
    # image dir
    train_image_dir = "data/images"

    # label
    labels = ['edge']

    ## Parse annotations 
    if not os.path.exists(train_annot_dir) or not os.path.exists(train_image_dir):
        raise ValueError("directory not found:" + train_annot_dir)
    if not os.path.exists(train_image_dir):
        raise ValueError("directory not found:" + train_image_dir)

    train_annot_folder = glob.glob( os.path.join(train_annot_dir, "*.xml") )
    print("numbers of annotation file: ", len(train_annot_folder))
    train_image = parse_annotation(train_annot_folder,train_image_dir, labels=labels)
    print("N train = {}".format(len(train_image)))


    # 解析标注数据，获得true bbox
    bbox_wh = bbox2boxwh(train_image)

    # 聚类 && 输出聚类结果
    # results = {}
    # for k in range(2, 10):
    #     clusters, nearest_clusters, distances = kmeans(bbox_wh, k, seed = 2,dist = np.mean)
    #     WithinClusterMeanDist = np.mean(distances[np.arange(distances.shape[0]),nearest_clusters])
    #     result = {"clusters":             clusters,
    #             "nearest_clusters":     nearest_clusters,
    #             "distances":            distances,
    #             "WithinClusterMeanDist": WithinClusterMeanDist}
    #     print("{:2.0f} clusters: mean IoU = {:5.4f}".format(k,1-result["WithinClusterMeanDist"]), clusters)
    #     results[k] = result
    clusters, nearest_clusters, distances = kmeans(bbox_wh, 9, seed = 2,dist = np.mean)
    clusters = get_anchor_box(clusters)
    clusters = anchors_to_114_params(clusters, [8, 16, 32], 2048, 2448)
    print(clusters)


def get_class(class_path):
    class_labels = []
    with open(class_path, "r") as f:
        all_class_name = f.readlines()
    for i, class_name in enumerate(all_class_name):
        class_name = class_name.replace("\n","")
        if(class_name != ""):
            class_labels.append(class_name)
    
    return class_labels


def get_anchor_box(clusters):
    """

    """
    return sorted(clusters, key = lambda x : x[0] * x[1])


def main( _ ):
    annotation_dir = FLAGS.annotation_dir
    image_dir = FLAGS.image_dir
    labels_file = FLAGS.labels_file
    k = FLAGS.k


    # 输入判断
    if not os.path.exists(annotation_dir) \
        or not os.path.exists(image_dir) \
        or not os.path.exists(labels_file):
        print("annotation dir: %s\nimage dir: %s\nlabels file: %s" 
            % (annotation_dir, image_dir, labels_file))
        raise ValueError("directory or file not found.")
    else:
        if annotation_dir[-1] != "/" or annotation_dir[-1] != "\\":
            annotation_dir += '/'
        if image_dir[-1] != '/' or image_dir[-1] != "\\":
            image_dir += '/'
    
    ## Parse annotations 
    annotation_file = glob.glob(annotation_dir + "*.xml")

    # get bbox
    bbox = parse_annotation(annotation_file, image_dir, labels = get_class(labels_file))

    # parse bbox，get true bbox
    bbox_wh = bbox2boxwh(bbox)

    #聚类
    clusters, nearest_clusters, distances = kmeans(bbox_wh, k, seed = 2,dist = np.mean)

    clusters = get_anchor_box(clusters)
    print(clusters)

if __name__ == "__main__":
    # tf.app.run()
    test()
