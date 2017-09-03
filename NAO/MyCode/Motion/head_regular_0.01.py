# -*- encoding: UTF-8 -*-
""" 头的偏角＜0.01
	update by Ian in 2017-9-2 19:35:21
	头转一定角度，保持头的相对角度不变，身体再同顺/逆时针转一定角度
"""
from naoqi import ALModule
from naoqi import ALProxy
from naoqi import ALBroker
import sys
import almath
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
        # self.motion.moveInit() # 动作初始化
        self.motion.setStiffnesses("Head", 1.0)  # 设置刚度，不设置不能转动

    def headMove(self):
        """设置头部转动一定角度"""
        names = "HeadYaw"
        angleLists = self.angle * almath.TO_RAD  # 角度转换成弧度
        timeLists = 1.0
        isAbsolute = True
        self.motion.angleInterpolation(
            names, angleLists, timeLists, isAbsolute)  # 头部转相应角度
        headangle = self.memory.getData(
            "Device/SubDeviceList/HeadYaw/Position/Actuator/Value")  # 获得头部理论转动偏角
        headangle2 = self.memory.getData(
            "Device/SubDeviceList/HeadYaw/Position/Sensor/Value") # 获得头部实际转动偏角
        print headangle, headangle2
        return headangle

    def bodyMove(self,headangle):
        self.motion.moveTo(0,0,headangle)
        print "done!"

    def headMoveBack(self):
        names = "HeadYaw"
        angleLists = 0
        timeLists = 1.0
        isAbsolute = True
        self.motion.angleInterpolation(
            names, angleLists, timeLists, isAbsolute)  # 头部转相应角度


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

    mymove = Motion("mymove",angle=60.0)
    headangle = mymove.headMove()
    mymove.bodyMove(headangle)
    mymove.headMoveBack()
