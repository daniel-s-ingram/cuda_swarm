#include <string>
#include <iostream>
#include <boost/lexical_cast.hpp>
#include <math.h>
#include <time.h>

#include "ros/ros.h"
#include "gazebo_msgs/ModelState.h"
#include "tf/tf.h"

#include "cuda.h"

__global__ void trajectories(gazebo_msgs::ModelState *msg, float x, float y, float z, float w, float t)
{
	int i = threadIdx.x + blockIdx.x * blockDim.x;

	msg[i].pose.position.x = sin(t) + i/10;
	msg[i].pose.position.y = sin(t) + i%10;
	msg[i].pose.position.z = sin(t+i) + 2;

	msg[i].pose.orientation.x = x;
	msg[i].pose.orientation.y = y;
	msg[i].pose.orientation.z = z;
	msg[i].pose.orientation.w = w;
}

int main(int argc, char **argv)
{
	ros::init(argc, argv, "move_swarm");
	ros::NodeHandle node;

	ros::Publisher swarm_pub = node.advertise<gazebo_msgs::ModelState>("/gazebo/set_model_state", 100);
	gazebo_msgs::ModelState *swarm_msg = new gazebo_msgs::ModelState[100];

	for (int i = 0; i < 100; i++)
	{
		swarm_msg[i].model_name = "quadrotor" + boost::lexical_cast<std::string>(i);
	}

	long msg_size = 100*sizeof(gazebo_msgs::ModelState);
	gazebo_msgs::ModelState *d_msg;

	cudaError_t error;
	if ((error = cudaMalloc((void **)&d_msg, msg_size)) != cudaSuccess)
	{
		printf("Error allocating d_a: %s in %s on line %d\n", cudaGetErrorString(error), __FILE__, __LINE__);
		exit(EXIT_FAILURE);
	}

	if ((error = cudaMemcpy(d_msg, swarm_msg, msg_size, cudaMemcpyHostToDevice)) != cudaSuccess)
	{
		printf("Error copying a to d_a: %s in %s on line %d\n", cudaGetErrorString(error), __FILE__, __LINE__);
		exit(EXIT_FAILURE);
	}

	clock_t initial, final;
	float t = 0;
	tf::Quaternion q;
	while (ros::ok())
	{
		q = tf::createQuaternionFromRPY(-0.5*cos(t), 0.5*cos(t), 0);

		initial = clock();
		trajectories<<<100,512>>>(d_msg, q[0], q[1], q[2], q[3], t);
		cudaMemcpy(swarm_msg, d_msg, msg_size, cudaMemcpyDeviceToHost);
		for (int i = 0; i < 100; i++) swarm_pub.publish(swarm_msg[i]);
		final = clock();

		std::cout << "Time taken by GPU: " << (double)(final-initial)/CLOCKS_PER_SEC << std::endl;

		initial = clock();
		for (int i = 0; i < 100; i++)
		{
			swarm_msg[i].pose.position.x = sin(t) + i/10;
			swarm_msg[i].pose.position.y = sin(t) + i%10;
			swarm_msg[i].pose.position.z = sin(t+i) + 2;

			swarm_msg[i].pose.orientation.x = q[0];
			swarm_msg[i].pose.orientation.y = q[1];
			swarm_msg[i].pose.orientation.z = q[2];
			swarm_msg[i].pose.orientation.w = q[3];

			swarm_pub.publish(swarm_msg[i]);
		}
		final = clock();

		std::cout << "Time taken by CPU: " << (double)(final-initial)/CLOCKS_PER_SEC << std::endl;
		
		t += 0.001;
	}

	delete[] swarm_msg;
	cudaFree(d_msg);
}
