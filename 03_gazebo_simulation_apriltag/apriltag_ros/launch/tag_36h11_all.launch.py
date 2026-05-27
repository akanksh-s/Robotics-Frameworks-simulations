import launch
from launch_ros.actions import ComposableNodeContainer, Node
from launch_ros.descriptions import ComposableNode

# detect all 36h11 tags
cfg_36h11 = {
    "image_transport": "raw",
    "family": "36h11",
    "size": 0.175,
    "max_hamming": 0,
    "z_up": True
}

def generate_launch_description():

    tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments = ['-2.0', '3.0', '3.0', '3.14', '3.14', '0', 'map', 'ceiling_camera']
    )

    tf_node_2 = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments = ['0.0', '0.0', '-0.2', '0.0', '0.0', '0', 'tag36h11:0', 'chassis']
    )


    tag_node = ComposableNode(
        name='apriltag_36h11',
        namespace='apriltag',
        package='apriltag_ros', plugin='AprilTagNode',
        remappings=[
            # This maps the 'raw' images for simplicity of demonstration.
            # In practice, this will have to be the rectified 'rect' images.
            ("/apriltag/image_rect", "/ceiling_camera/image_raw"),
            ("/apriltag/camera_info", "/ceiling_camera/camera_info"),
        ],
        parameters=[cfg_36h11],
        extra_arguments=[{'use_intra_process_comms': True}],
    )


    container = ComposableNodeContainer(
        name='tag_container',
        namespace='apriltag',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=[tag_node],
        output='screen'
    )

    return launch.LaunchDescription([tf_node, tf_node_2, container])
