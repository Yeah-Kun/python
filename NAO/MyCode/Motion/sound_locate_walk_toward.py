# -*- encoding: UTF-8 -*-
"""Locate the sound and walk toward you
    update by Ian in 2017-9-1 11:40:27

"""


import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
from optparse import OptionParser

from detail import Sound_location_walk_module

NAO_IP = "192.168.1.102"

motion = ALProxy("ALMotion", NAO_IP, 9559)
motion.moveInit()
motion.setStiffnesses('Body',1.0) # 设置刚度
parser = OptionParser() 

'''解释OptionParser对象的方法
    定义命令行参数:add_option(参数，help：解释参数，dest：将参数保存到变量名中，dest就是用于设置变量名)
    设置默认值：set_defaults()
    解析程序的命令行：parse_args()
'''
parser.add_option("--pip",
        help="Parent broker port. The IP address or your robot",
        dest="pip")
parser.add_option("--pport",
        help="Parent broker port. The port NAOqi is listening to",
        dest="pport",
        type="int")
parser.set_defaults(
        pip=NAO_IP,
        pport=9559)

(opts, args_) = parser.parse_args()
pip   = opts.pip
pport = opts.pport
    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port
       
       
    # Warning: Soundlocation must be a global variable
    # The name given to the constructor must be the name of the
    # variable
global Soundlocation
Soundlocation = Sound_location_walk_module("Soundlocation")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print
    print "Interrupted by user, shutting down"
    myBroker.shutdown()
    sys.exit(0)