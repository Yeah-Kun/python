"""
	create by Ian in 2018-8-31 22:44:47
	KCF测试程序
"""
import cv2
class TestKCF:
	def __init__(self, video_path):
		self.ROI = None
		self.video_path = video_path
		self.init_once = False

	def select_roi(self):
		# 是否显示网格 
		ok, image = self.cap.read()
		showCrosshair = True

		# 如果为Ture的话 , 则鼠标的其实位置就作为了roi的中心
		# False: 从左上角到右下角选中区域
		fromCenter = False
		# Select ROI
		self.bbox = cv2.selectROI("selectROI", image, showCrosshair, fromCenter)
		self.tracker = cv2.TrackerKCF_create()
		ok = self.tracker.init(image, self.bbox)


	def check_content(self):
		self.cap = cv2.VideoCapture(self.video_path)
		if self.cap.isOpened() == False:
			raise "输入视频有问题"
			

	def run(self):
		self.check_content()
		self.select_roi()
		while True:
			ok, image = self.cap.read()
			ok, newbox = self.tracker.update(image)
			if ok == True:# 读取成功标志位
				if ok:
					p1 = (int(newbox[0]), int(newbox[1]))
					p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
					cv2.rectangle(image, p1, p2, (200,0,0))

			cv.imshow("tracking", image)
			if cv2.waitKey(27):
				break


if __name__ == '__main__':
	video = r"D:\Users\Yeah_Kun\Desktop\clip\11_clip.mp4"
	kcf = TestKCF(video)
	kcf.run()
