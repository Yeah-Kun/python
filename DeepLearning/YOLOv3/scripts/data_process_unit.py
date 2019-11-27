import os
import shutil
import glob
import cv2 as cv
from lxml import objectify
from lxml import etree


def copy_file_to_dst_dir(target_file, src_dir, dst_dir, format):
    """
        target_file: 需要复制的文件的前缀名
        src_dir: 源目录
        dst_dir: 目的目录
    """
    # 输入判断
    if not os.path.exists(src_dir) or not os.path.exists(dst_dir):
        raise ValueError("input file was not exists, src path:",
                         src_dir, " dst path:", dst_dir)
    if '.' not in format:
        format = '.' + format

    for name in target_file:
        src_file = os.path.join(src_dir, name + format)
        # 判断文件是否存在
        if(not os.path.exists(src_file)):
            raise ValueError("file not found, path: ", src_file)

        # 传输文件
        dst_file = os.path.join(dst_dir, name + format)
        shutil.copyfile(src_file, dst_file)


def get_target_prefix(src_dir, format):
    """
        获得目录下对应所有文件的前缀列表
    """
    # 输入判断
    if not os.path.exists(src_dir):
        raise ValueError("input file was not exists, path:", src_dir)
    if('.' not in format):
        format = '.' + format

    file_path = glob.glob(os.path.join(src_dir, '*' + format))
    prefix = []
    for f in file_path:
        f = os.path.basename(f)
        prefix.append(os.path.splitext(f)[0])

    print("number of prefix:", len(prefix))
    return prefix


def read_xml(xml_file):
    """
        xml_file: xml文件路径

        return: 
    """
    if not os.path.exists(xml_file):
        raise ValueError("file not found, path:", xml_file)

    xml_info = {'object': []}
    root = etree.parse(xml_file).getroot()
    for elem in root:
        obj = {}
        if 'filename' in elem.tag:
            path_to_image = elem.text
            xml_info['filename'] = path_to_image

        if "size" in elem.tag:
            for sub_elem in elem:
                if 'width' in sub_elem.tag:
                    xml_info['width'] = int(sub_elem.text)
                if 'height' in sub_elem.tag:
                    xml_info['height'] = int(sub_elem.text)

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
            xml_info['object'].append(obj)

    return xml_info


def draw_bbox_two_corner_point(image_path, bboxes, color=(0, 0, 255)):
    """
        图像绘制bbox
    """
    image = cv.imread(str(image_path))
    if isinstance(image, type(None)):
        raise ValueError("image could not be load, path:", image_path)

    for bbox in bboxes:
        left_top = (bbox['xmin'], bbox['ymin'])
        right_bottom = (bbox['xmax'], bbox['ymax'])
        image = cv.rectangle(image, left_top, right_bottom, color, 1)

    return image


def draw_bbox_four_corner_point(image_path, bboxes, color=(0, 0, 255)):
    """

    """
    image = cv.imread(image_path)
    if not isinstance(image, None):
        raise ValueError("image could not be load, path:", image_path)

    for bbox in bboxes:
        left_top = bbox[0]
        right_bottom = bbox[2]
        image = cv.rectangle(image, left_top, right_bottom, color, 1)

    return image


def draw_bbox_xywh(image_path, bboxes, color=(0, 0, 255)):
    pass


def dataset_show(images_dir, xml_dir, save_dir):
    """
        将数据集可视化：
            image_dir的图像经过可视化保存在save_dir

        image_dir: 图像目录
        xml_dir: xml文件目录
        save_dir: 保存目录
    """
    # 输入判读
    if not os.path.exists(images_dir):
        raise ValueError("images dir is not exits, path:", images_dir)
    if not os.path.exists(xml_dir):
        raise ValueError("xml dir is not exits, path:", xml_dir)
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    images_file_path = glob.glob(os.path.join(images_dir, "*.??g"))
    print("number of images:", len(images_file_path))

    for image_path in images_file_path:
        image = cv.imread(image_path)

        if image is not None:
            name = os.path.splitext(os.path.basename(image_path))[0]

            xml_file_path = os.path.join(xml_dir, name + ".xml")
            if os.path.exists(xml_file_path):
                # 从xml中获取框数据
                xml_info = read_xml(xml_file_path)
                # 绘制
                image = draw_bbox_two_corner_point(
                    image_path, xml_info['object'])
                # 保存文件
                save_path = os.path.join(save_dir, name + ".jpg")
                cv.imwrite(save_path, image)
            else:
                print("xml file was empty, path:", xml_file_path)
        else:
            print("image was empty, path:", image_path)

    print("Successfully done.")


