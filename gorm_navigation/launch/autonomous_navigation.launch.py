from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    """
    Launch file for GORM autonomous navigation with RL.
    
    This launches:
    1. Camera system (ZED cameras)
    2. RL navigation node
    3. Any required transforms
    """
    
    # Declare launch arguments
    enable_triton_arg = DeclareLaunchArgument(
        'enable_triton',
        default_value='true',
        description='Enable Triton inference for RL navigation'
    )
    
    triton_server_url_arg = DeclareLaunchArgument(
        'triton_server_url',
        default_value='localhost:8000',
        description='URL of the Triton Inference Server'
    )
    
    # Include camera launch
    cameras_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('gorm_sensors'), '/launch/cameras.launch.py'
        ])
    )
    
    # Include RL navigation launch
    rl_navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('gorm_navigation'), '/launch/rl_navigation.launch.py'
        ]),
        launch_arguments={
            'enable_triton': LaunchConfiguration('enable_triton'),
            'triton_server_url': LaunchConfiguration('triton_server_url'),
        }.items()
    )
    
    # Goal pose publisher node (for testing)
    goal_publisher_node = Node(
        package='gorm_navigation',
        executable='goal_publisher_node',
        name='goal_publisher',
        output='screen',
        parameters=[{
            'goal_x': 5.0,
            'goal_y': 0.0,
            'goal_z': 0.0,
        }]
    )
    
    return LaunchDescription([
        enable_triton_arg,
        triton_server_url_arg,
        cameras_launch,
        rl_navigation_launch,
        # goal_publisher_node,  # Uncomment for testing
    ])
