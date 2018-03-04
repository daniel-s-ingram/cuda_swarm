#!/usr/bin/env python
import rospy
from gazebo_msgs.msg import ModelState
from tf.transformations import quaternion_from_euler
from math import sin, cos

rospy.init_node('swarm_sine_wave', anonymous=True)

swarm_pub = [rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=1) for _ in xrange(100)]
swarm_msg = [ModelState() for _ in xrange(100)]

for i in xrange(10):
	for j in xrange(10):
		swarm_msg[10*i+j].model_name = 'quadrotor%s' % str(10*i+j)
		swarm_msg[10*i+j].pose.position.x = i
		swarm_msg[10*i+j].pose.position.y = j
		swarm_msg[10*i+j].pose.position.z = 2

t = 0
A = 1

while not rospy.is_shutdown():
	quaternion = quaternion_from_euler(-0.5*cos(t), 0.5*cos(t), 0)
	for i in xrange(100):
		try:
			x = int(swarm_msg[i].model_name.split('r')[2][0])
			y = int(swarm_msg[i].model_name.split('r')[2][1])
		except IndexError:
			x = 0
			y = int(swarm_msg[i].model_name.split('r')[2][0])

		swarm_msg[i].pose.position.x = A * sin(t) + x
		swarm_msg[i].pose.position.y = A * sin(t) + y
		swarm_msg[i].pose.position.z = A * sin(t+i) + 2

		swarm_msg[i].pose.orientation.x = quaternion[0]
		swarm_msg[i].pose.orientation.y = quaternion[1]
		swarm_msg[i].pose.orientation.z = quaternion[2]
		swarm_msg[i].pose.orientation.w = quaternion[3]

		swarm_pub[i].publish(swarm_msg[i])

		
	t = t + 0.01