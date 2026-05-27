# EU_02 – Robot Operating System II

> **Robotics Frameworks (RoF) · FAU Erlangen-Nürnberg · Winter Semester 2025/26**
> Lecturer: Dr.-Ing. Sebastian Reitelshöfer

---

## 📖 Theory Overview

### Launch Files
A **launch file** is a Python script that starts multiple ROS2 nodes simultaneously using a single command. This eliminates the need to open many terminals for complex systems.

```python
ros2 launch <package_name> <launch_file.py>
```

### Custom Messages with IDL
ROS2 uses the **Interface Definition Language (IDL)** to define custom message types in `.msg` files and service types in `.srv` files. After building and sourcing, these become typed C++ headers or Python modules.

| File type | Where | Usage |
|---|---|---|
| `.msg` | `<pkg>/msg/Num.msg` | Custom message for topics |
| `.srv` | `<pkg>/srv/Add.srv` | Custom request/response for services |

### TF2 — Transform Tree
**TF2** maintains a tree of coordinate frames and their relationships over time. Every robot system needs it for localization, sensor fusion, and navigation.

```
world                  ← fixed/global frame
  └── frame1            ← robot body (offset 1,1,0 from world)
        └── frame2       ← rotating child frame (0,0,1.5 above frame1)
```

A `TransformBroadcaster` publishes `geometry_msgs/TransformStamped` on `/tf`.
The rotation uses **quaternions** (4-component rotation representation, avoids gimbal lock):

```
tf2::Quaternion q;
q.setRPY(roll, pitch, yaw);   // convert Euler angles to quaternion
```

### ROS2 Services (Client–Server Pattern)
Services implement **synchronous** request/response:
- Only ONE server per service name can exist
- MANY clients can call the same server
- The client **blocks** (or waits asynchronously) until the server replies

```
Client ──[Request: a=5, b=7]──► Server
       ◄──[Response: sum=12]──
```

---

## 📁 File Structure

```
EU_02_ROS_II/
├── README.md
├── msg/
│   └── Num.msg                  # Custom Int64 message definition
├── srv/
│   └── Add.srv                  # Service: (int64 a, int64 b) → int64 sum
├── launch/
│   └── pubsub_launch.py         # Launches publisher + subscriber together
└── src/
    ├── broadcaster_node.cpp     # TF Task 1: world→frame1→frame2 broadcaster
    ├── server_node.cpp          # Service server: add_two_ints
    └── client_node.cpp          # Service client: sends A+B, prints result
```

---

## 🔨 Build Instructions

### Package 1: `my_tf_package` (TF Broadcaster)
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake \
  --dependencies rclcpp geometry_msgs tf2 tf2_ros \
  --node-name broadcaster_node my_tf_package

# Replace src/broadcaster_node.cpp with this file's content
cd ~/ros2_ws
colcon build --symlink-install --packages-select my_tf_package
source install/setup.bash
```

### Package 2: `my_cliserv_package_interfaces` (Service Interface)
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake my_cliserv_package_interfaces
cd my_cliserv_package_interfaces && mkdir srv
# Copy Add.srv into srv/

# Edit package.xml and CMakeLists.txt per PDF instructions:
#   package.xml: add rosidl_default_generators, rosidl_default_runtime, rosidl_interface_packages
#   CMakeLists.txt: add find_package(rosidl_default_generators)
#                       rosidl_generate_interfaces(${PROJECT_NAME} "srv/Add.srv")

cd ~/ros2_ws && colcon build --symlink-install --packages-select my_cliserv_package_interfaces
```

### Package 3: `my_cliserv_package` (Server + Client)
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake \
  --dependencies rclcpp my_cliserv_package_interfaces \
  --node-name server_node my_cliserv_package
# Copy server_node.cpp and client_node.cpp into src/
cd ~/ros2_ws && colcon build --symlink-install --packages-select my_cliserv_package
source install/setup.bash
```

---

## ▶️ Running the Nodes

### Task 1 — TF2 Broadcaster
```bash
# Terminal 1: Run the broadcaster
ros2 run my_tf_package broadcaster_node

# Terminal 2: Visualise in RViz2
ros2 run rviz2 rviz2
# In RViz: Add → By Display Type → TF
# Set Fixed Frame to "world"

# Terminal 3: Print TF tree
ros2 run tf2_tools view_frames
```

### Tasks 2/3 — Service Server + Client
```bash
# Terminal 1: Start the server
ros2 run my_cliserv_package server_node

# Terminal 2: Call with A=5 and B=7
ros2 run my_cliserv_package client_node 5 7
# Expected output: 5 + 7 = 12

# Or call the service manually via CLI:
ros2 service call /add_two_ints my_cliserv_package_interfaces/srv/Add "{a: 10, b: 32}"
```

### Launch File
```bash
# Start both publisher and subscriber nodes in one command:
ros2 launch my_pubsub_package pubsub_launch.py
```

---

## 📝 Task Summary (from EU_02 PDF – Page 15)

> **Task 1:** Extend the `transform_broadcaster_node` to publish:
> - `world → frame1` with XYZ=(1, 1, 0) and RPY=(0, 0, 0)
> - `frame1 → frame2` with XYZ=(0, 0, 1.5) and a **continuous rotation around Z** at +10° every 100 ms

---

## 🔗 References
- [TF2 Tutorial (ROS2 Humble)](https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Tf2-Main.html)
- [Writing a ROS2 Service (C++)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Service-And-Client-CPP.html)
- [Custom Interfaces](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html)
- [Launch Files](https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Launch-system.html)
