# -*- encoding: UTF-8 -*-
"""
	update by Ian in 2017-8-31 21:55:54
	控制机器人识别人脸，并正面对准人脸
"""
from naoqi import ALModule
from naoqi import ALProxy
from naoqi import ALBroker
import sys
import time
import argparse


class SoundAndFocus(object):
    """docstring for SoundAndFocus

    """

    def __init__(self, name):
        self.motion = ALProxy('ALMotion')
        self.awareness = ALProxy('ALBasicAwareness')  # 让nao机器人建立和保持与人的眼神交流
        self.life = ALProxy('ALAutonomousLife')
        self.posture = ALProxy('ALRobotPosture')

        # 初始化
        self.life.setState('disabled')  # 设置禁用状态，关闭一切反射
        self.motion.wakeUp()  # 唤醒机器人
        #self.posture.goToPosture("StandInit", 0.5)  # 姿态初始化

        self.awareness.setParameter('LookStimulusSpeed', 0.5)  # 设置看到刺激时头部的速度
        status = self.awareness.getParameter(
            'LookStimulusSpeed')  # 获得头部速度的基本参数
        if status != 0.5:
            print 'Failed to set the lookstimulusspeed'
        try:
            self.awareness.setStimulusDetectionEnabled(
                'Sound', True)  # 激活/禁用指定类型的刺激
            status = self.awareness.isStimulusDetectionEnabled('Sound')
        except ALError as errmsg:
            print errmsg
            sys.exit(0)
        if status == False:
            print 'stimulus can not set Sound'
            sys.exit(0)
        self.awareness.setTrackingMode("BodyRotation")  # 设置头和脚转动
        status = self.awareness.getTrackingMode()  # 获得当前的跟踪模式
        if status != 'BodyRotation':
            print 'The TrackingMode can not set as BodyRotation'
            sys.exit(0)
        self.awareness.setEngagementMode('FullyEngaged')  # 参与模式，一直跟踪某个人
        status = self.awareness.getEngagementMode()
        if status != 'FullyEngaged':
            print 'The EngagementMode can not set as FullyEngaged'
            sys.exit(0)
        self.awareness.startAwareness()  # 开始定义好的模式和动作
        print "start Awareness"
        status = self.awareness.isAwarenessRunning()
        if status == False:
            print 'basic awareness can not start'
            sys.exit(0)


def main():
    """主函数"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.102",
                        help="192.168.1.101")
    parser.add_argument("--port", type=int, default=9559,
                        help="9987")
    parser.add_argument("--facesize", type=float, default=0.1,
                        help="0.2")

    args = parser.parse_args()
    myBroker = ALBroker("myBroker", "0.0.0.0", 0, args.ip, args.port)

    Soundlocation = SoundAndFocus("Soundlocation")
    memProxy = ALProxy("ALMemory")
    print memProxy.getData("Device/SubDeviceList/HeadYaw/Position/Actuator/Value")
    
    Soundlocation = SoundAndFocus("Soundlocation")
    memProxy = ALProxy("ALMemory")
    print memProxy.getData("Device/SubDeviceList/HeadYaw/Position/Actuator/Value")
    dataList = []
    try:
        while True:
            time.sleep(1)
            
            memProxy = ALProxy("ALMemory")
            data = memProxy.getData("Device/SubDeviceList/HeadYaw/Position/Actuator/Value")
            print data
            dataList.append(data)
            while len(dataList) == 3:
            	if dataList[0] == dataList[2]:
            		Soundlocation.motion.moveTo(0,0,dataList[0])
            	del dataList
            	dataList = []
			
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)


if __name__ == '__main__':
    main()