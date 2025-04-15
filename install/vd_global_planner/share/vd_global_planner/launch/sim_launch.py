import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.conditions import IfCondition

def generate_launch_description():

    return LaunchDescription([

        DeclareLaunchArgument(
            'VD_file',            
            default_value= "vd_param.yaml",
            description='Path to the payload parameters file'
        ),
    
        DeclareLaunchArgument(
                'controller_file',            
                default_value= "controller_param.yaml",
                description='Path to the payload parameters file'
            ),

        DeclareLaunchArgument(
                'planner_file',            
                default_value= "vd_param.yaml",
                description='Path to the payload parameters file'
            ),



        # Node 1: Start global planner
        Node(
            package='vd_global_planner',
            executable='vd_golbal_planner',
            name='vd_golbal_planner',
            output='screen',
            parameters=[{'use_sim_time': True}],
            
        ),

        #Node 2: Start MPC Controller
        Node(
            package='vd_local_planner',
            executable='vd_nmpc_node',
            name='vd_local_planner',
            output='screen',
            parameters=[{'use_sim_time': True}],
            
        ),

        # Node 3: Start ROS Bag Node
        Node(
            package='vd_data_saver',
            executable='data_saver_node',
            name='data_saver_node',
            output='screen',
            parameters=[{'use_sim_time': True}]
        )
    ])
