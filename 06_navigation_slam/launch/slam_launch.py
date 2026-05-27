"""
EU_06 – Navigation of Mobile Robots with ROS2
SLAM Toolbox Launch File

Theory:
  SLAM = Simultaneous Localization and Mapping
  The robot builds a map while simultaneously estimating its own position.

  slam_toolbox (Steve Macenski):
  - Uses laser scan data (/scan) to correlate consecutive scans -> odometry
  - Builds an occupancy grid map incrementally
  - In 'mapping' mode: creates new map
  - In 'localization' mode: localizes within a pre-saved map

  Key ROS2 concepts:
  - The slam_toolbox node subscribes to /scan (sensor_msgs/LaserScan)
  - It publishes /map (nav_msgs/OccupancyGrid) and the map→odom transform
  - Parameters are loaded from a .yaml config file

  TF chain for navigation:
    map → odom → base_footprint → sensors

  Command to build and run:
    colcon build --symlink-install --packages-select rof_ex6
    source install/setup.bash
    ros2 launch rof_ex6 slam_launch.py

"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # ── Parameters ────────────────────────────────────────────────────────────
    use_sim_time = LaunchConfiguration('use_sim_time')
    slam_params_file = LaunchConfiguration('slam_params_file')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true')

    declare_slam_params_file_cmd = DeclareLaunchArgument(
        'slam_params_file',
        default_value=os.path.join(
            get_package_share_directory('rof_ex6'),
            'config', 'slam_params.yaml'),
        description='Full path to the slam_toolbox parameter file')

    # ── SLAM Toolbox Node ─────────────────────────────────────────────────────
    # async_slam_toolbox_node: performs SLAM asynchronously (does not block)
    start_async_slam_toolbox_node = Node(
        parameters=[
            slam_params_file,
            {'use_sim_time': use_sim_time}
        ],
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen')

    return LaunchDescription([
        declare_use_sim_time_cmd,
        declare_slam_params_file_cmd,
        start_async_slam_toolbox_node,
    ])
