#! /usr/bin/env python

from std_msgs.msg import String
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

import rospy

import urx

import sys

import actionlib

import urx_ros.msg


class GripperAction(object):
	_result = actionlib_gripper.msg.GripperResult()





	def __init__(self, name):
		self._action_name = name
		self._as = actionlib.SimpleActionServer(self._action_name, 
		actionlib_gripper.msg.GripperAction, execute_cb=self.execute_cb,
		auto_start = False)

		self._as.start()
		


	def execute_cb(self, goal):
		#helper variables
		r = rospy.Rate(1)
		success = True

		rospy.loginfo('%s: Executing, returning value of %s' %(self._action_name,
		goal.request))

		if self._as.is_preempt_requested():
                	rospy.loginfo('%s: Preempted' % self._action_name)
                	self._as.set_preempted()
                	success = False
                		


		if success:
			
			
			rob = urx.Robot("172.22.22.2")
	

			robotiqgrip = Robotiq_Two_Finger_Gripper(rob, 1.25)

			rospy.loginfo('Print request of %s'%(goal.request))

			#need to do this so data type matches the request
			#std_msgs/String is not the same as a regular string!
			compStr1 = String()
			compStr1.data = "open"

			compStr2 = String()
			compStr2.data = "close"
			
			
			if (goal.request == compStr1):
				#open gripper:
				check = True
				robotiqgrip.open_gripper()
				rospy.loginfo('Reached if')
				

			elif (goal.request == compStr2):
				#close gripper:
				check = False
				robotiqgrip.close_gripper()
				rospy.loginfo('Reached elseif') 
			
			#rob.send_program(robotiqgrip.ret_program_to_run())
			rob.close()
			sys.exit() 	
			
			self._result.OpenOrClose = check
			rospy.loginfo('%s: Succeeded' % self._action_name)
	            	self._as.set_succeeded(self._result)

			
if __name__ == '__main__':
	rospy.init_node('Gripper')
	server = GripperAction(rospy.get_name())

       
	rospy.spin()


