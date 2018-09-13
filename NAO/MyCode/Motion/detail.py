# -*- encoding: UTF-8 -*-
"""
	update by Ian in 2017-8-31 21:55:54

"""
from naoqi import ALModule
from naoqi import ALProxy
import sys
import time
memory=None
memory1=None
class Sound_location_walk_module(ALModule):
    """ A simple module able to make the Nao
    locate the sound and walk toward person
    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create a proxy to ALTextToSpeech for later use 
        #设置所有参数在先，激活在后
        self.motion=ALProxy('ALMotion')
        self.awareness=ALProxy('ALBasicAwareness')  # 让nao机器人建立和保持与人的眼神交流
        self.awareness.setParameter('LookStimulusSpeed',0.5) # 设置看到刺激时头部的速度
        
        STATUS=self.awareness.getParameter('LookStimulusSpeed') # 获得头部速度的基本参数
        if STATUS != 0.5:
            print 'Failed to set the lookstimulusspeed'
            #sys.exit(0)
        try:
            self.awareness.setStimulusDetectionEnabled('Sound',True) # 激活/禁用指定类型的刺激
            STATUS=self.awareness.isStimulusDetectionEnabled('Sound')
        except ALError as errmsg:
            print errmsg
            sys.exit(0)
        if STATUS==False:
            print 'stimulus can not set Sound'
            sys.exit(0)
        self.awareness.setTrackingMode("BodyRotation") # 设置头和脚转动
        STATUS=self.awareness.getTrackingMode() # 获得当前的跟踪模式
        if STATUS !='BodyRotation':
            print 'The TrackingMode can not set as BodyRotation'
            sys.exit(0)
        self.awareness.setEngagementMode('FullyEngaged') # 参与模式，一直跟踪某个人
        STATUS=self.awareness.getEngagementMode()
        if STATUS !='FullyEngaged':
            print 'The EngagementMode can not set as FullyEngaged'
            sys.exit(0)
        self.awareness.startAwareness() # 开始定义好的模式和动作
        STATUS=self.awareness.isAwarenessRunning()
        if STATUS == False:
            print 'basic awareness can not start'
            sys.exit(0)
        global memory
        memory=ALProxy('ALMemory')
        memory.subscribeToEvent("ALBasicAwareness/StimulusDetected", # 这是干嘛的？
            'Sound',
            "onStimulusDetected")


        #motion 部分
        '''
        FRAME_TORSO = 0
        FRAME_WORLD = 1
        FRAME_ROBOT = 2
        Pos_obs=self.motion.getChainClosestObstaclePosition('LArm',FRAME_ROBOT) # 获得当前正交安全距离
        self.motion.setOrthogonalSecurityDistance(0.4)  # 设置正交安全距离
        self.motion.setExternalCollisionProtectionEnabled('All',True) # 启动外部碰撞保护
        global memory1
        memory1=ALProxy('ALMemory')
        memory1.subscribeToEvent("ALMotion/Safety/ChainVelocityClipped",
            ['ChainName',Pos_obs],
            "onSafety")
        '''
    def onStimulusDetected(self, *_args):
        print 'yes'
        #self.motion.setAngles('Torso')
        #self.motion.move()
        #self.motion.waitUntilMoveIsFinished()
    def onSafety(self,*_args):
        pass