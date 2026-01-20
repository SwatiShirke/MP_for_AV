# MP_for_AV
This repo consist of code for real time motion planning for Autonomous Vehicle with simulation in Carla Engine. 


##start carla
cd carla_sim10/Carla-0.10.0-Linux-Shipping/
source CarlaUnreal.sh --ROS2

## start
cd Motion_Planning/MP_for_AV/src/MP_for_AV/carla_client/
python3 CBF_test.py



## start client 
cd Motion_Planning/MP_for_AV
source install/setup.bash


#start planner
ros2 service call /global_plan_srv vd_msgs/srv/PlannerSrv "{x: 19.39, y: 130.46, yaw: 0.0}"

ros2 service call /global_plan_srv vd_msgs/srv/PlannerSrv "{x: 57.57, y: -67.85, yaw: 0.60}"

ros2 service call /global_plan_srv vd_msgs/srv/PlannerSrv "{x: -60.57, y: 80, yaw: 0.90}"

longest dist
Point A: (-110.96, 59.69, 0.60)

Point B: (57.57, -67.85, 0.60)


Spawning Mini Cooper at: Location(x=-64.644844, y=24.471010, z=0.600000)