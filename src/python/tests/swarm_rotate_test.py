#!/usr/bin/env python
import rospy
from gazebo_msgs.msg import ModelState
from tf.transformations import quaternion_from_euler

rospy.init_node('swarm_rotate_test', anonymous=True)

swarm_pub = [rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=1) for _ in xrange(25)]
swarm_msg = [ModelState() for _ in xrange(25)]

for i in xrange(5):
	for j in xrange(5):
		swarm_msg[5*i+j].model_name = 'quadrotor%s' % str(5*i+j)
		swarm_msg[5*i+j].pose.position.x = i
		swarm_msg[5*i+j].pose.position.y = j

z = 0

while not rospy.is_shutdown():
	for i in xrange(25):
		quaternion = quaternion_from_euler(0, 0, z)

		swarm_msg[i].pose.orientation.x = quaternion[0]
		swarm_msg[i].pose.orientation.y = quaternion[1]
		swarm_msg[i].pose.orientation.z = quaternion[2]
		swarm_msg[i].pose.orientation.w = quaternion[3]

		swarm_pub[i].publish(swarm_msg[i])
		
	z = z + 0.01