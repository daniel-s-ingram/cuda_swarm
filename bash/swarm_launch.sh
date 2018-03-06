#!/usr/bin/env bash

for f in ../launch/swarms/*.launch
do
	roslaunch $f
done