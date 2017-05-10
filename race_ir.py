#!/usr/bin/env python
import rospy

# the message that we get from the arduino
from std_msgs.msg import Int32

# the output message controlling the speed and direction of the robot
from geometry_msgs.msg import Twist

def ir_callback(data):


    # Twist is a message type in ros, here we use an Twist message to control kobuki's speed
    # twist. linear.x is the forward velocity, if it is zero, robot will be static,
    # if it is grater than 0, robot will move forward, otherwise, robot will move backward
    # twist.angular.axis is the rotatin velocity around the axis
    #
    # Around which axis do we have to turn? In wich direction will it turn with a positive value?
    # Right hand coordinate system: x forward, y left, z up

    twist = Twist()
    twist.linear.x = 0.3  # still needs measuring !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    twist.angular.z = 0.
    global i
    global left
    global right


    # write your code here


    # input the data
    data = data.data
    rpr220 = data >> 16
    sharp = data & 0x0000ffff

    # process the data
        # calculate the average
    if rpr220 <= 160:  # the beginning of a circulate
        left, right = [], []
        i = 0
    else:
        if i<130:
            left.append(sharp)
            i += 1

        elif i<260:
            right.append(sharp)
            i += 1

        elif i >= 260:
            left_min = 9999999999999999999999
            left_num = 0
            for j in range(13):
                for i in range(10):
                    t += left[i+j*10]
                t = t/10
                if left_min > t:
                    left_min = t
                    left_num = j
                # left_average[j] = t

            right_min = 9999999999999999999999
            right_num = 0
            for j in range(13):
                for i in range(10):
                    t += right[i+j*10]
                t = t/10
                if right_min > t:
                    right_min = t
                    right_num = j
                # right_average[j] = t

            angular = left_num - 12 + right_num
            # process the twist
            if abs(angular) <= 1:
                di = 0
            elif angular > 1 and angular <= 4:
                di = -1
            elif angular < -1 and angular >= -4:
                di = 1
            elif angular >4 and angular <=8:
                di = -2
            elif angular < -4 and angular >= -8:
                di = 2
            elif angular > 8:
                di = -3
            elif angular < -8:
                di = 3
            else:
                di = 0
            #
            # angular = (left_num -12 + right_num)*(45/13)
            # # process the twist
            # if abs(angular) <= 3.5:
            #     di = 0
            # elif angular > 3.5 and angular <= 14:
            #     di = -1
            # elif angular < -3.5 and angular >= -14:
            #     di = 1
            # elif angular >14 and angular <=28:
            #     di = -2
            # elif angular < -14 and angular >= -28:
            #     di = 2
            # elif angular > 28:
            #     di = -3
            # elif angular < -28:
            #     di = 3
            # else:
            #     di = 0

        twist.angular.z = 0.3 * di # still needs measuring !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



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
    i = 0
    left, right = [], []
    range_controller()

    # for i in range(len(l)):
    #     if l[i][0] < 1 :
    #         print(i)
