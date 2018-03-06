#include <string>
#include <iostream>
#include <boost/lexical_cast.hpp>
#include <math.h>

#include "ros/ros.h"
#include "gazebo_msgs/ModelState.h"
#include "tf/tf.h"

#include "cuda.h"

__global__ void trajectories(gazebo_msgs::ModelState *msg, tf::Quaternion *quat, float t)
{

}

int main(int argc, char **argv)
{
	ros::init(argc, argv, "move_swarm");
	ros::NodeHandle node;

	ros::Publisher *swarm_pub = new ros::Publisher[100];
	gazebo_msgs::ModelState *swarm_msg = new gazebo_msgs::ModelState[100];

	for (int i = 0; i < 100; i++)
	{
		swarm_pub[i] = node.advertise<gazebo_msgs::ModelState>("/gazebo/set_model_state", 1);
		swarm_msg[i].model_name = "quadrotor" + boost::lexical_cast<std::string>(i);
	}

	cudaError_t error;
	gazebo_msgs::ModelState *d_msg;
	if ((error = cudaMalloc((void **)&d_msg, 100*sizeof(gazebo_msgs::ModelState))) != cudaSuccess)
	{
		printf("Error allocating d_a: %s in %s on line %d\n", cudaGetErrorString(error), __FILE__, __LINE__);
		exit(EXIT_FAILURE);
	}

	if ((error = cudaMemcpy(d_msg, swarm_msg, 100*sizeof(gazebo_msgs::ModelState), cudaMemcpyHostToDevice)) != cudaSuccess)
	{
		printf("Error copying a to d_a: %s in %s on line %d\n", cudaGetErrorString(error), __FILE__, __LINE__);
		exit(EXIT_FAILURE);
	}

	float t = 0;
	tf::Quaternion quaternion;
	while (ros::ok())
	{
		quaternion = tf::createQuaternionFromRPY(-0.5*cos(t), 0.5*cos(t), 0);
		
		for (int i = 0; i < 100; i++)
		{
			swarm_msg[i].pose.position.x = sin(t) + i/10;
			swarm_msg[i].pose.position.y = sin(t) + i%10;
			swarm_msg[i].pose.position.z = sin(t+i) + 2;

			swarm_msg[i].pose.orientation.x = quaternion[0];
			swarm_msg[i].pose.orientation.y = quaternion[1];
			swarm_msg[i].pose.orientation.z = quaternion[2];
			swarm_msg[i].pose.orientation.w = quaternion[3];

			swarm_pub[i].publish(swarm_msg[i]);
		}
		t += 0.001;
	}

	delete[] swarm_pub; 
	delete[] swarm_msg;
}
