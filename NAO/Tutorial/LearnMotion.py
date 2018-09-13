#! /usr/bin/env python
#-*- coding: utf-8 -*-
'''
	made by Ian in 2017-8-4 17:16:46
	Locomotion control Tutorial: The Robot Position
	http://doc.aldebaran.com/2-1/naoqi/motion/control-walk-tuto2.html
'''

import time
from naoqi import ALProxy
robot_ip = "192.168.1.102" #NAO的IP地址。注：确保主机和NAO处于同一局域网
robot_port = 9559   # default port : 9559
motionProxy = ALProxy("ALMotion", robot_ip, robot_port)
postureProxy = ALProxy("ALRobotPosture", robot_ip, robot_port)

#aup.playFileFromPosition("F:\\CloudMusic\\Alvaro Soler - Volar.mp3")
#at.ALMotionProxy(0.1)
motionProxy.wakeUp() # 唤醒机器人
motionProxy.moveInit() # 初始化行走动作
motionProxy.moveTo(0,0,5) # 行走距离 （前后、左右、转向角度）

# Send robot to Stand Init
postureProxy.goToPosture("StandInit", 0.5)
# Initialize the move
motionProxy.moveInit()
'''
# end init, begin experiment

# First call of move API
# with post prefix to not be bloquing here.
motionProxy.post.moveTo(0.3, 0.0, 0.5)

# wait that the move process start running
time.sleep(0.1)

# get robotPosition and nextRobotPosition
useSensors = False
robotPosition     = almath.Pose2D(motionProxy.getRobotPosition(useSensors))
nextRobotPosition = almath.Pose2D(motionProxy.getNextRobotPosition())
'''
motionProxy.rest() # 机器人复位

