# MP_for_AV
This repo consist of code for real time motion planning for Autonomous Vehicle with simulation in Carla Engine. 

#start carla with ros arg from the dir where carla is installed
source ./CarlaUnreal.sh --ROS2

#go to the MP_for_AV dir, start carla client node with pygame, vehicle is spawned here
cd carla_client 
python3 CBF_test.py

#start the planer and control, rosbag nodes
ros2 launch vd_global_planner sim_launch.py

#start planning by sending request with goal node
ros2 service call /global_plan_srv vd_msgs/srv/PlannerSrv "{x: 19.39, y: 130.46}"

#build - MP_for_AV
colcon build
source install/setup.bash

