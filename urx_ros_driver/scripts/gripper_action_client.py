#! /usr/bin/env python

from __future__ import print_function
from std_msgs.msg import String
import rospy
 


# Brings in the SimpleActionClient
import actionlib

import urx_ros.msg



def gripper_client():

	client = actionlib.SimpleActionClient('Gripper', actionlib_gripper.msg.GripperAction)
	
	client.wait_for_server()

	retStr = String()
	retStr.data = "open"	
	
	goal = actionlib_gripper.msg.GripperGoal(request = retStr)

	client.send_goal(goal)

	client.wait_for_result()

	return client.get_result()



if __name__ == '__main__':
	try:
		#initializes a node so the client can publish and subscribe using ROS
		rospy.init_node('gripper_client_py')
		result = gripper_client()
		print("Result:", result.OpenOrClose)
	except rospy.ROSInterruptException:
        	print("program interrupted before completion", file=sys.stderr)
