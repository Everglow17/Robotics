#!/usr/bin/env python
import rospy

# the message that we get from the arduino
from std_msgs.msg import Int32

# the output message controlling the speed and direction of the robot
from geometry_msgs.msg import Twist

from math import sqrt

def ir_callback(data):
#----------------------------crash---------------start
    global front, front_distance
    global istwist, twistimer
#----------------------------crash---------end

    global left, right
    global left_distance, right_distance
    global timer

    twist = Twist()
    twist.linear.x = 0.15
    twist.angular.z = 0.

    data = data.data
    rpr220 = data >> 16
    sharp = data & 0x0000ffff

#----------------------------crash---------------start
    if istwist:
        twistimer += 1
    if twistimer >= 100:
        istwist = False
        twistimer = 0
#----------------------------crash--------end

    #read and store
    if rpr220 <= 55:
        left, right = [], []
        left_distance, right_distance = 0, 0
        timer = -1
        shift = False
#----------------------------crash---------------start
        front = []
#----------------------------crash--------end

    else:
        timer += 1

        if 64 <= timer and timer <= 83:
            left.append(sharp)

#----------------------------crash---------------start
        if 120 <= timer and timer <= 149:
            front.append(sharp)
#----------------------------crash------end

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
#----------------------------remove noise----end

#----------------------------crash---------------------start
            front_distance = sum(front[:])/len(front)
            if front_distance >= 250:
                istwist = True
#----------------------------crash-----------end

            left_distance = sum(left[:])/len(left)
            right_distance = sum(right[:])/len(right)
    print("left", left)
    print("right", right)
    print("left_distance", left_distance)
    print("right_distance", right_distance)
    print("front", front)
    print("front_distance", front_distance)

#--------------------------with crash----------------start
    if front_distance >= 250 and istwist:
        if left_distance < right_distance:
            twist.angular.z = -0.35
            twist.angular.x = -0.05
        elif left_distance < right_distance:
            twist.angular.z = 0.35
            twist.angular.x = 0.05
    else:
        twist.angular.z  = 0.03 * (right_distance - left_distance)
#--------------------------without crash-----end


#--------------------------without crash----------------start
    # twist.angular.z = 0.003 * (right_distance - left_distance)
#--------------------------without crash-----end

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
    left_distance, right_distance = 0, 0
    timer = -1
    #--------------------crash--------------------start
    front = []
    front_distance = 0
    twistimer = 0
    istwist = False
    #--------------------crash--------------------end
    range_controller()
