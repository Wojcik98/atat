#!/usr/bin/env python2
import serial
import rospy
from atat.msg import ServoPositions


def get_cmd_end():
    return [ord('\r'), ord('\n')]


def get_cmd_time(time):
    cmd = 'T' + str(time)
    return [ord(c) for c in cmd]


def get_cmd_impulse(channel, impulse):
    cmd = '#' + str(channel) + 'P' + str(impulse)
    return [ord(c) for c in cmd]


def get_cmd_angle(channel, angle):
    impulse = int(float(angle)*2200./180. + 500)
    return get_cmd_impulse(channel, impulse)


def set_servos(port, channels, angles, time):
    cmd = []
    for i in range(len(channels)):
        cmd += get_cmd_angle(channels[i], angles[i])
    cmd += get_cmd_time(time)
    cmd += get_cmd_end()
    return port.write(cmd)


def set_legs(port, channels, angles, times):
    for i in range(4):
        set_servos(port, channels[i], angles[i], times[i])


def callback(servo_positions):
    angles = [servo_positions.front_left, servo_positions.front_right,
              servo_positions.back_left, servo_positions.back_right]
    rospy.loginfo('Setting servos: ' + str(angles))
    # TODO set this in parameter server
    channels = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    times = [200] * 4
    set_legs(port, channels, angles, times)


def listener():
    global port
    port = serial.Serial('/dev/ttyS0')
    port.baudrate = 9600
    rospy.init_node('servo_controller')

    rospy.Subscriber('servo_positions', ServoPositions, callback)

    rospy.spin()


if __name__ == '__main__':
    listener()

