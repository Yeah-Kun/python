# -*- encoding: UTF-8 -*-
""" 获取声音，使头部面对声源
    create by Ian in 2017-9-4 16:48:30
    解决方法：
        1. 读取声源信息
        2. 转动头部
"""
from naoqi import ALModule
from naoqi import ALProxy
from naoqi import ALBroker
import sys
import time
import argparse


class SoundAndMoveHead(ALModule):
    """听声音转动头部"""

    def __init__(self, name):
        ALModule.__init__(self, name)  # 需要先调用父类的初始化方法
        self.life = ALProxy('ALAutonomousLife')
        self.motion = ALProxy('ALMotion')
        self.posture = ALProxy('ALRobotPosture')
        self.memory = ALProxy('ALMemory')
        self.name = name

        # 初始化
        self.life.setState('disabled')  # 设置禁用状态，关闭一切反射
        self.motion.wakeUp()  # 唤醒机器人
        self.posture.goToPosture("StandInit", 0.5)  # 姿态初始化
        self.motion.setStiffnesses("Head", 1.0)

    def sound(self):
        self.sound = ALProxy('ALSoundLocalization')
        self.sound.setParameter('Sensitivity', 0.1)  # 设置灵敏度0~1
        self.memory.subscribeToEvent(
            'ALSoundLocalization/SoundLocated', self.name, 'move_head')  # 订阅事件，并且回调函数执行回调函数里面的内容

    def move_head(self):
        """获取新事件的数据值，并转头"""
        self.memory.unsubscribeToEvent(
            'ALSoundLocalization/SoundLocated', self.name)  # 取消事件订阅，以免电机转动影响声音的监听
        # 获取新事件数据
        data = self.memory.getData('ALSoundLocalization/SoundLocated')

        names = ["HeadYaw", "HeadPitch"]
        angles = data[1][:2]
        print angles
        fractionMaxSpeed = 0.5
        self.motion.setAngles(names, angles, fractionMaxSpeed) # 头转向
        self.memory.subscribeToEvent(
            'ALSoundLocalization/SoundLocated', self.name, 'move_head')  # 重新订阅事件


def main():
    """主函数"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.101",
                        help="192.168.1.101")
    parser.add_argument("--port", type=int, default=9559,
                        help="9987")
    parser.add_argument("--facesize", type=float, default=0.1,
                        help="0.2")

    args = parser.parse_args()

    # 设置代理
    myBroker = ALBroker("myBroker", "0.0.0.0", 0, args.ip, args.port)
    global mymotion
    mymotion = SoundAndMoveHead('mymotion')
    mymotion.sound()
    # 在类外部也能使用订阅事件，使事件被触发时，也能做出反应
    # mymotion.memory.subscribeToEvent('ALSoundLocalization/SoundLocated','mymotion','test')
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)


if __name__ == '__main__':
    main()
