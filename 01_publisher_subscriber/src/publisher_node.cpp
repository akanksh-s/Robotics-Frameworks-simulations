/**
 * @file publisher_node.cpp
 * @brief EU_01 - Robot Operating System I
 *        Task 1: Talker Node
 *
 * Theory:
 *   A ROS2 publisher node sends typed messages on a named topic.
 *   - rclcpp::Node is the base class for all ROS2 nodes.
 *   - create_publisher<MsgType>(topic, queue_size) creates a publisher.
 *   - A wall timer fires a callback at a fixed rate (here 20 Hz = 50 ms).
 *   - std_msgs::msg::Int64 carries a single 64-bit integer value.
 *
 * Task:
 *   Publish an Int64 message on "first_test_topic" at 20 Hz,
 *   counting 0 → 50 and wrapping back to 0 indefinitely.
 *   Node name: "talker"
 */

#include <chrono>
#include <functional>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int64.hpp"

using namespace std::chrono_literals;

// ─────────────────────────────────────────────────────────────────────────────
// Talker: publishes Int64 on "first_test_topic" at 20 Hz (0..50 cycle)
// ─────────────────────────────────────────────────────────────────────────────
class Talker : public rclcpp::Node
{
public:
  Talker()
  : Node("talker"), count_(0)
  {
    // Create publisher on topic "first_test_topic" with queue depth 10
    publisher_ = this->create_publisher<std_msgs::msg::Int64>("first_test_topic", 10);

    // Timer fires at 20 Hz (every 50 ms)
    timer_ = this->create_wall_timer(
      50ms,
      std::bind(&Talker::timer_callback, this));

    RCLCPP_INFO(this->get_logger(), "Talker node started. Publishing on 'first_test_topic' at 20 Hz.");
  }

private:
  // ── Callback ──────────────────────────────────────────────────────────────
  void timer_callback()
  {
    auto msg = std_msgs::msg::Int64();
    msg.data = count_;

    RCLCPP_INFO(this->get_logger(), "Publishing: %ld", msg.data);
    publisher_->publish(msg);

    // Increment counter; wrap around after 50
    count_ = (count_ >= 50) ? 0 : count_ + 1;
  }

  // ── Members ───────────────────────────────────────────────────────────────
  rclcpp::Publisher<std_msgs::msg::Int64>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  int64_t count_;
};

// ─────────────────────────────────────────────────────────────────────────────
// main
// ─────────────────────────────────────────────────────────────────────────────
int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Talker>());
  rclcpp::shutdown();
  return 0;
}
