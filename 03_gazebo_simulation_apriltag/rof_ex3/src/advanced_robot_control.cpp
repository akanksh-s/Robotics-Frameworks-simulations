// Copyright 2016 Open Source Robotics Foundation, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "jetbot_gazebo/advanced_robot_control.h"

using namespace std::chrono_literals;

void AdvancedRobotControl::odom_callback(
    const nav_msgs::msg::Odometry::SharedPtr msg) {
  // Auslesen der aktuellen Pose und Konvertierung des Quaternions in
  // Euler-Winkel
  current_x_pos_ = msg->pose.pose.position.x;
  current_y_pos_ = msg->pose.pose.position.y;

  tf2::Quaternion q(msg->pose.pose.orientation.x, msg->pose.pose.orientation.y,
                    msg->pose.pose.orientation.z, msg->pose.pose.orientation.w);

  tf2::Matrix3x3 m(q);
  double roll, pitch, yaw;
  m.getRPY(roll, pitch, yaw);

  current_theta_ = yaw;
}

void AdvancedRobotControl::laser_front_callback(
    const sensor_msgs::msg::Range::SharedPtr msg) {

  // Wenn aktueller Messwert im Messbereich des Sensors liegt,abspeichern in
  // Variable
  if (msg->range > 0.1f and msg->range < 10.0f) {
    current_distance_front_ = msg->range;
  }
}

void AdvancedRobotControl::laser_side_callback(
    const sensor_msgs::msg::Range::SharedPtr msg) {

  // Wenn aktueller Messwert im Messbereich des Sensors liegt, abspeichern in
  // Variable
  if (msg->range > 0.1f and msg->range < 10.0f) {
    current_distance_side_ = msg->range;
  }

  // Wenn der Messwert über 10m bzw.ausßerhalb des Messbereichs liegt,
  // wurde kein Objekt vor dem Sensor erkannt
  // Wird als Indikator genutzt, dass das Ende einer Kiste erreicht wurde
  else if (msg->range >= 10.0f) {
    space_trigger_ = true;
    current_distance_side_ = 10.0f;
  }

  // Wenn der Messwert einen Wert von 1.5m unterschreitet,wurde ein Objekt
  // vor dem Sensor erkannt Wird als Indikator genutzt, dass der Anfang
  // einer Kiste erreicht wurde
  if (space_trigger_ == true and current_distance_side_ < 1.5f) {
    object_trigger_ = true;
    space_trigger_ = false;
    object_start_pos_ = current_y_pos_;
    RCLCPP_INFO(this->get_logger(), "--- object position ---");
    RCLCPP_INFO(this->get_logger(), "--- x: %f",
                static_cast<double>(current_x_pos_ + current_distance_side_));
    RCLCPP_INFO(this->get_logger(), "--- y: %f",
                static_cast<double>(current_y_pos_));
  }
  if (object_trigger_ == true and space_trigger_ == true) {
    object_trigger_ = false;
    space_trigger_ = false;
    RCLCPP_INFO(this->get_logger(), "width: %f",
                static_cast<double>(abs(current_y_pos_ - object_start_pos_)));
  }
}

void AdvancedRobotControl::setpoint_callback() {
  // Zurücksetzen der Geschwindigkeiten
  // Führt zu einem Abbremsen des Roboters, wenn der Wert nicht unten wieder
  // überschrieben wird
  geometry_msgs::msg::Twist vel_msg;

  // Solange der Mindestabstand in Fahrrichtung nicht unterschritten wurde,
  // Fahrt nach vorne mit 0,5 m/s
  if (reached_first_position_ == false && current_distance_front_ >= 0.85f) {
    vel_msg.linear.x = 1.0;
  } else if (reached_first_position_ == false &&
             current_distance_front_ < 0.85f) {
    reached_first_position_ = true;
    RCLCPP_INFO(this->get_logger(), "Reached first position");
  }

  // Wenn die erste Position erreicht wurde und der Roboter noch nicht gedreht
  // ist, wird eine Drehgeschwindigkeit vorgegeben
  if (reached_first_position_ == true && rotated_ == false &&
      current_theta_ > -M_PI / 2) {
    double angle_difference = -M_PI / 2 - current_theta_;
    if (angle_difference < 0) {
      vel_msg.angular.z = 1.25 * angle_difference - 0.04;
    }
  } else if (reached_first_position_ == true && current_theta_ <= -M_PI / 2) {
    rotated_ = true;
  }

  // Nach der Drehung wird eine Lineargeschwindigkeit vorgegeben, um zum
  // Zielpunkt zu fahren Zusätzlich werden kleine Drehungen ausgeglichen, um
  // parallel zu den Kisten zu fahren
  if (reached_first_position_ == true && rotated_ == true &&
      current_distance_front_ >= 0.85f) {
    double angle_difference = -M_PI / 2 - current_theta_;
    vel_msg.angular.z = 1.0 * angle_difference;
    vel_msg.linear.x = 1.0;
  }

  // An der Zielposition werden die Geschwindigkeiten auf Null gesetzt
  else if (reached_first_position_ == true && rotated_ == true &&
           current_distance_front_ < 0.85f) {
    RCLCPP_INFO(this->get_logger(), "Destination reached");
    vel_msg.linear.x = 0.0;
    vel_msg.angular.z = 0.0;
    reached_final_position_ = true;
  }

  publisher_->publish(vel_msg);
}

AdvancedRobotControl::AdvancedRobotControl()
    : Node("navigation_node_solution"), count_(0) {

  publisher_ =
      this->create_publisher<geometry_msgs::msg::Twist>("jetbot/cmd_vel", 10);

  odom_sub_ = this->create_subscription<nav_msgs::msg::Odometry>(
      "jetbot/odom", 1,
      std::bind(&AdvancedRobotControl::odom_callback, this,
                std::placeholders::_1));

  distance_side_sub_ = this->create_subscription<sensor_msgs::msg::Range>(
      "jetbot/laser_side", 1,
      std::bind(&AdvancedRobotControl::laser_side_callback, this,
                std::placeholders::_1));

  distance_front_sub_ = this->create_subscription<sensor_msgs::msg::Range>(
      "jetbot/laser_front", 1,
      std::bind(&AdvancedRobotControl::laser_front_callback, this,
                std::placeholders::_1));

  timer_ = this->create_wall_timer(
      100ms, std::bind(&AdvancedRobotControl::setpoint_callback, this));
}

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<AdvancedRobotControl>());
  rclcpp::shutdown();
  return 0;
}
