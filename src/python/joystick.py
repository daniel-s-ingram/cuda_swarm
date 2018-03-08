#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from gazebo_msgs.msg import ModelState
from tf.transformations import quaternion_from_euler
from math import floor, cos

vx = 0
vy = 0
vz = 0

def joy_callback(msg):
	global vx, vy, vz
	vx = -msg.axes[3]
	vy = msg.axes[4]
	if not msg.buttons[6] and msg.buttons[7]:
		vz = 1
	elif msg.buttons[6] and not msg.buttons[7]:
		vz = -1
	else:
		vz = 0

rospy.init_node('joystick', anonymous=True)

swarm_pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=1000)
swarm_msg = [ModelState() for _ in xrange(100)]
for i in xrange(100):
	swarm_msg[i].model_name = 'quadrotor' + str(i)

rospy.Subscriber('/joy', Joy, joy_callback)

dt = 0.1
x = 0
y = 0
z = 0

while not rospy.is_shutdown():
	x = x + vx*dt
	y = y + vy*dt
	z = z + vz*dt

	q = quaternion_from_euler(-0.25*vy, 0.25*vx, 0)

	for i in xrange(100):
		swarm_msg[i].pose.position.x = x + floor(i/10)
		swarm_msg[i].pose.position.y = y + i%10
		swarm_msg[i].pose.position.z = z

		swarm_msg[i].pose.orientation.x = q[0]
		swarm_msg[i].pose.orientation.y = q[1]
		swarm_msg[i].pose.orientation.z = q[2]
		swarm_msg[i].pose.orientation.w = q[3]

		swarm_pub.publish(swarm_msg[i])

