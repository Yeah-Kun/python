## YOLOv3代码仓库

![](data/show/5dcb6826b6670e5e91c30e8c.png)



### 安装

```
pip install -r requirement.txt
```


### 快速使用

```
# 1. 修改data/images文件

# 2. 生成data/dataset中生成相应文件
python 02_YOLO数据构建.py

# 3. 修改data/dataset里面的train和text文件，手动分配数据

# 4. 调整训练参数
vim core/config 

# 5. 训练数据
python train.py 
```

### 目录树

```
├─checkpoint // 模型权重保存点
├─core // 核心代码（模型计算图）
│  └─__pycache__
├─data // 数据
│  ├─anchors // 先验框文件目录
│  ├─classes // 类别目录
│  ├─dataset // 标注文件
│  ├─images // 具体的数据文件（图像，标注文件）
│  │  └─datas // 图像数据对应的xml文件
│  └─log2 // 训练记录文件
├─mAP
│  └─extra
├─results
│  └─classes
├─script // 聚类、生成TFRecord、可视化等脚本程序
└─test
```
