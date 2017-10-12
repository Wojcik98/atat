#!/usr/bin/env python2
import rospy
from atat.msgs import ServoAngle, ServosAngles
from sensor_msgs.msg import Joy


def callback(joy):
    msg = ServosAngles()
    tmp = ServoAngle()
    gle = []
    for i in range(4):
        tmp.channel = i
        tmp.angle = 180.0 * joy.axes[i]
        gle.append(tmp)
    msg = [gle] * 4
    pub.publish(msg)


def talker():
    global pub
    pub = rospy.Publisher('servo_angles', ServosAngles, queue_size=10)
    rospy.Subscriber('joy', Joy, callback)
    rospy.init_node('leg_test', anonymous=True)
    rospy.spin()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
