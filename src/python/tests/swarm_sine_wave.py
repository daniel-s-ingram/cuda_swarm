#!/usr/bin/env python
import rospy
from gazebo_msgs.msg import ModelState
from math import sin

rospy.init_node('swarm_sine_wave', anonymous=True)

swarm_pub = [rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=1) for _ in xrange(100)]
swarm_msg = [ModelState() for _ in xrange(100)]

for i in xrange(10):
	for j in xrange(10):
		swarm_msg[10*i+j].model_name = 'quadrotor%s' % str(10*i+j)
		swarm_msg[10*i+j].pose.position.x = i
		swarm_msg[10*i+j].pose.position.y = j
		swarm_msg[10*i+j].pose.position.z = 2

z = 0
A = 1

while not rospy.is_shutdown():
	for i in xrange(100):
		swarm_msg[i].pose.position.z = A*sin(z+i)+2
		swarm_pub[i].publish(swarm_msg[i])
		
	z = z + 0.01