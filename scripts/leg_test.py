#!/usr/bin/env python2
import rospy
from atat.msg import ServoAngle, ServosAngles
from sensor_msgs.msg import Joy


def callback(joy):
    msg = []
    for i in range(4):
        tmp = ServoAngle()
        tmp.channel = i + 1
        tmp.angle = 90.0 + 90.0 * joy.axes[i]
        msg.append(tmp)
    rospy.loginfo(msg)
    pub.publish(msg)


def talker():
    global pub
    pub = rospy.Publisher('servos_angles', ServosAngles, queue_size=10)
    rospy.Subscriber('joy', Joy, callback)
    rospy.init_node('leg_test', anonymous=True)
    rospy.spin()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
