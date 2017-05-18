#!/usr/bin/env python
import rospy

# the message that we get from the arduino
from std_msgs.msg import Int32

# the output message controlling the speed and direction of the robot
from geometry_msgs.msg import Twist

from kobuki_msgs.msg import ButtonEvent


def ButtonEventCallback(data):
    if (data.state == ButtonEvent.RELEASED):
        state = "released"
    else:
        state = "pressed"
    if (data.button == ButtonEvent.Button0):
        button = "B0"
    elif (data.button == ButtonEvent.Button1):
        button = "B1"
    else:
        button = "B2"
    rospy.loginfo("Button %s was %s." % (button, state))


def ir_callback(data):
    # Twist is a message type in ros, here we use an Twist message to control kobuki's speed
    # twist. linear.x is the forward velocity, if it is zero, robot will be static,
    # if it is grater than 0, robot will move forward, otherwise, robot will move backward
    # twist.angular.axis is the rotatin velocity around the axis
    #
    # Around which axis do we have to turn? In wich direction will it turn with a positive value?
    # Right hand coordinate system: x forward, y left, z up

    twist = Twist()
    twist.linear.x = 0.01
    twist.angular.z = 0.

    # write your code here




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
    # rospy.Subscriber("/ir_data", Int32, ir_callback)
    rospy.Subscriber("/mobile_base/events/button", ButtonEvent, ButtonEventCallback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


# start the line follow
if __name__ == '__main__':
    range_controller()
