#!/usr/bin/env bash

roslaunch cuda_swarm swarm0-24.launch &

sleep 10

roslaunch cuda_swarm swarm25-49.launch &

sleep 10

roslaunch cuda_swarm swarm50-74.launch &

sleep 10

roslaunch cuda_swarm swarm75-99.launch &