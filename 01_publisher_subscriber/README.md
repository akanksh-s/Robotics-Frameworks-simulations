# EU_01 – Robot Operating System I

> **Robotics Frameworks (RoF) · FAU Erlangen-Nürnberg · Winter Semester 2025/26**
> Lecturer: Dr.-Ing. Sebastian Reitelshöfer

---

## 📖 Theory Overview

### What is ROS 2?
ROS 2 (Robot Operating System 2) is a middleware framework for building robot software. It provides:
- **Nodes** — independent processes that perform computation
- **Topics** — named buses over which nodes exchange messages (publish/subscribe)
- **Services** — synchronous request/response communication
- **Actions** — asynchronous goal-based communication with feedback
- **Parameters** — runtime configuration for nodes

### Key Concepts Introduced in EU_01

| Concept | Description |
|---|---|
| **Workspace** (`ros2_ws/`) | Root folder containing all ROS 2 packages built from source |
| **Package** | Basic unit of ROS 2 software, containing nodes, launch files, and config |
| **`colcon build`** | Build tool that compiles all packages in the workspace |
| **Publisher** | Node component that sends messages on a topic |
| **Subscriber** | Node component that receives messages from a topic |
| **`std_msgs`** | Standard ROS 2 message package (String, Int64, Float32, …) |

### Publisher–Subscriber Pattern

```
  ┌─────────────┐       /first_test_topic        ┌──────────────┐
  │   Talker    │  ──── Int64 @ 20 Hz ─────────► │   Listener   │
  │ (publisher) │                                 │ (subscriber) │
  └─────────────┘                                 └──────────────┘
```

The **Talker** node:
- Counts from 0 to 50, then wraps back to 0
- Publishes an `std_msgs/msg/Int64` message on `first_test_topic` at **20 Hz** (every 50 ms)
- Uses a `create_wall_timer()` callback to drive publishing

The **Listener** node:
- Subscribes to `first_test_topic`
- Prints every received value with `RCLCPP_INFO()`

---

## 📁 File Structure

```
EU_01_ROS_I/
├── CMakeLists.txt          # Build configuration
├── package.xml             # Package metadata & dependencies
├── README.md               # This file
└── src/
    ├── publisher_node.cpp  # Talker: publishes Int64 at 20 Hz (0→50 cycle)
    └── subscriber_node.cpp # Listener: subscribes and logs received values
```

---

## 🔨 Build Instructions

```bash
# 1. Clone / Copy into your ROS 2 workspace source folder
cp -r EU_01_ROS_I ~/ros2_ws/src/my_pubsub_package

# 2. Build the package
cd ~/ros2_ws
colcon build --symlink-install --packages-select my_pubsub_package

# 3. Source the workspace
source install/setup.bash
```

---

## ▶️ Running the Nodes

Open **three terminals**, each sourced with the workspace:

**Terminal 1 — Listener (start first so it's ready):**
```bash
ros2 run my_pubsub_package subscriber_node
```

**Terminal 2 — Talker:**
```bash
ros2 run my_pubsub_package publisher_node
```

**Terminal 3 — Inspect the topic:**
```bash
# List all active topics
ros2 topic list

# Show topic info (type, publisher count, subscriber count)
ros2 topic info /first_test_topic

# Echo live messages
ros2 topic echo /first_test_topic

# Manually publish a message
ros2 topic pub /first_test_topic std_msgs/msg/Int64 "data: 42"
```

---

## 📊 Visualisation with rqt

```bash
# Open rqt plot to display the history of first_test_topic
rqt

# In rqt → Plugins → Visualization → Plot
# Add /first_test_topic/data to the chart
```

---

## 🐛 Debugging with VS Code
1. Build with debug info:
   ```bash
   colcon build --symlink-install --packages-select my_pubsub_package \
     --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo
   ```
2. Run the publisher node in Terminal 1.
3. In VS Code, open `~/ros2_ws` and attach the debugger to the running process via `launch.json` (type: `cppdbg`, request: `attach`).

---

## 📝 Task Summary (from EU_01 PDF – Page 17)

> **Task 1:** Create a Publisher node named **Talker** that publishes an `int64` message (from `std_msgs`) on the topic `first_test_topic` at **20 Hz**, counting up from 0 to 50 and repeating indefinitely. Write a Subscriber node named **Listener** that subscribes to `first_test_topic` and prints the received value using `RCLCPP_INFO()`. Display the value history using **rqt**.

---

## 🔗 References
- [ROS 2 Publisher/Subscriber Tutorial (C++)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.html)
- [std_msgs API](https://docs.ros2.org/latest/api/std_msgs/)
- [colcon documentation](https://colcon.readthedocs.io/)
