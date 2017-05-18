#!/usr/bin/env python
import rospy

# the message that we get from the arduino
from std_msgs.msg import Int32

# the output message controlling the speed and direction of the robot
from geometry_msgs.msg import Twist

from kobuki_msgs.msg import ButtonEvent
from kobuki_msgs.msg import BumperEvent


def ButtonEventCallback(data):
    global mainswitch

    if (data.state == ButtonEvent.RELEASED):
        state = "released"
    else:
        state = "pressed"
    if (data.button == ButtonEvent.Button0):
        button = "B0"

        mainswitch = False

    elif (data.button == ButtonEvent.Button1):
        button = "B1"
    else:
        button = "B2"
    rospy.loginfo("Button %s was %s." % (button, state))

def BumperEventCallback(data):
    global mainswitch

    if ( data.state == BumperEvent.RELEASED ) :
        state = "released"
    else:
        state = "pressed"

        mainswitch = True

    if ( data.bumper == BumperEvent.LEFT ) :
        bumper = "Left"
    elif ( data.bumper == BumperEvent.CENTER ) :
        bumper = "Center"
    else:
        bumper = "Right"
    rospy.loginfo("%s bumper is %s."%(bumper, state))

def ir_callback(data):

    global left, right, front
    global left_distace, right_distance, front_distance
    global timer

    # Twist is a message type in ros, here we use an Twist message to control kobuki's speed
    # twist. linear.x is the forward velocity, if it is zero, robot will be static,
    # if it is grater than 0, robot will move forward, otherwise, robot will move backward
    # twist.angular.axis is the rotatin velocity around the axis
    #
    # Around which axis do we have to turn? In wich direction will it turn with a positive value?
    # Right hand coordinate system: x forward, y left, z up

    twist = Twist()
    twist.linear.x = 0.15
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

        if 0 <= timer and timer < 124:
            left.append(sharp)

        elif 124 <= timer and timer <= 135:
            left.append(sharp)
            front.append(sharp)
            right.append(sharp)

        elif 135 < timer and timer <= 259:
            right.append(sharp)

        elif timer == 260:
            front_distance = sum(front[:])/len(front)
            left_distace = sum(left[:])/len(left)
            right_distance = sum(right[:])/len(right)
    print("front_distance", front_distance)
    print("left_distace", left_distace)
    print("right_distance", right_distance)
    if front_distance >= 220:
        twist.linear.x =  0.0
    print(twist.linear.x)
    twist.angular.z = 0.012 * (right_distance - left_distace)

    # actually publish the twist message
    if mainswitch:
        twist.linear.x = 0.0
        twist.angular.z = 0.0
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

    rospy.Subscriber("/mobile_base/events/button", ButtonEvent, ButtonEventCallback)
    rospy.Subscriber("/mobile_base/events/bumper", BumperEvent, BumperEventCallback)
    rospy.Subscriber("/ir_data", Int32, ir_callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


# start the line follow
if __name__ == '__main__':
    mainswitch = False
    left, right, front = [], [], []
    left_distace, right_distance, front_distance = 0, 0, 0
    timer = 0

    range_controller()
