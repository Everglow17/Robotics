#!/usr/bin/env python
import rospy

# the message that we get from the arduino
from std_msgs.msg import Int32

# the output message controlling the speed and direction of the robot
from geometry_msgs.msg import Twist

from math import sqrt

def ir_callback(data):
    global left, right, front
    global left_distace, right_distance, front_distance
    global timer
    global pre, now

    # Twist is a message type in ros, here we use an Twist message to control kobuki's speed
    # twist. linear.x is the forward velocity, if it is zero, robot will be static,
    # if it is grater than 0, robot will move forward, otherwise, robot will move backward
    # twist.angular.axis is the rotatin velocity around the axis
    #
    # Around which axis do we have to turn? In wich direction will it turn with a positive value?
    # Right hand coordinate system: x forward, y left, z up

    twist = Twist()
    twist.linear.x = 0.1
    twist.angular.z = 0.



    # write your code here
    data = data.data
    rpr220 = data >> 16
    sharp = data & 0x0000ffff

    #read and store
    if rpr220 <= 55:
        left, right, front = [], [], []
        left_distace, right_distance, front_distance = 0, 0, 0
        timer = -1

    else:
        timer += 1

        if 0 <= timer and timer < 114:
            left.append(sharp)

        elif 114 <= timer and timer <= 145:
            left.append(sharp)
            front.append(sharp)
            right.append(sharp)

        elif 145 < timer and timer <= 259:
            right.append(sharp)

        elif timer == 260:
            i = 1
            while i<=len(front)-1:
                if front[i]-front[i-1]>=50 and front[i]-fonrt[i+1]>=50:
                    del(front[i])
                else:
                    i += 1
            front_distance = max(front[:])
            # front_distance = sum(front[:])/len(front)
            left_distace = sum(left[:])/len(left)
            right_distance = sum(right[:])/len(right)

            now = right_distance- left_distace

    print("front_distance", front_distance)
    print("left_distace", left_distace)
    print("right_distance", right_distance)
    print("pre", pre)
    print("now", now)
    print(" ")
    if timer == 500:
        pre = now

    if front_distance >= 210:
        twist.linear.x =  0.0

    twist.angular.z = 0.012 * (1 + 0.002*abs(pre - now)) * (right_distance - left_distace)

    # actually publish the twist message
    kobuki_velocity_pub.publish(twist)


def range_controller():

    # define the publisher globally
    global kobuki_velocity_pub

    # initialize the node
    rospy.init_node('range_controller', anonymous=True)

    # initialize the publisher - to publish Twist message on the topic below...
    kobuki_velocity_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)

    # subscribe to the topic '/ir_data' of message type Int32. The function 'ir_callback' will be called
    # every time a new message is received - the parameter passed to the function is the message
    rospy.Subscriber("/ir_data", Int32, ir_callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

# start the line follow
if __name__ == '__main__':
    left, right, front = [], [], []
    left_distace, right_distance, front_distance = 0, 0, 0
    timer = 0
    pre, now = 0, 0
    range_controller()
