# MP_for_AV
This repo consist of code for real time motion planning for Autonomous Vehicle with simulation in Carla Engine. 

#start planner

ros2 service call /global_plan_srv vd_msgs/srv/PlannerSrv ""{x: 5.0, y: 10.0}""
