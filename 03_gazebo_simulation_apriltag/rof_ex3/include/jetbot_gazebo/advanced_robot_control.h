#ifndef ROBOT_CONTROL_H
#define ROBOT_CONTROL_H

#include <chrono>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include <math.h>

#include "geometry_msgs/msg/twist.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "sensor_msgs/msg/range.hpp"

#include <tf2/buffer_core.h>
#include <tf2/transform_datatypes.h>
#include <tf2_ros/transform_listener.h>

#endif // ROBOT_CONTROL_H

using namespace std::chrono_literals;

class AdvancedRobotControl : public rclcpp::Node {
private:
  /// current x-position of the robot
  double current_x_pos_ = 0.0;

  /// current y-position of the robot
  double current_y_pos_ = 0.0;

  /// current orientation of the robot
  double current_theta_ = 0.0;

  /// aktueller Abstand des vorderen Lidar in Meter
  float current_distance_front_ = 100.0;

  /// aktueller Abstand des vorderen Lidar in Meter
  float current_distance_side_ = 100.0;

  /// Indikator, dass der Drehpunkt erreicht wurde
  bool reached_first_position_ = false;

  /// Indikator, dass die Zielposition erreicht wurde
  bool reached_final_position_ = false;

  /// Indikator, dass sich der Roboter bereits gedreht hat
  bool rotated_ = false;

  bool object_trigger_ = false;
  bool space_trigger_ = false;
  double object_start_pos_ = 0.0;

  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
  size_t count_;

  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr odom_sub_;

  rclcpp::Subscription<sensor_msgs::msg::Range>::SharedPtr distance_side_sub_;

  rclcpp::Subscription<sensor_msgs::msg::Range>::SharedPtr distance_front_sub_;

  void timer_callback();

  void odom_callback(const nav_msgs::msg::Odometry::SharedPtr msg);

  void laser_side_callback(const sensor_msgs::msg::Range::SharedPtr msg);

  void laser_front_callback(const sensor_msgs::msg::Range::SharedPtr msg);

  void setpoint_callback();

public:
  AdvancedRobotControl();
};
