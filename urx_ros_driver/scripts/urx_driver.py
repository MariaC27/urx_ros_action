#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped

from signal import signal, SIGINT
from sys import exit

import actionlib

import urx
import logging

# some global variables
robot = None

# publishers
pub_joint_state = None
pub_tool_pose = None
pub_tool_force = None


pub = None 
rate = None
monitor = None

def ctrlc_handler(signa_received, frame):
	rospy.loginfo("shutting down...")
	global robot
	robot.close()
	exit(0)

def initialize_driver():
	global pub, pub_joint_state, robot, rate, monitor, pub_tool_force, pub_tool_pose
	
	# initialize node
	rospy.init_node('urx_driver', anonymous=True)
	
	# setup publishers and subscribers
	pub = rospy.Publisher('chatter', String, queue_size=10)
	pub_joint_state = rospy.Publisher('joint_state', JointState, queue_size=10)
	pub_tool_force = rospy.Publisher('tool_force', Twist, queue_size=10)
	pub_tool_pose = rospy.Publisher('tool_pose', PoseStamped, queue_size=10)
	
	# connect to the robot
	logging.basicConfig(level=logging.INFO)
	robot = urx.Robot("172.22.22.2",use_rt=True)
	rospy.loginfo("Connection to the robot established.")
	
	# get pointer to real time monitor
	monitor = robot.get_realtime_monitor()

def loop():
	global pub, pub_joint_state, robot, rate, monitor, pub_tool_force, pub_tool_pose
	
	
	# get data from robot
	#pose_l = robot.getl(wait=True) # this seems to be identical to pose_p
	
	# end effector pose
	pose_p = robot.get_pose(wait=False)
	
	# joint positions
	joint_positions = robot.getj(wait=False)
	
	# force at the tool-center-point
	tcp_force = monitor.getTCFForce(True)
     
	#print pose_l
	print pose_p
	print joint_positions
	print tcp_force
	
	
	
	# publish the data -- TO DO
	

def urx_background():
    global pub, pub_joint_state, robot, rate
    
    rate = rospy.Rate(200) # 10hz
    while not rospy.is_shutdown():
		# get data from robot and publish it
        loop()
        
		# sleep to maintain frame rate
        rate.sleep()

if __name__ == '__main__':
	try:
		# register ctrl-c handler
		signal(SIGINT, ctrlc_handler)
		
		# init driver
		initialize_driver()
		
		# run loop in background
		urx_background()
		
	except rospy.ROSInterruptException:
		pass
