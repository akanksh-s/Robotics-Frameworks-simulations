#include "jetbot_gazebo/simple_robot_control.h"

using namespace std::chrono_literals;

void SimpleRobotControl::laser_front_callback(
    const sensor_msgs::msg::Range::SharedPtr msg) {

  // If the sensor reading is within the valid measurement range, print the
  // value
  if (msg->range > 0.1f and msg->range < 10.0f) {

    auto &clk = *this->get_clock();
    RCLCPP_INFO_THROTTLE(this->get_logger(), clk, 1000,
                         "Lidar distance front: %.2f", msg->range);
  }
}

void SimpleRobotControl::setpoint_callback() {

  std::string fromFrameRel = "tag36h11:0";
  std::string toFrameRel = "map";

  // Look up for the transformation
  try {
    current_pose_ = tf_buffer_->lookupTransform(toFrameRel, fromFrameRel,
                                                tf2::TimePointZero);
    // If the tag was located for the first time, store the position as initial
    // pose
    if (!tag_init_) {
      inital_pose_ = current_pose_;
      tag_init_ = true;
    }
    // Print the current position to the Info stream
    RCLCPP_INFO(
        this->get_logger(),
        "Current robot position in camera frame --- x: %.2f --- y: %.2f",
        current_pose_.transform.translation.x,
        current_pose_.transform.translation.y);

  } catch (const tf2::TransformException &ex) {
    RCLCPP_INFO(this->get_logger(), "Could not transform %s to %s: %s",
                toFrameRel.c_str(), fromFrameRel.c_str(), ex.what());
  }

  // Reset the velocity message
  geometry_msgs::msg::Twist vel_msg;

  // While the travelled distance in x-direction is less than 1 m, drive forward
  if (abs(inital_pose_.transform.translation.x -
          current_pose_.transform.translation.x) < 1.0) {
    vel_msg.linear.x = 1.0;
  } else { // else, stop the robot
    vel_msg.linear.x = 0.0;
    RCLCPP_INFO(this->get_logger(),
                "Robot stopped. Travelled more than one meter.");
  }

  // publish the setpoint to the defined topic
  publisher_->publish(vel_msg);
}

SimpleRobotControl::SimpleRobotControl()
    : Node("simple_robot_control"), count_(0) {

  tf_buffer_ = std::make_unique<tf2_ros::Buffer>(this->get_clock());
  tf_listener_ = std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);

  publisher_ =
      this->create_publisher<geometry_msgs::msg::Twist>("jetbot/cmd_vel", 10);

  timer_ = this->create_wall_timer(
      500ms, std::bind(&SimpleRobotControl::setpoint_callback, this));

  distance_front_sub_ = this->create_subscription<sensor_msgs::msg::Range>(
      "jetbot/laser_front", 1,
      std::bind(&SimpleRobotControl::laser_front_callback, this,
                std::placeholders::_1));
}

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SimpleRobotControl>());
  rclcpp::shutdown();
  return 0;
}