def build_xml(image_name, bboxes, width, height, folder="image"):
    """
        根据输入信息建立xml文件
    """
    name = os.path.basename(image_name)

    E = objectify.ElementMaker(annotate=False)

    anno_tree = E.annotation(
        E.folder(folder),
        E.filename(name),
        E.path(image_name),
        E.source(
            E.database("Unknown")
        ),
        E.size(
            E.width(width),
            E.height(height),
            E.depth(3)
        ),
        E.segmented(0),
    )
    for bbox in bboxes:
        anno_tree.append(
            E.object(
                E.name(0),
                E.pose("Unspecified"),
                E.truncated(0),
                E.difficult(0),
                E.bndbox(
                    E.xmin(bbox[0]),
                    E.ymin(bbox[1]),
                    E.xmax(bbox[2]),
                    E.ymax(bbox[3])
                )
            )
        )

    return anno_tree


def build_xml_multi_classes(image_name, bboxes, width, height, folder="image"):
    """
        根据输入信息建立xml文件
    """
    name = os.path.basename(image_name)

    E = objectify.ElementMaker(annotate=False)

    anno_tree = E.annotation(
        E.folder(folder),
        E.filename(name),
        E.path(image_name),
        E.source(
            E.database("Unknown")
        ),
        E.size(
            E.width(width),
            E.height(height),
            E.depth(3)
        ),
        E.segmented(0),
    )
    for bbox in bboxes:
        anno_tree.append(
            E.object(
                E.name(bbox[0]),
                E.pose("Unspecified"),
                E.truncated(0),
                E.difficult(0),
                E.bndbox(
                    E.xmin(bbox[1]),
                    E.ymin(bbox[2]),
                    E.xmax(bbox[3]),
                    E.ymax(bbox[4])
                )
            )
        )

    return anno_tree


def dataset_show_interface():
    # image_dir: 图像目录
    image_dir = "data/new_images"

    # xml_dir: xml文件目录
    xml_dir = "data/new_images/datas"

    # save_dir: 保存目录
    save_dir = "C:/Users/BZL/Desktop/c2/check"

    dataset_show(image_dir, xml_dir, save_dir)


def dataset_divide():
    """
        划分数据集
    """
    # 需要拷贝的图像前缀目录
    prefix_dir = "data/images"
    prefix = get_target_prefix(prefix_dir, "png")

    # 源xml 目录
    src_xml_path = "data/new_images/datas"
    # 目标xml目录
    dst_xml_path = "data/images/datas"
    copy_file_to_dst_dir(prefix, src_xml_path, dst_xml_path, ".xml")

    # # 源图像目录
    # src_image_path = "D:/Company/DeepLearningFloorTile/class_1/biaoqian/edges_label/VOCdevkit/VOC2018/JPEGImages"
    # # 目标图像目录
    # dst_image_path = "D:/myself/LearningYOLOv3/tensorflow1.x/tensorflow-yolov3-master/tensorflow-yolov3-master/data/images"
    # copy_file_to_dst_dir(prefix, src_image_path, dst_image_path, ".jpg")

    print("Successfully done.")


