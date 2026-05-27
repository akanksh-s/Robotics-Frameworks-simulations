#!/usr/bin/env python3
"""
EU_10-12 – Practical Task: Object Perception via YOLO ROS Wrapper
Task 3: Percept Objects using YOLO + iRobot Camera System

Theory:
  The iRobot Create 3 has a USB camera mounted at the front. On the Jetson
  Orin Nano board, a pre-installed yolo_ros package wraps YOLOv8 and
  publishes detection results as ROS2 topics.

  This script demonstrates how to:
    1. Subscribe to the YOLO detection topics on your Ubuntu system
    2. Visualise the detections overlaid on the camera image
    3. Identify which objects are suitable for the logistics task

  IMPORTANT:
    The yolo_ros package runs on the ROBOT (Jetson Orin Nano), NOT on your PC.
    You only need to SUBSCRIBE to its topics.
    Clone yolo_msgs from:
      https://git.faps.uni-erlangen.de/heengelhardt/yolo_msgs
    and build it to get the message types.

  Key topics published by yolo_ros on the iRobot:
    /yolo/detections         (yolo_msgs/msg/DetectionArray)
    /yolo/detection_image    (sensor_msgs/msg/Image)

  ROS2 Domain setup:
    Make sure your PC and the iRobot have the SAME ROS_DOMAIN_ID in .bashrc:
      export ROS_DOMAIN_ID=<id_provided_in_lab>

Usage:
  python3 yolo_subscriber.py
  → Subscribes to detections, displays class name + confidence for each frame
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


# ─────────────────────────────────────────────────────────────────────────────
# YoloSubscriber: subscribes to the raw camera image and detection image
# ─────────────────────────────────────────────────────────────────────────────
class YoloSubscriber(Node):
    """
    Subscribes to camera image and YOLO detection image topics from the iRobot.

    Topics:
      /camera/image_raw       → raw camera feed from iRobot USB camera
      /yolo/detection_image   → image with bounding boxes drawn by yolo_ros
    """

    def __init__(self):
        super().__init__('yolo_subscriber')
        self.bridge = CvBridge()

        # ── Subscribe to raw camera image ─────────────────────────────────────
        self.raw_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.raw_image_callback,
            10)

        # ── Subscribe to YOLO annotated image (bboxes already drawn) ──────────
        self.det_sub = self.create_subscription(
            Image,
            '/yolo/detection_image',
            self.detection_image_callback,
            10)

        self.get_logger().info('YoloSubscriber started.')
        self.get_logger().info('Waiting for topics /camera/image_raw and /yolo/detection_image ...')
        self.get_logger().info('Make sure ROS_DOMAIN_ID matches the iRobot!')

    def raw_image_callback(self, msg: Image):
        """Display the raw camera frame."""
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        cv2.imshow('iRobot Camera (Raw)', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            rclpy.shutdown()

    def detection_image_callback(self, msg: Image):
        """Display the YOLO annotated frame (bounding boxes + labels)."""
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        cv2.imshow('YOLO Detections (iRobot)', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            rclpy.shutdown()


# ─────────────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────────────
def main(args=None):
    rclpy.init(args=args)
    node = YoloSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
