#ifndef ROBOT_CONTROL_H
#define ROBOT_CONTROL_H

#include <chrono>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include <math.h>

#include "geometry_msgs/msg/twist.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "sensor_msgs/msg/range.hpp"

#include "tf2/exceptions.h"
#include <tf2/transform_datatypes.h>
#include <tf2_ros/buffer.h>
#include <tf2_ros/transform_listener.h>

using namespace std::chrono_literals;

class SimpleRobotControl : public rclcpp::Node {
private:
  /// current x-position of the robot
  geometry_msgs::msg::TransformStamped inital_pose_;

  /// current y-position of the robot
  geometry_msgs::msg::TransformStamped current_pose_;

  /// indicate if the tag has already been detected once
  bool tag_init_ = false;

  /// Timer object to trigger the cyclic publishing
  rclcpp::TimerBase::SharedPtr timer_;

  /// Publisher for the velocity commands
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;

  /// Transform listener object
  std::shared_ptr<tf2_ros::TransformListener> tf_listener_{nullptr};

  /// Transform buffer object
  std::unique_ptr<tf2_ros::Buffer> tf_buffer_;

  /// Subscriber for the message provided by the front laser sensor
  rclcpp::Subscription<sensor_msgs::msg::Range>::SharedPtr distance_front_sub_;

  size_t count_;

  void setpoint_callback();

  void laser_front_callback(const sensor_msgs::msg::Range::SharedPtr msg);

public:
  SimpleRobotControl();
};

#endif // ROBOT_CONTROL_H
