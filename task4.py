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
    global allist
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
        allist = []

    else:
        current_time = rospy.Time.now()
        timer += 1

        if 0 <= timer and timer < 114:
            left.append(sharp)
            allist.append(sharp)

        elif 114 <= timer and timer <= 145:
            left.append(sharp)
            front.append(sharp)
            right.append(sharp)
            allist.append(sharp)


        elif 145 < timer and timer <= 259:
            right.append(sharp)
            allist.append(sharp)
	    #print(allist)


        elif timer == 260:
            i = 1
            while i<=len(front)-1:
                if front[i]-front[i-1]>=50 and front[i]-front[i+1]>=50:
                    del(front[i])
                else:
                    i += 1
            front_distance = max(front[:])
            # front_distance = sum(front[:])/len(front)
            left_distace = sum(left[:])/len(left)
            right_distance = sum(right[:])/len(right)

            now = right_distance- left_distace

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
    
    rospy.init_node('laser_scan_publisher')

    scan_pub = rospy.Publisher('scan', LaserScan, queue_size=50)

    num_readings = 260
    laser_frequency = 260

    count = 0

    scan = LaserScan()

    scan.header.stamp = current_time
    scan.header.frame_id = 'laser_frame'
    scan.angle_min = -1.57
    scan.angle_max = 1.57
    scan.angle_increment = 3.14 / num_readings
    scan.time_increment = (1.0 / laser_frequency) / (num_readings)
    scan.range_min = 0.0
    scan.range_max = 1000.0
    print(allist)

    scan.ranges = allist
    print(scan.ranges)
    scan.intensities = []
    for i in range(0, num_readings):  
        scan.intensities.append(100)

    scan_pub.publish(scan)

# start the line follow
if __name__ == '__main__':
    left, right, front = [], [], []
    left_distace, right_distance, front_distance = 0, 0, 0
    allist = []
    timer = 0
    pre, now = 0, 0
    range_controller()
