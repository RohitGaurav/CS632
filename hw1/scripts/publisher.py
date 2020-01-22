#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from p2os_msgs.msg import MotorState
import sys

class Publisher():
    def __init__(self):
        rospy.loginfo('Initializing Publisher Node')
        rospy.init_node('publisher')
        rospy.on_shutdown(self.cleanup)
        self.cmd_vel_pub_time = 0
        self.motor_enabled = False
        self.pub_time = False
        self.start_time = 0
        self.end_time = 0
        self.motor_state_pub = rospy.Publisher('/cmd_motor_state', MotorState, queue_size=10, latch=True) # Message Latched
        self.motor_cmd_vel_pub = rospy.Publisher('/r1/cmd_vel', Twist, queue_size=10)
        self.pub_rate = rospy.Rate(10)

    def enable_motors(self):
        motor_state_msg = MotorState()
        motor_state_msg.state = 1
        self.motor_state_pub.publish(motor_state_msg)
        rospy.loginfo("Motors Enabled")
        self.motor_enabled = True
    def main(self):
        if not self.motor_enabled:
            self.enable_motors()
        while not rospy.is_shutdown():
            if not self.pub_time:
                self.cmd_vel_pub_time = input('Enter Publish Time ')
                cmd_vel_msg = Twist()
                cmd_vel_msg.linear.x = 0.5
                cmd_vel_msg.angular.z = 0.4
                self.pub_time = True
                self.start_time = rospy.Time.now()
            self.motor_cmd_vel_pub.publish(cmd_vel_msg)
            self.pub_rate.sleep()
            self.end_time = rospy.Time.now()
            if self.end_time.secs - self.start_time.secs == int(self.cmd_vel_pub_time):
                rospy.loginfo('Stopping robot')
                cmd_vel_msg.linear.x = 0
                cmd_vel_msg.angular.z = 0
                self.motor_cmd_vel_pub.publish(cmd_vel_msg)
                self.pub_time = False
                # break
    
    def cleanup(self):
        rospy.loginfo("Exiting Node")
        

if __name__ == "__main__":
    node = Publisher()
    node.main()
    
        




