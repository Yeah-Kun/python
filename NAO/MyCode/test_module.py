# -*- encoding: UTF-8 -*-
""" 测试ALSoundLocalization用法
	update by Ian in 2017-9-3 14:51:11
	解决方法：
        1. setParameter设置灵敏度参数
        2. subscribe订阅这个事件
        3. getData获得订阅的数据
"""
from naoqi import ALModule
from naoqi import ALProxy
from naoqi import ALBroker
import sys
import time
import argparse


class Motion(ALModule):
    """控制机器人的动作"""

    def __init__(self, name,angle=50.0):
        ALModule.__init__(self, name)  # 需要先调用父类的初始化方法
        self.life = ALProxy('ALAutonomousLife')
        self.motion = ALProxy('ALMotion')
        self.posture = ALProxy('ALRobotPosture')
        self.memory = ALProxy('ALMemory')

        # 初始化
        self.angle = angle
        self.headangle = 0
        self.life.setState('disabled')  # 设置禁用状态，关闭一切反射
        self.motion.wakeUp()  # 唤醒机器人
        self.posture.goToPosture("StandInit", 0.5)  # 姿态初始化
        self.motion.setStiffnesses("Head", 1.0)  # 设置刚度，不设置不能转动

    def SoundLocalization(self):
        self.sound = ALProxy('ALSoundLocalization')
        self.sound.setParameter('Sensitivity',0.5)
        self.sound.subscribe('ALSoundLocalization/SoundLocated') # 订阅这个事件，或者说启动这个模块
        try:
            while True:
                time.sleep(1)
                data = self.memory.getData('ALSoundLocalization/SoundLocated')
                print data
        except KeyboardInterrupt:
            print
            print "Interrupted by user, shutting down"
            sys.exit(0)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.102",
                        help="192.168.1.101")
    parser.add_argument("--port", type=int, default=9559,
                        help="9987")
    parser.add_argument("--facesize", type=float, default=0.1,
                        help="0.2")

    args = parser.parse_args()

    # 设置代理
    myBroker = ALBroker("myBroker", "0.0.0.0", 0, args.ip, args.port)
    mymotion = Motion('mymotion')
    mymotion.SoundLocalization()
    myBroker.shutdown()
