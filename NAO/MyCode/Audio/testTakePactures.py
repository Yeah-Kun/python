#-*- coding: utf-8 -*-
'''
	Created by Ian in 2017-8-7 14:45:16
	读取NAO机器人的摄像头数据
'''

import time
from naoqi import ALProxy
robot_ip = "192.168.1.103" #NAO的IP地址。注：确保主机和NAO处于同一局域网
robot_port = 9559   # default port : 9559

# Create a proxy to ALPhotoCapture
try:
	pcp = ALProxy("ALPhotoCapture", robot_ip, robot_port)
except Exception, e:
	print "Error when creating ALPhotoCapture proxy:"
	print str(e)
	exit(1)

pcp.setResolution(2)
pcp.setPictureFormat("jpg")
print ("start to take picture")
print(pcp.takePictures(1, "E:/AllData/workspace/NAO/Cameras/", "images"))
'''
pcp.setCameraID(0)
pcp.setFrameRate(30)
pcp.startRecording("E:\\AllData\\workspace\\NAO\\Cameras\\","video",overwrite=True)
time.sleep(5)
#pcp.stopRecording()
'''
