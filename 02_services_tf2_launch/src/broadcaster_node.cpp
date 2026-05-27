/**
 * @file broadcaster_node.cpp
 * @brief EU_02 - Robot Operating System II
 *        Task 1: TF2 Transform Broadcaster
 *
 * Theory:
 *   TF2 (Transform library 2) manages a tree of coordinate frames over time.
 *   A tf2_ros::TransformBroadcaster publishes geometry_msgs/TransformStamped
 *   messages on the /tf topic. These describe how one coordinate frame
 *   relates to another (position + rotation as quaternion).
 *
 *   Homogeneous 4×4 transformation matrix T = [R | p; 0 0 0 1]
 *     R = 3×3 rotation matrix
 *     p = 3×1 translation vector
 *
 *   Quaternion from roll/pitch/yaw:  tf2::Quaternion q; q.setRPY(R, P, Y);
 *
 * Task 1 (EU_02 PDF Page 15):
 *   Publish two transforms every 100 ms:
 *     world → frame1  :  XYZ = (1, 1, 0),  RPY = (0, 0, 0)
 *     frame1 → frame2 :  XYZ = (0, 0, 1.5), RPY = (0, 0, z_angle)
 *       where z_angle increases by 10° every 100 ms (continuous rotation)
 */

#include <chrono>
#include <cmath>
#include <functional>
#include <memory>
#include <string>

#include "geometry_msgs/msg/transform_stamped.hpp"
#include "rclcpp/rclcpp.hpp"
#include "tf2/LinearMath/Quaternion.h"
#include "tf2_ros/transform_broadcaster.h"

using namespace std::chrono_literals;

// ─────────────────────────────────────────────────────────────────────────────
// SimpleTfBroadcaster
//   Publishes:
//     world  → frame1  (static offset: 1,1,0  no rotation)
//     frame1 → frame2  (0,0,1.5 above frame1 + rotating around Z)
// ─────────────────────────────────────────────────────────────────────────────
class SimpleTfBroadcaster : public rclcpp::Node
{
public:
  SimpleTfBroadcaster()
  : Node("my_tf_broadcaster"), angle_z_deg_(0.0)
  {
    // Create two broadcasters (can share one; two used for clarity)
    tf_broadcaster1_ = std::make_unique<tf2_ros::TransformBroadcaster>(*this);
    tf_broadcaster2_ = std::make_unique<tf2_ros::TransformBroadcaster>(*this);

    // Timer: 100 ms → 10 Hz  (~10° rotation per tick)
    timer_ = this->create_wall_timer(
      100ms,
      std::bind(&SimpleTfBroadcaster::timer_callback, this));

    RCLCPP_INFO(this->get_logger(),
      "TF Broadcaster started. Publishing world→frame1 and frame1→frame2.");
  }

private:
  void timer_callback()
  {
    auto now = this->get_clock()->now();
    tf2::Quaternion q;

    // ── Transform 1: world → frame1 ─────────────────────────────────────────
    // XYZ = (1, 1, 0),  RPY = (0, 0, 0)
    geometry_msgs::msg::TransformStamped t1;
    t1.header.stamp    = now;
    t1.header.frame_id = "world";
    t1.child_frame_id  = "frame1";
    t1.transform.translation.x = 1.0;
    t1.transform.translation.y = 1.0;
    t1.transform.translation.z = 0.0;
    q.setRPY(0.0, 0.0, 0.0);
    t1.transform.rotation.x = q.x();
    t1.transform.rotation.y = q.y();
    t1.transform.rotation.z = q.z();
    t1.transform.rotation.w = q.w();
    tf_broadcaster1_->sendTransform(t1);

    // ── Transform 2: frame1 → frame2 ────────────────────────────────────────
    // XYZ = (0, 0, 1.5),  RPY = (0, 0, angle_z) with +10°/100 ms
    double angle_z_rad = angle_z_deg_ * M_PI / 180.0;
    geometry_msgs::msg::TransformStamped t2;
    t2.header.stamp    = now;
    t2.header.frame_id = "frame1";
    t2.child_frame_id  = "frame2";
    t2.transform.translation.x = 0.0;
    t2.transform.translation.y = 0.0;
    t2.transform.translation.z = 1.5;
    q.setRPY(0.0, 0.0, angle_z_rad);
    t2.transform.rotation.x = q.x();
    t2.transform.rotation.y = q.y();
    t2.transform.rotation.z = q.z();
    t2.transform.rotation.w = q.w();
    tf_broadcaster2_->sendTransform(t2);

    RCLCPP_INFO_THROTTLE(this->get_logger(), *this->get_clock(), 1000,
      "Broadcasting TF: frame2 Z-rotation = %.1f deg", angle_z_deg_);

    // Increment rotation by 10° each 100 ms
    angle_z_deg_ += 10.0;
    if (angle_z_deg_ >= 360.0) {
      angle_z_deg_ -= 360.0;
    }
  }

  // ── Members ───────────────────────────────────────────────────────────────
  rclcpp::TimerBase::SharedPtr timer_;
  std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster1_;
  std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster2_;
  double angle_z_deg_;
};

// ─────────────────────────────────────────────────────────────────────────────
// main
// ─────────────────────────────────────────────────────────────────────────────
int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SimpleTfBroadcaster>());
  rclcpp::shutdown();
  return 0;
}
