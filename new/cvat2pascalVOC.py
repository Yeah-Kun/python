'''
	cvat格式转pascal_VOC格式脚本
	2018-7-30 19:49:59
'''

from lxml import etree, objectify

class CVAT2VOC(object):
	"""docstring for CVAT2VOC"""
	def __init__(self, srcpath, despath,width = 640, height = 480, depth = 3, folder="label.xml"):
		super(CVAT2VOC, self).__init__()
		self._width = width
		self._height = height
		self._depth = depth
		self._srcpath = srcpath
		self._despath = despath
		self._folder = folder # 文件名


	def path2XML(self):
		"""从地址获取原始XML文件
		"""
		try:
			self.org_xml = etree.parse(self._srcpath)
		except Exception as e:
			raise "无法加载文件"


	def get_orginfo(self):
		"""获得待转化文件的关键信息
		"""
		root = self.org_xml.getroot()
		self.images = root.xpath("./image")


	def translation(self):
		"""关键转化
		"""
		annotations = []
		for imageInfo in self.images:
			E = objectify.ElementMaker(annotate=False)
			anno_tree = E.annotation(
				E.folder(self._folder),
				E.filename(imageInfo.attrib["name"]),
				E.path(self._folder + imageInfo.attrib["name"]),
				E.source(
					E.database("Unknown")
					),
				E.size(
					E.width(self._width),
					E.height(self._height),
					E.depth(self._depth)
					),
				E.segmented(0),
				)

			for eachbox in imageInfo.xpath("./box"):
				E2 = objectify.ElementMaker(annotate=False)
				tree2 = E2.object(
					E2.name(eachbox.attrib["label"]),
					E2.pose("Unspecified"),
					E2.truncated(eachbox.attrib["occluded"]),
					E2.difficult(0),
					E2.bndbox(
						E2.xmin(float(eachbox.attrib["xtl"])),
						E2.ymin(float(eachbox.attrib["ytl"])),
						E2.xmax(float(eachbox.attrib["xbr"])),
						E2.ymax(float(eachbox.attrib["ybr"]))
						),
					)
				anno_tree.append(tree2)

			annotations.append(anno_tree)
		return annotations

	def to_file(self, annotation_list):
		"""输出到文件
		"""
		try:
			for anno in annotation_list:
				with open(self._despath, "ab+") as file:
					file.write(etree.tostring(anno, pretty_print=True))
			print("finished!")
		except Exception as e:
			raise e


	def test_trans(self):
		"""非标准版本使用，数据一致性转换，跟超强的数据匹配
		"""
		annotations = []
		for imageInfo in self.images:
			E = objectify.ElementMaker(annotate=False)
			anno_tree = E.annotation(
				E.folder(self._folder),
				E.filename(imageInfo.attrib["name"]),
				E.path(self._folder + imageInfo.attrib["name"]),
				E.source(
					E.database("Unknown")
					),
				E.size(
					E.width(256),
					E.height(256),
					E.depth(self._depth)
					),
				E.segmented(0),
				)

			for eachbox in imageInfo.xpath(".//box"):
				E2 = objectify.ElementMaker(annotate=False)
				tree2 = E2.object(
					E2.name(eachbox.attrib["label"]),
					E2.pose("Unspecified"),
					E2.truncated(eachbox.attrib["occluded"]),
					E2.difficult(0),
					E2.bndbox(
						E2.xmin(int(float(eachbox.attrib["xtl"])//2.5)),
						E2.ymin(int(float(eachbox.attrib["ytl"])//1.875)),
						E2.xmax(int(float(eachbox.attrib["xbr"])//2.5)),
						E2.ymax(int(float(eachbox.attrib["ybr"])//1.875))
						),
					)
				anno_tree.append(tree2)
				print(etree.tostring(anno_tree, pretty_print=True))

			annotations.append(anno_tree)
		return annotations

	def common(self):
		"""转化组件
		"""
		self.path2XML() 
		self.get_orginfo()
		#anno_list = self.translation() # 标准模块
		anno_list = self.test_trans() # 超强数据匹配模块
		self.to_file(anno_list)


if __name__ == '__main__':
	srcpath = r"D:\Users\Yeah_Kun\Desktop\chaoqiang.xml"
	despath = r"D:\Users\Yeah_Kun\Desktop\chaoqiang2.xml"
	folder = r"D:\Users\Yeah_Kun\Desktop\rotation"
	trans = CVAT2VOC(srcpath, despath, folder)
	trans.common()
