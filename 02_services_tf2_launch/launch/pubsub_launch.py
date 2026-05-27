"""
EU_02 - Launch file for the pubsub package

Theory:
  A ROS2 launch file is a Python script that starts multiple nodes at once.
  It uses the `launch` and `launch_ros` packages:
    - LaunchDescription: top-level container for launch actions
    - Node: action that starts a single ROS2 node

  Command to run:
    ros2 launch my_pubsub_package pubsub_launch.py

  This launch file starts the publisher (talker) and subscriber (listener)
  nodes from the my_pubsub_package simultaneously in one terminal.
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # Start the publisher (Talker)
        Node(
            package='my_pubsub_package',
            namespace='',
            executable='publisher_node',
            name='talker',            # remapped node name
            output='screen',
        ),
        # Start the subscriber (Listener)
        Node(
            package='my_pubsub_package',
            namespace='',
            executable='subscriber_node',
            name='listener',          # remapped node name
            output='screen',
        ),
    ])
