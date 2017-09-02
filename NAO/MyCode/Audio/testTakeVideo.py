#-*- coding: utf-8 -*-
'''
	Created by Ian in 2017-8-7 14:45:16
	读取NAO机器人的摄像头数据
'''


import os
import sys
import time
from naoqi import ALProxy

IP = "192.168.1.103" #NAO的IP地址。注：确保主机和NAO处于同一局域网
PORT = 9559   # default port : 9559



# Create a proxy to ALVideoRecorder
try:
	videoRecorderProxy = ALProxy("ALVideoRecorder", IP, PORT)
except Exception, e:
	print "Error when creating ALVideoRecorder proxy:"
	print str(e)
	exit(1)

videoRecorderProxy.setFrameRate(10.0)
videoRecorderProxy.setResolution(2) # Set resolution to VGA (640 x 480)
# We'll save a 5 second video record in /home/nao/recordings/cameras/
videoRecorderProxy.startRecording("E:/AllData/workspace/NAO/Cameras/", "test")
print "Video record started."

time.sleep(5)

videoInfo = videoRecorderProxy.stopRecording()
print "Video was saved on the robot: ", videoInfo[1]
print "Total number of frames: ", videoInfo[0]