#!/usr/bin/env bash

#roslaunch cuda_swarm swarm0-24.launch
#roslaunch cuda_swarm swarm25-49.launch
#roslaunch cuda_swarm swarm50-74.launch
#roslaunch cuda_swarm swarm75-99.launch

for f in ../launch/swarms/*.launch
do
	roslaunch $f
done