def label_txt2xml_edge(image_dir, txt_dir, save_dir):
    """
        自定义txt文件转换为pascal xml文件
    """
    def prase_txt(read_path):
        if not os.path.exists(read_path):
            raise ValueError("can not find the directory, path:", read_path)

        basename = os.path.basename(read_path)
        with open(read_path, "r") as f:
            file_info = f.readlines()

        return basename, [line.replace("\n", "") for line in file_info]

    def txt_clean(txt_info):
        """
            数据清洗
        """
        clean_text = []
        for line in txt_info:
            # 每行剔除剔除非关键信息
            line = line.replace("\n", "")

            # 提取关键信息
            line = line.split(" ")

            # 整形化
            line = [int(float(line[0])), int(float(line[1])), int(float(line[2])), int(float(line[3]))]
            clean_text.append(line)

        return clean_text

    
    def from_dir_find_image(name, image_files_path):
        path = ""
        for image_path in image_files_path:
            if name in image_path:
                path = image_path
                break
        return path

    # 输入判断
    if not os.path.exists(txt_dir):
        raise ValueError("can not find txt directory, path:", txt_dir)
    if not os.path.exists(image_dir):
        raise ValueError("can not find image directory, path:", image_dir)
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    # 读文件列表
    txt_files_path = glob.glob(os.path.join(txt_dir, "*.txt"))
    image_files_path = glob.glob(os.path.join(image_dir, "*.??g"))
    print("number of txt files:", len(txt_files_path))

    # txt转换为xml
    for path in txt_files_path:
        # 解析txt文件
        txt_name, txt_info = prase_txt(path)
        name = os.path.splitext(txt_name)[0].replace(".", "")

        # 搜寻txt对应image
        image_name = from_dir_find_image(name, image_files_path)
        if(image_name == ""):
            raise ValueError("can not find image from txt name, txt name:", txt_name)

        # 数据清洗
        txt_info = txt_clean(txt_info)


        # 新建xml
        anno_tree = build_xml(image_name, txt_info, 2448, 2048, "image")

        # 写入文件
        save_path = os.path.join(save_dir, name + ".xml")
        with open(save_path, "w") as f:
            f.write(etree.tostring(anno_tree, pretty_print=True).decode("utf-8"))

    print("Successfully done.")


def test_label_txt2xml_edge():
    image_dir = "D:/Company/DeepLearningFloorTile/class_1/biaoqian/point_label/VOC2018/JPEGImages"
    txt_dir = "C:/Users/BZL/Desktop/标注/labels"
    save_dir = "C:/Users/BZL/Desktop/标注/xml"
    label_txt2xml_edge(image_dir, txt_dir, save_dir)


def temp_copy_src_to_dst():
    # 需要拷贝的图像前缀目录
    prefix_dir = "C:/Users/BZL/Desktop/clip/new/bad_edge"
    prefix = get_target_prefix(prefix_dir, "png")
    prefix = [p.replace("_dump", "") for p in prefix]


    # 源图像目录
    src_image_path = "D:/Company/FloorImageProcessing/floorlog"
    # 目标图像目录
    dst_image_path = "C:/Users/BZL/Desktop/clip/new/clip"
    copy_file_to_dst_dir(prefix, src_image_path, dst_image_path, ".png")

    print("Successfully done.")



def delete_already_label_info(self_label_xml_dir, delete_dir, delete_prefix = ".txt"):
    """
        删除已经标注的图像
    """
    def delete_halcon_file(prefix, delete_dir):
        delete_txt_path = os.path.join(delete_dir, prefix + ".txt")
        delete_png_path = os.path.join(delete_dir, prefix + "_dump" +".png")

        if os.path.exists(delete_txt_path):
            os.remove(delete_txt_path)
        if os.path.exists(delete_png_path):
            os.remove(delete_png_path)


def move_label_self_and_halcon(self_label_xml_dir, halcon_label_txt_dir, output_dir):
    def get_all_file(dir, prefix):
        # 获得所有需要删除的前缀名
        return glob.glob( os.path.join(dir, "*." + prefix) )
    
    xml_file = get_all_file(self_label_xml_dir, "xml")
    print("number of xml file:", len(xml_file))
    for xml in xml_file:
        shutil.move(xml, os.path.join(output_dir, "xml"))

    txt_file = get_all_file(halcon_label_txt_dir, "txt")
    print("number of txt file:", len(txt_file))
    for txt in txt_file:
        shutil.move(txt, os.path.join(output_dir, "txt"))



