#!/usr/bin/env python
#
# IST Intelligent Machines and Robotics Practice Homework 1
#
# Related ROS Tutorial:
# http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29
#
# Derived from https://raw.githubusercontent.com/ros/ros_tutorials/indigo-devel/rospy_tutorials/001_talker_listener/talker.py
#
# BSD Licence
#
# [...]
#

import rospy
from std_msgs.msg import String

def talker():
    # Initialize the rosnode with the name 'talker'
    rospy.init_node('forward_Tu_Zhi')
    # Create a publisher for publishing (sending) messages on the topic (name) 'chatter'.
    # The messages are of type 'String'
    pub = rospy.Publisher('chatter', String, queue_size=10)
    # Create a Rate object for running a loop with 10 Hz
    rate = rospy.Rate(10) # 10hz
    # As long as this rosnode is running do....
    while not rospy.is_shutdown():
        # Create a string object with a text and the current (ROS) time
        hello_str = "Hello, I am Tu Zhi" % rospy.get_time()
        # Log the current string (prints out on the screen and is also available in rqt_console
        rospy.loginfo(hello_str)
        # Publish the string (send the message)
        pub.publish(hello_str)
        # Sleep as much time as is needed to achive 10 Hz (e.g. if all of the above took 0.01 seconds it will sleep 0.09 seconds)
        rate.sleep()

# The main program
if __name__ == '__main__':
    try:
	# Try to make the talker object - the main look is running in the constructor
        talker()
    # If there was an exception (for example no roscore running) do ... nothing (and then exit)
    except rospy.ROSInterruptException:
        pass