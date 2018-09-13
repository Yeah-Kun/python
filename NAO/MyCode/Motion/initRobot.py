#! /usr/bin/env python
#-*- coding: utf-8 -*-
'''
	made by Ian in 2017-8-5 17:44:53
	使机器人复位
'''

import time
from naoqi import ALProxy
robot_ip = "192.168.1.101" #NAO的IP地址。注：确保主机和NAO处于同一局域网
robot_port = 9559   # default port : 9559
motionProxy = ALProxy("ALMotion", robot_ip, robot_port)
postureProxy = ALProxy("ALRobotPosture", robot_ip, robot_port)
motionProxy.wakeUp() # 唤醒机器人
motionProxy.moveInit() # 初始化行走动作
motionProxy.rest() # 机器人复位