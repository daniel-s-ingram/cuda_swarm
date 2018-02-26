cmake_minimum_required(VERSION 2.8.3)
project(cuda_swarm)

find_package(catkin REQUIRED COMPONENTS
  cuda
  roscpp
  rospy
)

catkin_package()

include_directories(${catkin_INCLUDE_DIRS})
