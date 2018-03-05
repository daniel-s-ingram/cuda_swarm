#include <string>
#include <iostream>
#include <boost/lexical_cast.hpp>
#include <math.h>

#include "ros/ros.h"
#include "gazebo_msgs/ModelState.h"

#include "cuda.h"

int main(int argc, char **argv)
{
	ros::init(argc, argv, "move_swarm");
	ros::NodeHandle node;

	ros::Publisher *swarm_pub;
	gazebo_msgs::ModelState *swarm_msg;

	swarm_pub = (ros::Publisher *)malloc(100*sizeof(ros::Publisher));
	swarm_msg = (gazebo_msgs::ModelState *)malloc(100*sizeof(gazebo_msgs::ModelState));

	for (int i = 0; i < 100; i++)
	{
		swarm_pub[i] = node.advertise<gazebo_msgs::ModelState>("/gazebo/set_model_state", 1);
		swarm_msg[i].model_name = "quadrotor" + boost::lexical_cast<std::string>(i);
	}

	int t = 0;
	while (ros::ok())
	{
		for (int i = 0; i < 100; i++)
		{
			swarm_msg[i].pose.position.x = 2.5*sin(t) + i/10;
			swarm_msg[i].pose.position.y = 2.5*sin(t) + i%10;
			swarm_msg[i].pose.position.z = 2;

			swarm_pub[i].publish(swarm_msg[i]);
		}
		t += 0.001;
	}

	free(swarm_pub); free(swarm_msg);
}
