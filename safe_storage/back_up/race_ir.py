#!/usr/bin/env python
import rospy

# the message that we get from the arduino
from std_msgs.msg import Int32

# the output message controlling the speed and direction of the robot
from geometry_msgs.msg import Twist
#
# import curses
#
# # set up curses (console input and output system)
# stdscr = curses.initscr()
# curses.noecho()
# curses.cbreak()
# stdscr.nodelay(1)
# stdscr.keypad(1)
#
# # global variable for steering commands to the robot
# twist = Twist()
#
# shapeCounter = 0
#
# # This is also responsible for the printout
#
#       #shapeCounter += 1
# #def printInfo():
#     #global twist
#     #global stdscr
#     #global activeShape
#     # prepare an informative line of text
#     #text = "Kobuki shape %d forward %f  turn %f     " % (activeShape, twist.linear.x, twist.angular.z)
#     # print out the text (at position 0, 0)
#     #stdscr.addstr(0, 0, text)
#
# def pub_in():
#     global shapeCounter
#
#     turnSpeed = 1   #########################
#     forwardSpeed = 1  ########################
#
#     data=____________#(form unknown)[(linear,angle),(linear,angle)]
#     twist.linear.x = forwardSpeed
#
#     #this is a stupid algorithim/can be improved
#
#     #set a set omega
#     while not rospy.is_shutdown(): ####################################
#         shapeCounter += 1
#         if shapeCounter < 1000:##############################
#             twist.angular.z = 1###############################
#         else:
#             twist.angular.z = 0###########################
#         pub.publish(twist)
#         # Sleep as much time as is needed to achive 100 Hz
#         rate.sleep()
#
#

def ir_callback(data):


    # Twist is a message type in ros, here we use an Twist message to control kobuki's speed
    # twist. linear.x is the forward velocity, if it is zero, robot will be static,
    # if it is grater than 0, robot will move forward, otherwise, robot will move backward
    # twist.angular.axis is the rotatin velocity around the axis
    #
    # Around which axis do we have to turn? In wich direction will it turn with a positive value?
    # Right hand coordinate system: x forward, y left, z up

    twist = Twist()
    twist.linear.x = 0.2 # still needs measuring !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    twist.angular.z = 0.0
    global i
    global left
    global right
    global left_average
    global right_average
    global di
    global tt

    # write your code here


    # input the data
    data = data.data
    rpr220 = data >> 16
    sharp = data & 0x0000ffff
    # rpr220 = int("0b"+str(rpr220),
    # sharp = int("0b"+str(sharp), 2)

    # process the data
        # calculate the average
    # print(sharp)
    # if rpr220 <= 50:
    #     # print("tt", tt)
    #     # print("len(tt)", len(tt))
    #     # tt = []
    # else:
    #     tt.append(rpr220)
        # print(tt)
        # print(len(tt))

    if rpr220 <= 55:  # the beginning of a circulate
        left, right = [], []
        left_average, right_average = [], []
        i = 0
        # print("rpr220", rpr220)
    else:
        if i<130:
            left.append(sharp)
            i += 1

        elif i<260:
            right.append(sharp)
            i += 1

        elif i >= 260:
            left_max = -1
            left_num = 0
            for j in range(13):
                t = 0
                for i in range(10):
                    t += left[i+j*10]
                t = t/10
                if left_max < t:
                    left_max = t
                    left_num = j
                left_average.append(t)
            print("left_average", left_average)

            right_max = -1
            right_num = 0
            for j in range(13):
                t = 0
                for i in range(10):
                    t += right[i+j*10]
                t = t/10
                if right_max < t:
                    right_max = t
                    right_num = j
                right_average.append(t)
            print("right_average", right_average)

            angular = left_num - 12 + right_num
            di = 0
            # process the twist
            if abs(angular) <= 1:
                di = 0
            elif angular > 1 and angular <= 4:
                di = -3
            elif angular < -1 and angular >= -4:
                di = 3
            elif angular >4 and angular <=8:
                di = -5
            elif angular < -4 and angular >= -8:
                di = 5
            elif angular > 8:
                di = -7
            elif angular < -8:
                di = 7
            else:
                di = 0

            # print("left_num", left_num-12)
            # print("right_num", right_num)
            # print("di", di)
            # print()
        twist.angular.z = -0.07 * di  # still needs measuring !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


            # test_print=================================

            # print("left_num", left_num-12)
            # print("right_num", right_num)
            # # print("left_average", left_average)
            # print("right_average", right_average)


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
    i, di = 0, 0
    tt = []
    left, right= [], []
    left_average, right_average = [], []
    range_controller()

    # for i in range(len(l)):
    #     if l[i][0] < 1 :
    #         print(i)

    # try:
    #     # Try to make the shape object - the main loop is running in the constructor
    #     pub_in()
    # # If there was an exception (for example no roscore running) do ... nothing (and then exit)
    # except rospy.ROSInterruptException:
    #     pass
    # finally:
    #     # restore the terminal
    #     curses.nocbreak(); stdscr.keypad(0); curses.echo()
    #     curses.endwin()
