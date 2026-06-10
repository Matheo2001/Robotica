#!/usr/bin/en python3
import rospy
from turtlesim.msg import Pose

def pose_callback(msg):
    rospy.logginfo(msg)
if __name__ == '__main__':
    rospy.innit_mode('turtle_pose_subscriber')
    sub = rospy.Subscriber('/turtle1/pos', Pose, callback=)pose_callback

    rospy.loggininfo('Node has been started')
