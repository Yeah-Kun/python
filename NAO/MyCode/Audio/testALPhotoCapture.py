#-*- coding: utf-8 -*-
'''
	http://doc.aldebaran.com/2-1/naoqi/vision/alphotocapture-tuto.html#alphotocapture-tuto
	获取图片程序
	实验结果：程序运行成功，图片获取失败
'''
import os
import sys
import time
from naoqi import ALProxy

# Replace this with your robot's IP address
IP = "192.168.1.101"
PORT = 9559

# Create a proxy to ALPhotoCapture
try:
	photoCaptureProxy = ALProxy("ALPhotoCapture", IP, PORT)
except Exception, e:
	print "Error when creating ALPhotoCapture proxy:"
	print str(e)
	exit(1)

photoCaptureProxy.setResolution(2)
photoCaptureProxy.setPictureFormat("jpg")
photoCaptureProxy.takePictures(3, "E:\\AllData\\workspace\\NAO\\code\\", "image")