def label_txt2xml_edge_multi_classes(image_dir, txt_dir, save_dir):
    """
        自定义txt文件转换为pascal xml文件
    """
    def prase_txt(read_path):
        if not os.path.exists(read_path):
            raise ValueError("can not find the directory, path:", read_path)

        basename = os.path.basename(read_path)
        with open(read_path, "r") as f:
            file_info = f.readlines()

        return basename, [line.replace("\n", "") for line in file_info]

    def txt_clean(txt_info):
        """
            数据清洗
        """
        clean_text = []
        for line in txt_info:
            # 每行剔除剔除非关键信息
            line = line.replace("\n", "")

            # 提取关键信息
            line = line.split(" ")

            # 整形化
            if line != ['']:
                line = [line[0], int(float(line[1])), int(float(line[2])), int(float(line[3])), int(float(line[4]))]
                clean_text.append(line)

        return clean_text

    
    def from_dir_find_image(name, image_files_path):
        path = ""
        for image_path in image_files_path:
            if name in image_path:
                path = image_path
                break
        return path

    # 输入判断
    if not os.path.exists(txt_dir):
        raise ValueError("can not find txt directory, path:", txt_dir)
    if not os.path.exists(image_dir):
        raise ValueError("can not find image directory, path:", image_dir)
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    # 读文件列表
    txt_files_path = glob.glob(os.path.join(txt_dir, "*.txt"))
    image_files_path = glob.glob(os.path.join(image_dir, "*.??g"))
    print("number of txt files:", len(txt_files_path))

    # txt转换为xml
    for path in txt_files_path:
        # 解析txt文件
        txt_name, txt_info = prase_txt(path)
        name = os.path.splitext(txt_name)[0].replace(".", "")

        # 搜寻txt对应image
        image_name = from_dir_find_image(name, image_files_path)
        if(image_name == ""):
            raise ValueError("can not find image from txt name, txt name:", txt_name)

        # 数据清洗
        txt_info = txt_clean(txt_info)


        # 新建xml
        anno_tree = build_xml_multi_classes(image_name, txt_info, 2448, 2048, "image")

        # 写入文件
        save_path = os.path.join(save_dir, name + ".xml")
        with open(save_path, "w") as f:
            f.write(etree.tostring(anno_tree, pretty_print=True).decode("utf-8"))



def auto_data_process(origin_images_dir, self_label_xml_dir, halcon_label_txt_dir, output_dir):
    # 删除halcon中已经标注的数据
    delete_already_label_info(self_label_xml_dir, halcon_label_txt_dir)

    # 检查halcon标注的数据

    # 将自标注和halcon标注的数据放到对应目录
    move_label_self_and_halcon(self_label_xml_dir, halcon_label_txt_dir, output_dir)

    # 转换txt的数据到xml目录中
    label_txt2xml_edge_multi_classes(origin_images_dir, os.path.join(output_dir, "txt"), os.path.join(output_dir, "xml"))

    # 寻找xml对应的图像，并保存在output目录
    xml_path = glob.glob( os.path.join(output_dir, "xml", "*.xml"))

    xml_path = [ os.path.splitext( os.path.basename(xml) )[0] for xml in xml_path ]
    
    copy_file_to_dst_dir(xml_path, origin_images_dir, os.path.join(output_dir, "image"), "png")

    # 检查整体数据的对错
    pass




def main():
    # 源图像目录
    origin_images_dir = "D:/Company/FloorImageProcessing/floorlog"

    # 自标注数据目录
    self_label_xml_dir = "C:/Users/BZL/Desktop/c2/p/outputs"

    # halcon标注数据txt目录
    halcon_label_txt_dir = "C:/Users/BZL/Desktop/label/labels"

    # output dir
    output_dir = "C:/Users/BZL/Desktop/edge2019-11-14"
    
    auto_data_process(origin_images_dir, self_label_xml_dir, halcon_label_txt_dir, output_dir)

    print("Successfully done.")


if __name__ == "__main__":
    main()
