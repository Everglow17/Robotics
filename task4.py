#!/usr/bin/env python
import rospy

# the message that we get from the arduino
from std_msgs.msg import Int32

from sensor_msgs.msg import LaserScan
# the output message controlling the speed and direction of the robot
from geometry_msgs.msg import Twist

from math import sqrt

from kobuki_msgs.msg import ButtonEvent
from kobuki_msgs.msg import BumperEvent

allist=[]
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
    global left, right, front, allist
    global left_distance, right_distance, front_distance
    global timer
    global pre, now, mainswitch
    global scan_pub
    global allist

    # Twist is a message type in ros, here we use an Twist message to control kobuki's speed
    # twist. linear.x is the forward velocity, if it is zero, robot will be static,
    # if it is grater than 0, robot will move forward, otherwise, robot will move backward
    # twist.angular.axis is the rotatin velocity around the axis
    #
    # Around which axis do we have to turn? In wich direction will it turn with a positive value?
    # Right hand coordinate system: x forward, y left, z up

    twist = Twist()
    if mainswitch:
        twist.linear.x = 0.
    else:
        twist.linear.x = 0.1
    twist.angular.z = 0.



    # write your code here
    data = data.data
    rpr220 = data >> 16
    sharp = data & 0x0000ffff

    #read and store
    if rpr220 <= 55:
        #current_time = rospy.Time.now()
        left, right, front = [], [], []
        left_distance, right_distance, front_distance = 0, 0, 0
        timer = -1
        # current_time = rospy.Time.now()


    else:
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



        elif timer == 260:
            # print(allist)

            i = 1
            while i<=len(front)-1:
                if front[i]-front[i-1]>=50 and front[i]-front[i+1]>=50:
                    del(front[i])
                else:
                    i += 1
            front_distance = max(front[:])
            # front_distance = sum(front[:])/len(front)
            left_distance = sum(left[:])/len(left)
            right_distance = sum(right[:])/len(right)

            now = right_distance- left_distance

    # print("front_distance", front_distance)
    # # print("left_distance", left_distance)
    # # print("right_distance", right_distance)
    # print("pre", pre)
    # print("now", now)
    # print(" ")

    if timer == 500:
        pre = now

    if front_distance >= 210:
        twist.linear.x =  0.0

    twist.angular.z = 0.012 * (1 + 0.002*abs(pre - now)) * (right_distance - left_distance)

    # actually publish the twist message
    # if mainswitch:
    #     twist.linear.x = 0.0
    #     twist.angular.z = 0.0





    kobuki_velocity_pub.publish(twist)
    #rospy.init_node('laser_scan_publisher')




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

    scan_pub = rospy.Publisher('scan', LaserScan, queue_size=50)

    num_readings = 100
    laser_frequency = 40

    count = 0
    r=rospy.Rate(1.0)

    while not rospy.is_shutdown():
        print(allist)
        current_time = rospy.Time.now()
        scan = LaserScan()
        scan.header.stamp = current_time
        scan.header.frame_id = 'laser'
        scan.angle_min = -3.14
        scan.angle_max = 3.14
        scan.angle_increment = 6.28 / num_readings
        scan.time_increment = (1.0 / laser_frequency) / (num_readings)
        scan.range_min = 0.0
        scan.range_max = 1000.0

        scan.ranges = allist
        scan.intensities = [100]

        scan_pub.publish(scan)
        count+=1
        r.sleep()


    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


# start the line follow
if __name__ == '__main__':
    left, right, front = [], [], []
    left_distance, right_distance, front_distance = 0, 0, 0
    timer = 0
    pre, now = 0, 0
    mainswitch = False
    allist = []
    range_controller()
