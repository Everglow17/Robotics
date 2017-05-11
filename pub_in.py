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

shapeCounter = 0

# This is also responsible for the printout

      #shapeCounter += 1
#def printInfo():
    #global twist
    #global stdscr
    #global activeShape
    # prepare an informative line of text
    #text = "Kobuki shape %d forward %f  turn %f     " % (activeShape, twist.linear.x, twist.angular.z)
    # print out the text (at position 0, 0)
    #stdscr.addstr(0, 0, text)

def pub_in():
    global shapeCounter

    turnSpeed = 1   #########################
    forwardSpeed = 1  ########################

    data=____________#(form unknown)[(linear,angle),(linear,angle)]
    twist.linear.x = forwardSpeed

    #this is a stupid algorithim/can be improved

    #set a set omega
    while not rospy.is_shutdown(): ####################################
        shapeCounter += 1
        if shapeCounter < 1000:##############################
            twist.angular.z = 1###############################
        else:
            twist.angular.z = 0###########################
        pub.publish(twist)
        # Sleep as much time as is needed to achive 100 Hz
        rate.sleep()

# The main program
if __name__ == '__main__':
    try:
        # Try to make the shape object - the main loop is running in the constructor
        pub_in()
    # If there was an exception (for example no roscore running) do ... nothing (and then exit)
    except rospy.ROSInterruptException:
        pass
    finally:
        # restore the terminal
        curses.nocbreak(); stdscr.keypad(0); curses.echo()
        curses.endwin()
