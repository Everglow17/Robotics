#!/usr/bin/env python
#
# IST Intelligent Machines and Robotics Practice 1
#

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

import curses

# set up curses (console input and output system)
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.nodelay(1)
stdscr.keypad(1)

# global variable for steering commands to the robot
twist = Twist()

activeShape = 0
shapeCounter = 0


# Function that reads the keyboard and adjusts the twist message accordingly.
# This is also responsible for the printout
def readKeys():
    global activeShape
    global shapeCounter
    # read a key from the keyboard
    key = stdscr.getch()

    # check which key was pressed (if any)
    if key == ord("1"):
        activeShape = 1
        shapeCounter = 0
    elif key == ord("2"):
        activeShape = 2
        shapeCounter = 0
    elif key == ord("3"):
        activeShape = 3
        shapeCounter = 0
    elif key != -1:
        activeShape = 0
    else:
        # key is -1 == no key pressed
        shapeCounter += 1


def shape_1():
    global activeShape
    global shapeCounter

    turnSpeed = 0.93
    forwardSpeed = 0.4

    if shapeCounter < 200:
        twist.linear.x = forwardSpeed
    elif shapeCounter < 400:
        twist.linear.x = 0
        twist.angular.z = turnSpeed
    elif shapeCounter < 600:
        twist.angular.z = 0
        twist.linear.x = forwardSpeed
    elif shapeCounter < 800:
        twist.linear.x = 0
        twist.angular.z = turnSpeed
    elif shapeCounter < 1000:
        twist.angular.z = 0
        twist.linear.x = forwardSpeed
    elif shapeCounter < 1200:
        twist.linear.x = 0
        twist.angular.z = turnSpeed
    elif shapeCounter < 1400:
        twist.angular.z = 0
        twist.linear.x = forwardSpeed
    elif shapeCounter < 1600:
        twist.linear.x = 0
        twist.angular.z = turnSpeed
    else:
        activeShape = 0
        twist.angular.z = 0
        twist.linear.x = 0


def shape_2():
    global shapeCounter

    if shapeCounter < 200:
        twist.linear.x = 0.3
    else:
        activeShape = 0
        twist.angular.z = 0
        twist.linear.x = 0


def shape_3():
    """self write function"""
    global shapeCounter

    if shapeCounter < 200:  # print the first edge
        twist.linear.x = 0.3
        twist.angular.z = 0
    elif shapeCounter < 400:  # rotate 90 degrees
        twist.linear.x = 0
        twist.angular.z = 1.2
    elif shapeCounter < 600:  # print the second edge
        twist.linear.x = 0.3
        twist.angular.z = 0
    elif shapeCounter < 800:  # rotate 90 degrees
        twist.linear.x = 0
        twist.angular.z = 1.2
    elif shapeCounter < 1000:  # print the third edge
        twist.linear.x = 0.3
        twist.angular.z = 0
    elif shapeCounter < 1200:  # rotate 90 degrees
        twist.linear.x = 0
        twist.angular.z = 1.2
    elif shapeCounter < 1400:  # print the forth edge
        twist.linear.x = 0
        twist.angular.z = 1.2
    else:
        activeShape = 0
        twist.angular.z = 0
        twist.linear.x = 0


def printInfo():
    global twist
    global stdscr
    global activeShape
    # prepare an informative line of text
    text = "Kobuki shape %d forward %f  turn %f     " % (activeShape, twist.linear.x, twist.angular.z)
    # print out the text (at position 0, 0)
    stdscr.addstr(0, 0, text)


# The main loop of our controller
def shape():
    global activeShape
    global shapeCounter

    # Initialize the rosnode with the name 'keyop'
    rospy.init_node('keyop')
    # Create a publisher for publishing (sending) messages on the topic (name) '/mobile_base/commands/velocity'.
    # The messages are of type 'Twist'
    pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
    # Create a Rate object for running a loop with 100 Hz
    rate = rospy.Rate(100)  # 100hz

    # As long as this rosnode is running do....
    while not rospy.is_shutdown():

        # read the keyboard input, update the twist message, and print some info
        readKeys()

        if activeShape == 1:
            shape_1()
        elif activeShape == 2:
            shape_2()
        elif activeShape == 3:
            shape_3()
        else:
            twist.linear.x = 0
            twist.angular.z = 0

        printInfo()

        # Publish the updated twist message
        pub.publish(twist)
        # Sleep as much time as is needed to achive 100 Hz
        rate.sleep()


# The main program
if __name__ == '__main__':
    try:
        # Try to make the shape object - the main loop is running in the constructor
        shape()
    # If there was an exception (for example no roscore running) do ... nothing (and then exit)
    except rospy.ROSInterruptException:
        pass
    finally:
        # restore the terminal
        curses.nocbreak();
        stdscr.keypad(0);
        curses.echo()
        curses.endwin()