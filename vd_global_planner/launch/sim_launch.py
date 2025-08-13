import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Node 1: Start global planner
        Node(
            package='vd_global_planner',
            executable='vd_golbal_planner',
            name='vd_golbal_planner',
            output='screen',
            parameters=[{'use_sim_time': True}]
        ),

        #Node 2: Start MPC Controller
        Node(
            package='vd_local_planner',
            executable='vd_nmpc_node',
            name='vd_local_planner',
            output='screen',
            parameters=[{'use_sim_time': True}]
        ),

        # Node 3: Start ROS Bag Node
        Node(
            package='vd_data_saver',
            executable='data_saver_node',
            name='data_saver_node',
            output='screen',
            parameters=[{'use_sim_time': True}]
        ),

        # Node 4: Start PID velocity control node
        Node(
            package='vd_pid_controller',
            executable='pid_controller_node',
            name='pid_controller_node',
            output='screen',
            parameters=[{'use_sim_time': True}]
        )

    ])
