cmake_minimum_required(VERSION 3.8)
project(my_cliserv_package)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# ── Dependencies ──────────────────────────────────────────────────────────────
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(my_cliserv_package_interfaces REQUIRED)

# ── Service Server ────────────────────────────────────────────────────────────
add_executable(server_node src/server_node.cpp)
ament_target_dependencies(server_node rclcpp my_cliserv_package_interfaces)

# ── Service Client ────────────────────────────────────────────────────────────
add_executable(client_node src/client_node.cpp)
ament_target_dependencies(client_node rclcpp my_cliserv_package_interfaces)

# ── TF2 Broadcaster ───────────────────────────────────────────────────────────
add_executable(broadcaster_node src/broadcaster_node.cpp)
ament_target_dependencies(broadcaster_node rclcpp geometry_msgs tf2 tf2_ros)

# ── Install ───────────────────────────────────────────────────────────────────
install(TARGETS
  server_node
  client_node
  broadcaster_node
  DESTINATION lib/${PROJECT_NAME})

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME})

ament_package()
