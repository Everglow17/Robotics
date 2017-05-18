#!/usr/bin/env python
import rospy

# the message that we get from the arduino
from std_msgs.msg import Int32

# the output message controlling the speed and direction of the robot
from geometry_msgs.msg import Twist

from math import sqrt

def ir_callback(data):
    global left, right
    global left_distace, right_distance
    global timer
    global shift
    global front

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
        left, right = [], []

#----------------------------front---------------start
        front = []
#----------------------------front-----------------end

        left_distace, right_distance = 0, 0
        timer = -1
        shift = False

    else:
        timer += 1

        if 64 <= timer and timer <= 83:
            left.append(sharp)

#----------------------------front---------------start
        if 120 <= timer and timer <= 149:
            front.append(sharp)
#----------------------------front----------------end

        elif 175 <= timer and timer <= 194:
            right.append(sharp)

        elif timer == 195:

#----------------------------remove noise----------------start
            front_count = 1
            while front_count <= (len(front)-2):
                if abs(front[front_count] - front[front_count-1]) >= 100 and abs(front[front_count] - front[front_count+1]) >= 100:
                    del(front[front_count])
                else:
                    front_count += 1

            left_count = 1
            while left_count <= (len(left)-2):
                if abs(left[left_count] - left[left_count-1]) >= 100 and abs(left[left_count] - left[left_count+1]) >= 100:
                    del(left[left_count])
                else:
                    left_count += 1

            right_count = 1
            while right_count <= (len(right)-2):
                if abs(right[right_count] - right[right_count-1]) >= 100 and abs(right[right_count] - right[right_count+1]) >= 100:
                    del(right[right_count])
                else:
                    right_count += 1
#----------------------------remove noise---------------end

            left_distace = sum(left[:])/len(left)
            right_distance = sum(right[:])/len(right)

    twist.angular.z = 0.003 * (right_distance - left_distace)


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
    left, right = [], []
    #--------------------front--------------------start
    front = []
    #--------------------front--------------------end
    left_distace, right_distance = 0, 0
    timer = 0
    shift = False
    range_controller()
