# 03 — Gazebo Simulation with AprilTag Detection

> **EU_03 · Robotics Frameworks · FAU Erlangen-Nürnberg**
>
> **Topic:** Robot simulation in Gazebo Classic + AprilTag-based robot localisation using a ceiling camera and TF2.

---

## 📁 Package Structure

```
03_gazebo_simulation_apriltag/
│
├── rof_gazebo/                     ← Gazebo world + TurtleBot3 robot model
│   ├── launch/
│   │   └── t3_simulation_faps.launch.py   ← Spawns Gazebo with FAPS world + TurtleBot3
│   ├── package.xml
│   └── CMakeLists.txt
│
├── apriltag_msgs/                  ← Custom AprilTag ROS2 message definitions
│   ├── msg/
│   │   ├── AprilTagDetection.msg
│   │   └── AprilTagDetectionArray.msg
│   ├── package.xml
│   └── CMakeLists.txt
│
├── apriltag_ros/                   ← AprilTag ROS2 detection node (C++)
│   ├── src/
│   │   ├── AprilTagNode.cpp        ← Main detector node (subscribes to camera, publishes TF + detections)
│   │   ├── tag_functions.cpp       ← Tag family factory functions
│   │   └── tag_functions.hpp
│   ├── launch/
│   │   └── tag_36h11_all.launch.py ← Launch: ceiling camera + static TF + tag detector
│   ├── package.xml
│   └── CMakeLists.txt
│
└── rof_ex3/                        ← Robot control nodes (C++)
    ├── src/
    │   ├── simple_robot_control.cpp    ← Task 1: Drive 1m using AprilTag TF feedback
    │   └── advanced_robot_control.cpp  ← Task 2 (Homework): Navigate with IR sensors + odometry
    ├── include/
    │   └── jetbot_gazebo/
    │       ├── simple_robot_control.h
    │       └── advanced_robot_control.h
    ├── package.xml
    └── CMakeLists.txt
```

---

## 🧠 How It Works

### The System Pipeline

```
Gazebo Simulation
  ↓ /ceiling_camera/image_raw   (overhead camera image)
  ↓ /ceiling_camera/camera_info (intrinsics)

AprilTagNode (apriltag_ros)
  ↓ Detects tag36h11:0 on the robot
  ↓ Computes 3D pose via homography  H = K·T  →  T = K⁻¹·H
  ↓ Publishes TF:  ceiling_camera → tag36h11:0
  ↓ Publishes: /apriltag/detections

Static TF publishers (in launch file)
  ↓ map → ceiling_camera          (where is the camera in the world?)
  ↓ tag36h11:0 → chassis          (where is the tag on the robot?)

SimpleRobotControl
  ↓ tf_buffer->lookupTransform("map", "tag36h11:0")
  ↓ If robot moved < 1.0 m from initial TF pose → drive forward
  ↓ Publishes /jetbot/cmd_vel (geometry_msgs/Twist)
```

### Key Concept: AprilTag Pose Estimation
The `AprilTagNode` receives a camera image and intrinsic matrix **K** from `camera_info`, detects the AprilTag pattern, and computes the 3×3 homography **H** relating image to tag corners. The tag's 3D pose is recovered as:

```
T = K⁻¹ · H
```

Where the columns of **T** give the rotation matrix columns and the last column gives the 3D translation. This pose is broadcast as a TF transform.

---

## ⚙️ Dependencies

### 1. System library — apriltag v3.3.0 (must be built from source)
```bash
cd ~
git clone https://github.com/AprilRobotics/apriltag.git
cd apriltag
git checkout v3.3.0
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
sudo make install
sudo ldconfig
```

### 2. ROS2 packages
```bash
sudo apt install -y \
  ros-humble-cv-bridge \
  ros-humble-image-transport \
  ros-humble-camera-info-manager \
  ros-humble-tf2-ros \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-turtlebot3-gazebo \
  libeigen3-dev
```

### 3. VirtualBox GPU fix (prevents Gazebo crash)
```bash
echo "export SVGA_VGPU10=0" >> ~/.bashrc
source ~/.bashrc
```

---

## 🔨 Build

```bash
# Copy packages into your workspace
cp -r 03_gazebo_simulation_apriltag/apriltag_msgs ~/ros2_ws/src/
cp -r 03_gazebo_simulation_apriltag/apriltag_ros  ~/ros2_ws/src/
cp -r 03_gazebo_simulation_apriltag/rof_ex3       ~/ros2_ws/src/
cp -r 03_gazebo_simulation_apriltag/rof_gazebo    ~/ros2_ws/src/

# Build in dependency order
cd ~/ros2_ws
colcon build --packages-select apriltag_msgs
colcon build --packages-select apriltag_ros
colcon build --packages-select rof_gazebo rof_ex3
source install/setup.bash
```

---

## ▶️ Run

### Step 1 — Start Gazebo with FAPS world + TurtleBot3
```bash
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/ros2_ws/install/rof_gazebo/share/rof_gazebo/models
ros2 launch rof_gazebo t3_simulation_faps.launch.py
```

### Step 2 — Start AprilTag detector + TF publishers
```bash
# In a new terminal:
source ~/ros2_ws/install/setup.bash
ros2 launch apriltag_ros tag_36h11_all.launch.py
```

### Step 3 — Start the robot controller
```bash
# Task 1: Simple control (TF-based, drives 1 m using AprilTag feedback)
ros2 run rof_ex3 simple_robot_control

# OR Task 2 (Homework): Advanced control (IR sensors + odometry)
ros2 run rof_ex3 advanced_robot_control
```

### Step 4 — Visualise in RViz2
```bash
rviz2
# Add displays: TF, Image (/ceiling_camera/image_raw), RobotModel
```

---

## 📋 Exercise Tasks

| Task | Node | What it does |
|------|------|-------------|
| **Task 1** | `simple_robot_control` | Reads TF `map→tag36h11:0`. Drives forward until 1 m has been travelled (comparing initial vs. current TF pose). |
| **Task 2 (HW)** | `advanced_robot_control` | Uses front IR sensor to navigate to a wall, rotates 90°, then drives along a row of boxes using side IR sensor to detect gaps. |

---

## 🔑 Key Code Concepts

### TF Lookup in C++ (`simple_robot_control.cpp`)
```cpp
// Look up robot position in map frame via AprilTag TF
current_pose_ = tf_buffer_->lookupTransform("map", "tag36h11:0", tf2::TimePointZero);

// Compute travelled distance from initial pose
double dx = inital_pose_.transform.translation.x - current_pose_.transform.translation.x;
if (abs(dx) < 1.0) {
    vel_msg.linear.x = 1.0;  // drive forward
}
```

### AprilTag TF chain
```
map  →(static)→  ceiling_camera  →(AprilTagNode)→  tag36h11:0  →(static)→  chassis
```

---

## 🔗 References
- [AprilTag library](https://github.com/AprilRobotics/apriltag)
- [apriltag_ros (christianrauch)](https://github.com/christianrauch/apriltag_ros)
- [Gazebo ROS packages](http://gazebosim.org/tutorials?tut=ros2_overview)
- [TF2 C++ tutorial](https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Listener-Cpp.html)
