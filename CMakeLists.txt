cmake_minimum_required(VERSION 2.8.3)
project(cuda_swarm)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  gazebo_msgs
)

find_package(CUDA REQUIRED)

catkin_package()

include_directories(${catkin_INCLUDE_DIRS})

cuda_add_executable(move_swarm src/move_swarm.cu)
target_link_libraries(move_swarm ${catkin_LIBRARIES})