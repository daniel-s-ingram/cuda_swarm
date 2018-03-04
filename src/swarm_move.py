#!/usr/bin/env python
import rospy
from gazebo_msgs.msg import ModelState
from tf.transformations import quaternion_from_euler
from math import sin, cos

rospy.init_node('swarm_sine_wave', anonymous=True)

swarm_pub = [rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=1) for _ in xrange(25)]
swarm_msg = [ModelState() for _ in xrange(25)]

for i in xrange(5):
	for j in xrange(5):
		swarm_msg[5*i+j].model_name = 'quadrotor%s' % str(5*i+j)
		swarm_msg[5*i+j].pose.position.x = i
		swarm_msg[5*i+j].pose.position.y = j
		swarm_msg[5*i+j].pose.position.z = 2

x = 0
A = 1

while not rospy.is_shutdown():
	quaternion = quaternion_from_euler(0, 0.25*cos(x), 0)
	for i in xrange(5):
		swarm_msg[i].pose.position.x = A*sin(x)+5
		swarm_msg[i].pose.orientation.x = quaternion[0]
		swarm_msg[i].pose.orientation.y = quaternion[1]
		swarm_msg[i].pose.orientation.z = quaternion[2]
		swarm_msg[i].pose.orientation.w = quaternion[3]
		swarm_pub[i].publish(swarm_msg[i])

	for i in xrange(5, 10):
		swarm_msg[i].pose.position.x = A*sin(x)+4
		swarm_msg[i].pose.orientation.x = quaternion[0]
		swarm_msg[i].pose.orientation.y = quaternion[1]
		swarm_msg[i].pose.orientation.z = quaternion[2]
		swarm_msg[i].pose.orientation.w = quaternion[3]
		swarm_pub[i].publish(swarm_msg[i])

	for i in xrange(10, 15):
		swarm_msg[i].pose.position.x = A*sin(x)+3
		swarm_msg[i].pose.orientation.x = quaternion[0]
		swarm_msg[i].pose.orientation.y = quaternion[1]
		swarm_msg[i].pose.orientation.z = quaternion[2]
		swarm_msg[i].pose.orientation.w = quaternion[3]
		swarm_pub[i].publish(swarm_msg[i])

	for i in xrange(15, 20):
		swarm_msg[i].pose.position.x = A*sin(x)+2
		swarm_msg[i].pose.orientation.x = quaternion[0]
		swarm_msg[i].pose.orientation.y = quaternion[1]
		swarm_msg[i].pose.orientation.z = quaternion[2]
		swarm_msg[i].pose.orientation.w = quaternion[3]
		swarm_pub[i].publish(swarm_msg[i])

	for i in xrange(20, 25):
		swarm_msg[i].pose.position.x = A*sin(x)+1
		swarm_msg[i].pose.orientation.x = quaternion[0]
		swarm_msg[i].pose.orientation.y = quaternion[1]
		swarm_msg[i].pose.orientation.z = quaternion[2]
		swarm_msg[i].pose.orientation.w = quaternion[3]
		swarm_pub[i].publish(swarm_msg[i])
		
	x = x + 0.001