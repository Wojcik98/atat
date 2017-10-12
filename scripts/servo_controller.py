#!/usr/bin/env python2
import serial
import rospy
from atat.msg import ServosAngles


def get_cmd_end():
    return [ord('\r'), ord('\n')]


def get_cmd_time(time):
    cmd = 'T' + str(time)
    return [ord(c) for c in cmd]


def get_cmd_impulse(impulse, channel):
    cmd = '#' + str(channel) + 'P' + str(impulse)
    return [ord(c) for c in cmd]


def get_cmd_angle(angle, channel):
    impulse = int(float(angle)*2200./180. + 500)
    return get_cmd_impulse(impulse, channel)


def set_servos(angles, time):
    cmd = []
    for channel, angle in angles:
        cmd += get_cmd_angle(angle, channel)
    cmd += get_cmd_time(time)
    cmd += get_cmd_end()
    rospy.logdebug(''.join([chr(a) for a in cmd]))
    return port.write(cmd)


def given2real(given_angles):
    real_angles = []
    for servo in given_angles.servos:
        ch = servo.channel
        angle = servo.angle
        angle_zero = rospy.get_param('servo_' + str(ch) + '_angle_zero')
        servo_direction = int(rospy.get_param('servo_' + str(ch) + '_direction'))   # 1 or -1

        real_angle = angle_zero + angle
        if servo_direction == -1:
            real_angle = 180. - real_angle

        real_angles.append((ch, real_angle))
    return real_angles


def callback(given_angles):
    time = 200     # TODO read from parameter server
    real_angles = given2real(given_angles)
    rospy.loginfo(real_angles)
    set_servos(real_angles, time)


def listener():
    global port
    port = serial.Serial('/dev/ttyS0')
    port.baudrate = 9600
    rospy.init_node('servo_controller')

    rospy.Subscriber('servos_angles', ServosAngles, callback)

    rospy.spin()


if __name__ == '__main__':
    listener()
