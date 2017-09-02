# -*- encoding: UTF-8 -*-

"""
This example shows how to use ALTracker with face.
"""

import time
import argparse
from naoqi import ALProxy

def main(IP, PORT, faceSize):

    print "Connecting to", IP, "with port", PORT
    motion = ALProxy("ALMotion", IP, PORT)
    tracker = ALProxy("ALTracker", IP, PORT)

    # First, wake up.
    motion.wakeUp()

    # Add target to track.
    targetName = "Face"
    faceWidth = faceSize
    tracker.registerTarget(targetName, faceWidth)

    # Then, start tracker.
    tracker.track(targetName)

    print "ALTracker successfully started, now show your face to robot!"
    print "Use Ctrl+c to stop this script."

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print "Interrupted by user"
        print "Stopping..."

    # Stop tracker.
    tracker.stopTracker()
    tracker.unregisterAllTargets()
    motion.rest()

    print "ALTracker stopped."


if __name__ == "__main__" :

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.100",
                        help="192.168.1.100")
    parser.add_argument("--port", type=int, default=9559,
                        help="9987")
    parser.add_argument("--facesize", type=float, default=0.1,
                        help="0.2")

    args = parser.parse_args()

    main(args.ip, args.port, args.facesize)