/**
 * @file client_node.cpp
 * @brief EU_02 - Robot Operating System II
 *        ROS2 Service Client — "add_two_ints"
 *
 * Theory:
 *   The SERVICE CLIENT sends a typed request to a named service and waits
 *   for the server's response. Key steps:
 *     1. Create the client:  node->create_client<SrvType>("service_name")
 *     2. Wait for server:    client->wait_for_service(timeout)
 *     3. Fill request:       auto req = make_shared<SrvType::Request>()
 *     4. Send asynchronously: auto future = client->async_send_request(req)
 *     5. Wait for result:    spin_until_future_complete(node, future)
 *     6. Read result:        future.get()->sum
 *
 * Usage:
 *   ros2 run my_cliserv_package client_node <A> <B>
 *   Example: ros2 run my_cliserv_package client_node 5 7  → Sum: 12
 */

#include <chrono>
#include <cstdlib>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "my_cliserv_package_interfaces/srv/add.hpp"

using namespace std::chrono_literals;

// ─────────────────────────────────────────────────────────────────────────────
// main
// ─────────────────────────────────────────────────────────────────────────────
int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);

  // Require exactly two command-line arguments: A and B
  if (argc != 3) {
    RCLCPP_ERROR(rclcpp::get_logger("add_client"),
      "Usage: client_node <A> <B>  (e.g. client_node 5 7)");
    return 1;
  }

  auto node   = rclcpp::Node::make_shared("add_two_ints_client");
  auto client = node->create_client<my_cliserv_package_interfaces::srv::Add>("add_two_ints");

  // ── Wait until the server is available ────────────────────────────────────
  while (!client->wait_for_service(1s)) {
    if (!rclcpp::ok()) {
      RCLCPP_ERROR(rclcpp::get_logger("add_client"),
        "Interrupted while waiting for the server. Exiting.");
      return 0;
    }
    RCLCPP_INFO(rclcpp::get_logger("add_client"), "Server not yet available, waiting…");
  }

  // ── Build and send the request ────────────────────────────────────────────
  auto request = std::make_shared<my_cliserv_package_interfaces::srv::Add::Request>();
  request->a = std::atoll(argv[1]);
  request->b = std::atoll(argv[2]);

  auto result_future = client->async_send_request(request);

  // ── Wait for response ─────────────────────────────────────────────────────
  if (rclcpp::spin_until_future_complete(node, result_future) ==
    rclcpp::FutureReturnCode::SUCCESS)
  {
    RCLCPP_INFO(rclcpp::get_logger("add_client"),
      "%ld + %ld = %ld", request->a, request->b,
      result_future.get()->sum);
  } else {
    RCLCPP_ERROR(rclcpp::get_logger("add_client"),
      "Failed to call service 'add_two_ints'.");
  }

  rclcpp::shutdown();
  return 0;
}
