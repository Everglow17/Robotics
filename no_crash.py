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
    twist.linear.x = 0.25
    twist.angular.z = 0.



    # write your code here
    data = data.data
    rpr220 = data >> 16
    sharp = data & 0x0000ffff

    #Edition 1:
    #only judge left 80 degree and right 80 degree, aviod crash
    global timer, istwist, twistimer, left_nz, right_nz
    global left_max
    global right_max
    global di, left, right, left_average, right_average, shift

    #initialize the circulate

    if istwist:
        twistimer += 1
    if twistimer >= 300:
        istwist = False
        twistimer = 0

    if rpr220 <= 55:
        left, right = [], []
        left_average, right_average = [], []
        timer = -1
        shift = False

    else:
        timer += 1

        if timer < 110:
            left.append(sharp)


        elif timer > 149 and timer < 260:
            right.append(sharp)
            if timer == 259:
                shift = True

        elif timer >= 260 and shift:
            shift = False

            left_nz = [True for i in range(109)]
            for i in range(1, 110):
                if left[i] - left[i - 1] >= 50 and left[i] - left[i + 1] >= 50:
                    left_nz[i] = False

            right_nz = [True for i in range(109)]
            for i in range(1, 110):
                if right[i] - right[i - 1] >= 50 and right[i] - right[i + 1] >= 50:
                    right_nz[i] = False

            left_max = 0
            left_num = 0

            for j in range(11):
                t = 0
                ct = 0
                for i in range(10):
                    if left_nz:
                        ct += 1
                        t += left[i+j*10]
                t = t/ct
                left_average.append(t)
                if left_max < t:
                    left_max = t
                    left_num = j
            left_num = left_num - 11

            right_max = 0
            right_num = 0
            for j in range(11):
                t = 0
                ct = 0
                for i in range(10):
                    if right_nz:
                        ct += 1
                        t += right[i+j*10]
                t = t/ct
                right_average.append(t)
                if right_max < t:
                    right_max = t
                    right_num = j

            angular = left_num + right_num

            if left_max >= 200 or right_max >= 200:
                istwist = True

            if abs(angular) <= 1:
                di = 0
            elif angular > 1 and angular <= 4:
                di = 0.1
            elif angular < -1 and angular >= -4:
                di = -0.1
            elif angular > 4 and angular <= 8:
                di = 0.2
            elif angular < -4 and angular >=-8:
                di = -0.2
            elif angular > 8:
                di = 0.3
            elif angular < -8:
                di = -0.3

    if left_max >= 280 and istwist:
        twist.linear.x = 0.3
        twist.angular.z = -0.7

    elif right_max >= 280 and istwist:
        twist.linear.x = 0.3
        twist.angular.z = 0.7

    else:
        twist.angular.z = di

    # print("left_max", left_max)
    # print("right_max", right_max)
    # print("left_average", left_average)
    # print("right_average", right_average)
    # print("twist.angular.z", twist.angular.z)
    print(" ")
    print("left", left)
    print("right", right)









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
    left_max, right_max = 0, 0
    left, right = [], []
    left_average, right_average = [], []
    left_nz, right_nz = [], []
    timer, twistimer = 0, 0
    shift, istwist = False, False
    di = 0

    range_controller()
