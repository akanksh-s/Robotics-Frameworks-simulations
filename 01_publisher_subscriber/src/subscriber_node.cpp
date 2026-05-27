/**
 * @file subscriber_node.cpp
 * @brief EU_01 - Robot Operating System I
 *        Task 1: Listener Node
 *
 * Theory:
 *   A ROS2 subscriber listens to a topic and invokes a callback whenever
 *   a new message arrives.
 *   - create_subscription<MsgType>(topic, queue_size, callback) registers
 *     the subscriber.
 *   - The callback receives a shared pointer to the message.
 *   - RCLCPP_INFO() logs information to the ROS2 console and /rosout.
 *   - rclcpp::spin() keeps the node alive, processing incoming messages.
 *
 * Task:
 *   Subscribe to "first_test_topic" (std_msgs/Int64) and print every
 *   received value using RCLCPP_INFO().
 *   Node name: "listener"
 */

#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int64.hpp"

// ─────────────────────────────────────────────────────────────────────────────
// Listener: subscribes to "first_test_topic" and logs received values
// ─────────────────────────────────────────────────────────────────────────────
class Listener : public rclcpp::Node
{
public:
  Listener()
  : Node("listener")
  {
    // Subscribe with queue depth 10; bind member callback
    subscription_ = this->create_subscription<std_msgs::msg::Int64>(
      "first_test_topic",
      10,
      std::bind(&Listener::topic_callback, this, std::placeholders::_1));

    RCLCPP_INFO(this->get_logger(), "Listener node started. Waiting for messages on 'first_test_topic'.");
  }

private:
  // ── Callback ──────────────────────────────────────────────────────────────
  void topic_callback(const std_msgs::msg::Int64::SharedPtr msg) const
  {
    // Print the received integer value
    RCLCPP_INFO(this->get_logger(), "Received: %ld", msg->data);
  }

  // ── Members ───────────────────────────────────────────────────────────────
  rclcpp::Subscription<std_msgs::msg::Int64>::SharedPtr subscription_;
};

// ─────────────────────────────────────────────────────────────────────────────
// main
// ─────────────────────────────────────────────────────────────────────────────
int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Listener>());
  rclcpp::shutdown();
  return 0;
}
