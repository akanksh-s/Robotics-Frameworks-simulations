"""
EU_06 – Navigation of Mobile Robots with ROS2
Navigation2 (Nav2) Launch File

Theory:
  Nav2 is the ROS2 navigation stack. It provides:

  1. costmap_2d: Creates an occupancy grid (cost map) from the global map +
     sensor data. Each cell has a cost: FREE (0), INFLATED, LETHAL (254).
     The planner uses costs to avoid obstacles.

  2. NavFn/SmacPlanner (global planner): Finds a path from current position
     to goal using A* or Dijkstra on the costmap.

  3. DWBLocalPlanner / MPPI (local planner): Generates velocity commands
     to follow the global path while avoiding dynamic obstacles.

  4. BT Navigator: Orchestrates the whole pipeline using a Behavior Tree.

  5. AMCL (Adaptive Monte Carlo Localization): Particle filter that
     localizes the robot in a pre-built map.

  Full Nav2 pipeline:
    Goal Pose → BT Navigator → Global Planner → Local Planner → /cmd_vel

  Command to run:
    ros2 launch rof_ex6 navigation_launch.py use_sim_time:=true
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, GroupAction,
                             IncludeLaunchDescription)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node, PushRosNamespace


def generate_launch_description():
    # ── Config Paths ──────────────────────────────────────────────────────────
    bringup_dir = get_package_share_directory('nav2_bringup')
    nav_dir     = get_package_share_directory('rof_ex6')

    # ── Launch Arguments ──────────────────────────────────────────────────────
    use_sim_time       = LaunchConfiguration('use_sim_time',       default='true')
    params_file        = LaunchConfiguration('params_file',
                            default=os.path.join(nav_dir, 'config', 'navigation_params.yaml'))
    use_composition    = LaunchConfiguration('use_composition',    default='False')
    use_respawn        = LaunchConfiguration('use_respawn',        default='False')
    log_level          = LaunchConfiguration('log_level',          default='info')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time', default_value='true',
        description='Use simulation clock')

    declare_params_file_cmd = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(nav_dir, 'config', 'navigation_params.yaml'),
        description='Path to Nav2 parameters YAML')

    # ── Nav2 Stack (loaded as group action for optional composition) ──────────
    load_nodes = GroupAction(
        actions=[
            # ── Global Costmap + Planner ──────────────────────────────────────
            Node(
                package='nav2_planner',
                executable='planner_server',
                name='planner_server',
                output='screen',
                parameters=[params_file, {'use_sim_time': use_sim_time}]),

            # ── Local Costmap + Controller ────────────────────────────────────
            Node(
                package='nav2_controller',
                executable='controller_server',
                name='controller_server',
                output='screen',
                parameters=[params_file, {'use_sim_time': use_sim_time}]),

            # ── Behavior Tree Navigator ───────────────────────────────────────
            Node(
                package='nav2_bt_navigator',
                executable='bt_navigator',
                name='bt_navigator',
                output='screen',
                parameters=[params_file, {'use_sim_time': use_sim_time}]),

            # ── Recovery Behaviors ────────────────────────────────────────────
            Node(
                package='nav2_behaviors',
                executable='behavior_server',
                name='behavior_server',
                parameters=[params_file, {'use_sim_time': use_sim_time}],
                output='screen'),

            # ── Lifecycle Manager: manages startup/shutdown of Nav2 nodes ─────
            Node(
                package='nav2_lifecycle_manager',
                executable='lifecycle_manager',
                name='lifecycle_manager_navigation',
                output='screen',
                parameters=[
                    {'use_sim_time': use_sim_time},
                    {'autostart': True},
                    {'node_names': [
                        'planner_server',
                        'controller_server',
                        'bt_navigator',
                        'behavior_server',
                    ]}
                ]),
        ]
    )

    return LaunchDescription([
        declare_use_sim_time_cmd,
        declare_params_file_cmd,
        load_nodes,
    ])
