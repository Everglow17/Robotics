#!/usr/bin/env python
import rospy

# the message that we get from the arduino
from std_msgs.msg import Int32

# the output message controlling the speed and direction of the robot
from geometry_msgs.msg import Twist 
from sensor_msgs.msg import LaserScan

from find_path import *

def decode(data):
    sensor_rotate = data >> 16
    sensor_fix = data & ((1 << 16) - 1)

    sensor_fix_pub = rospy.Publisher('data_fix', Int32, queue_size=10)
    sensor_rotate_pub = rospy.Publisher('data_rotate', Int32, queue_size=10)

    sensor_rotate_pub.publish(sensor_rotate)
    sensor_fix_pub.publish(sensor_fix)
    
    return sensor_rotate, sensor_fix


def get_new_laser_scan():
    global laser_scan_at_begin, laser_scan_data_array, laser_scan
    laser_scan = LaserScan()
    laser_scan.header.stamp = rospy.Time.now()
    laser_scan.header.frame_id = "laser_frame"
    laser_scan.angle_min = -1.57
    laser_scan.angle_max = 1.57
    laser_scan.range_min = 0.0  
    laser_scan.range_max = 1000.0
    laser_scan.ranges = []
    laser_scan.intensities = []
    laser_scan_at_begin = True
        
    global twist
    ans_maker = Find_Path(laser_scan_data_array[len(laser_scan_data_array)/2:])
    twist.linear.x, twist.angular.z = ans_maker.get_ans()
    global have_turn_left, have_turn_right
    '''if have_turn_left:
        twist.angular.z -= 0.25
    elif have_turn_right:
        twist.angular.z += 0.25
    if twist.angular.z < -1.5:
        have_turn_right = True
        have_turn_left = False
    elif twist.angular.z > 1.5:
        have_turn_left = True
        have_turn_right = False
    else:
        have_turn_left = False
        have_turn_right = False
    '''
    print(twist.linear.x, twist.angular.z)

    laser_scan_data_array = []


def build_laser_scan():
    global laser_scan_data_array, laser_scan
    data_num = len(laser_scan_data_array)
    laser_scan.ranges = laser_scan_data_array[data_num/2:]
    real_data_num = len(laser_scan.ranges)
    laser_scan.angle_increment = 3.14 / real_data_num
    laser_scan.intensities = [100 for i in range(real_data_num)]
    current_time = rospy.Time.now()
    #print(current_time.to_sec() - laser_scan.header.stamp.to_sec())
    laser_scan.time_increment = (current_time.to_sec() - laser_scan.header.stamp.to_sec()) / data_num
    laser_scan_data_pub.publish(laser_scan)


def change_laser_data_to_number(laser_data):
    if laser_data <= 200:
        return 0.0
    else:
        x = 1 / (laser_data * 1.0)
        real_num = 8*10**11 * x**4 - 8*10**9 * x**3 + 3*10**7 * x**2 - 20142 * x + 0.8087
        if real_num >= 80:
            return 0
        else:
            return real_num


def deal_with_laser_scan(data_rotate, data_fix):
    global laser_scan_at_begin, laser_scan_data_array
    if data_fix < circle_data_limit and laser_scan_at_begin == False:
        laser_scan_at_begin = True
        if len(laser_scan_data_array) != 0:
            build_laser_scan()
        get_new_laser_scan()
    laser_scan_data_array.append(change_laser_data_to_number(data_rotate))
    if data_fix > circle_data_limit:
        laser_scan_at_begin = False


def ir_callback(data):


    # Twist is a message type in ros, here we use an Twist message to control kobuki's speed
    # twist. linear.x is the forward velocity, if it is zero, robot will be static, 
    # if it is grater than 0, robot will move forward, otherwise, robot will move backward
    # twist.angular.axis is the rotatin velocity around the axis 
    # 
    # Around which axis do we have to turn? In wich direction will it turn with a positive value? 
    # Right hand coordinate system: x forward, y left, z up

    global twist

    # write your code here

    data_rotate, data_fix = decode(data.data)

    deal_with_laser_scan(data_rotate, data_fix)

    # actually publish the twist message
    if len(laser_scan_data_array) % 300 == 0 and twist.angular.z != 0:
        twist.angular.z /= 4.0
    kobuki_velocity_pub.publish(twist)
    
    
def range_controller():
    global have_turn_left, have_turn_right
    have_turn_left = False
    have_turn_right = False
    global circle_data_limit # When fix data < this value, means the fix sensor being blocked
    circle_data_limit = 200
    global laser_scan_data_pub  # This is the publisher of the laser_scan value
    global laser_scan_at_begin
    laser_scan_at_begin = False
    global laser_scan_data_array
    laser_scan_data_array = []
    global laser_scan
    laser_scan = LaserScan()
        
    # define the publisher globally
    global kobuki_velocity_pub
    
    # initialize the node
    rospy.init_node('range_controller', anonymous=True)

    # initialize the publisher - to publish Twist message on the topic below...
    kobuki_velocity_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)

    laser_scan_data_pub = rospy.Publisher('laser_scan_data', LaserScan, queue_size=60)

    # subscribe to the topic '/ir_data' of message type Int32. The function 'ir_callback' will be called
    # every time a new message is received - the parameter passed to the function is the message

    global twist
    twist = Twist()
    twist.linear.x = 0.
    twist.angular.z = 0. 

    rospy.Subscriber("/ir_data", Int32, ir_callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

# start the line follow
if __name__ == '__main__':
    range_controller()
    
