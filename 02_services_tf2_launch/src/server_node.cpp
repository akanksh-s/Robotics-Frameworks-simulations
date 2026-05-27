/**
 * @file server_node.cpp
 * @brief EU_02 - Robot Operating System II
 *        ROS2 Service Server — "add_two_ints"
 *
 * Theory:
 *   Services in ROS2 implement the client–server (request/response) pattern.
 *   Unlike topics (fire-and-forget), a service call is SYNCHRONOUS:
 *   the client blocks until the server responds.
 *
 *   A service is defined by an interface (.srv file):
 *     # Request  (fields before ---)
 *     int64 a
 *     int64 b
 *     ---
 *     # Response (fields after  ---)
 *     int64 sum
 *
 *   Server side:
 *     node->create_service<SrvType>(name, callback);
 *   Client side:
 *     node->create_client<SrvType>(name);
 *     client->async_send_request(request);
 *
 * This file implements the SERVER that adds two integers and returns their sum.
 */

#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "my_cliserv_package_interfaces/srv/add.hpp"

// ─────────────────────────────────────────────────────────────────────────────
// Service callback: computes a + b = sum
// ─────────────────────────────────────────────────────────────────────────────
void add(
  const std::shared_ptr<my_cliserv_package_interfaces::srv::Add::Request> request,
  std::shared_ptr<my_cliserv_package_interfaces::srv::Add::Response>      response)
{
  response->sum = request->a + request->b;

  RCLCPP_INFO(rclcpp::get_logger("add_server"),
    "Incoming request — a: %ld  b: %ld", request->a, request->b);
  RCLCPP_INFO(rclcpp::get_logger("add_server"),
    "Sending response: sum = %ld", static_cast<long int>(response->sum));
}

// ─────────────────────────────────────────────────────────────────────────────
// main
// ─────────────────────────────────────────────────────────────────────────────
int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);

  auto node = rclcpp::Node::make_shared("add_two_ints_server");

  // Register the service on the name "add_two_ints"
  auto service = node->create_service<my_cliserv_package_interfaces::srv::Add>(
    "add_two_ints", &add);

  RCLCPP_INFO(rclcpp::get_logger("add_server"), "Ready to add two integers.");
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
