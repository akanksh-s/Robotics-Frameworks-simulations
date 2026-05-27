# Robotics Frameworks
> **ROS2 Humble · Gazebo Classic · Nav2 · FlexBE · OpenCV · TensorFlow/Keras · YOLOv8**
> WS 2025/26 | Dr.-Ing. Sebastian Reitelshofer

This repository contains **all exercise solutions and Colab notebooks** for the Robotics Frameworks course. Code is organized by exercise number and the concept it implements.

---

## 📁 Repository Structure

```
RoF_GitHub/
├── 01_publisher_subscriber/           EU_01 – ROS2 Publisher & Subscriber (C++)
├── 02_services_tf2_launch/            EU_02 – ROS2 Services, TF2, Launch Files (C++)
├── 03_gazebo_simulation_apriltag/     EU_03 – Gazebo Simulation + AprilTag Detection (C++)
│   ├── rof_gazebo/                      Gazebo FAPS world + TurtleBot3 launch
│   ├── apriltag_msgs/                   Custom ROS2 message definitions for AprilTag
│   ├── apriltag_ros/                    AprilTag detector node (camera → TF + detections)
│   └── rof_ex3/                         Robot control nodes (simple + advanced)
├── 05_computer_vision/                EU_05 – OpenCV Image Processing + Perspective Transform (Python)
├── 06_navigation_slam/                EU_06 – SLAM, Nav2, Path Planning (ROS2 + Colab Notebook)
├── 09_ai_machine_learning/            EU_09 – CNN, Transfer Learning (VGG16), YOLO (Python + Colab)
├── 10_12_logistics_capstone/          EU_10-12 – Logistics Task: FlexBE + Nav2 + YOLO (Python + Colab)
└── exam_prep/                         Practice Questions & Answer Key (Markdown)
```

---

## ⚡ Quick Start — Choose your path

| Goal | What to do |
|------|-----------|
| Run ROS2 exercises (EU_01, 02, 06) | Use **VirtualBox VM** with ROS2 Humble → see VM Setup below |
| Run Gazebo + AprilTag (EU_03) | Use **VirtualBox VM** → build apriltag from source first |
| Run CV exercises (EU_05) | Upload `EU_05_CV_Colab.ipynb` to **Google Colab** |
| Run AI exercises (EU_09) | Upload `EU_09_AI_Colab.ipynb` to **Google Colab (T4 GPU)** |
| Understand Navigation theory | Upload `EU_06_Navigation_Colab.ipynb` to **Google Colab** |
| Run logistics capstone (EU_10-12) | Upload `EU_10_12_Practical_Task_Colab.ipynb` to **Colab** |
| Practise for exam | Open `exam_prep/RoF_Practice_Questions.md` |

---

## 🖥️ VM Setup — ROS2 Humble (Ubuntu 22.04 in VirtualBox)

### 1. Base ROS2 Installation

```bash
# Set locale
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Add ROS2 apt repository
sudo apt install software-properties-common curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS2 Humble Desktop (includes RViz2, rqt)
sudo apt update
sudo apt install ros-humble-desktop -y

# Source in every terminal (add to ~/.bashrc)
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 2. Build Tools & colcon

```bash
sudo apt install python3-colcon-common-extensions python3-rosdep python3-vcstool -y
sudo rosdep init
rosdep update
```

### 3. Create the ROS2 Workspace

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# Clone this repo into src/
git clone <this-repo-url> src/rof_exercises

# Install all ROS2 package dependencies
rosdep install --from-paths src --ignore-src -r -y

# Build everything
colcon build
source install/setup.bash
```

### 4. Exercise-Specific Dependencies

#### EU_01 & EU_02 — ROS2 Basics (C++)
```bash
sudo apt install ros-humble-rclcpp ros-humble-std-msgs \
                 ros-humble-geometry-msgs ros-humble-tf2-ros -y
```

#### EU_03 — Gazebo Simulation + AprilTag
```bash
# Step 1: Build apriltag C library from source (v3.3.0 required)
git clone https://github.com/AprilRobotics/apriltag.git ~/apriltag
cd ~/apriltag && git checkout v3.3.0
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc) && sudo make install && sudo ldconfig

# Step 2: ROS2 packages for camera, CV bridge, Gazebo
sudo apt install -y \
  ros-humble-cv-bridge ros-humble-image-transport \
  ros-humble-gazebo-ros-pkgs ros-humble-turtlebot3-gazebo \
  libeigen3-dev

# Step 3: VirtualBox GPU fix
echo "export SVGA_VGPU10=0" >> ~/.bashrc && source ~/.bashrc
```

#### EU_06 — Navigation & SLAM
```bash
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup \
                 ros-humble-slam-toolbox ros-humble-turtlebot3-gazebo \
                 ros-humble-rqt-robot-steering ros-humble-gazebo-ros-pkgs -y

# VirtualBox GPU fix (prevents Gazebo crash)
echo "export SVGA_VGPU10=0" >> ~/.bashrc
source ~/.bashrc
```

#### EU_08 / EU_10-12 — FlexBE State Machines
```bash
# FlexBE core (build from source for Humble)
cd ~/ros2_ws/src
git clone https://github.com/FlexBE/flexbe_behavior_engine.git -b ros2-devel
cd ~/ros2_ws
colcon build --packages-select flexbe_core flexbe_states
source install/setup.bash
```

#### AprilTag (EU_05 ROS2 integration, optional)
```bash
# System library
sudo apt install libapriltag-dev -y

# Build apriltag_ros from source
cd ~/ros2_ws/src
git clone https://github.com/christianrauch/apriltag_ros.git
cd ~/ros2_ws
colcon build --packages-select apriltag_msgs apriltag_ros
source install/setup.bash
```

---

## ☁️ Google Colab Setup — Python Notebooks

No local installation needed — just open [colab.research.google.com](https://colab.research.google.com),
upload the `.ipynb` file, and run cells top-to-bottom.

### EU_05 — Computer Vision
```
Required runtime: CPU (default)
Upload files:     robots.png, paper.jpeg  (when prompted in notebook)
```

### EU_09 — AI / Machine Learning
```
Required runtime: T4 GPU
  → Runtime → Change runtime type → T4 GPU
Dependencies:     auto-installed by notebook (!pip install ultralytics)
```

### EU_06 — Navigation Theory (Colab)
```
Required runtime: CPU (default)
Dependencies:     numpy, matplotlib (pre-installed in Colab)
```

### EU_10-12 — Logistics Capstone (Colab)
```
Required runtime: T4 GPU (for YOLO section)
Dependencies:     auto-installed by notebook
```

---

## 🐍 Local Python Setup (optional — for running .py scripts without Colab)

```bash
# Create virtual environment
python3 -m venv rof_env
source rof_env/bin/activate          # Linux/Mac
# OR: rof_env\Scripts\activate       # Windows PowerShell

# EU_05 — Computer Vision
pip install opencv-python matplotlib numpy

# EU_09 — AI / Machine Learning
pip install tensorflow keras ultralytics matplotlib numpy

# EU_06 — Navigation theory scripts
pip install numpy matplotlib
```

---

## 📦 Package Overview

### [01_publisher_subscriber](./01_publisher_subscriber/) — EU_01: ROS2 Pub/Sub
**What it does:** Talker node publishes `Int64` on `first_test_topic` at 20 Hz (0→50 counter). Listener node subscribes and prints values.
**Run:**
```bash
colcon build --packages-select my_pubsub_package
source install/setup.bash
ros2 run my_pubsub_package publisher_node   # Terminal 1
ros2 run my_pubsub_package subscriber_node  # Terminal 2
rqt                                          # Terminal 3 – visualise topic history
```

---

### [03_gazebo_simulation_apriltag](./03_gazebo_simulation_apriltag/) — EU_03: Gazebo + AprilTag
**What it does:** Spawns a FAPS Gazebo world with TurtleBot3 and a ceiling camera. The `apriltag_ros` node detects an AprilTag mounted on the robot, broadcasts its TF pose in the map frame. Two robot control nodes use that TF to drive the robot autonomously.

| Package | Role |
|---------|------|
| `rof_gazebo` | Gazebo world (FAPS lab) + TurtleBot3 URDF/SDF |
| `apriltag_msgs` | Custom `AprilTagDetection` + `AprilTagDetectionArray` messages |
| `apriltag_ros` | Detects tag36h11 family; publishes TF + `/apriltag/detections` |
| `rof_ex3` | `simple_robot_control`: drives 1m via TF feedback; `advanced_robot_control`: IR + odometry navigation |

**Build & Run:**
```bash
# Build dependency order matters!
colcon build --packages-select apriltag_msgs
colcon build --packages-select apriltag_ros
colcon build --packages-select rof_gazebo rof_ex3
source install/setup.bash

# Terminal 1 — Gazebo
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/ros2_ws/install/rof_gazebo/share/rof_gazebo/models
ros2 launch rof_gazebo t3_simulation_faps.launch.py

# Terminal 2 — AprilTag detector + static TFs
ros2 launch apriltag_ros tag_36h11_all.launch.py

# Terminal 3 — Robot controller
ros2 run rof_ex3 simple_robot_control
```

---

### [02_services_tf2_launch](./02_services_tf2_launch/) — EU_02: Services, TF2, Launch
**What it does:**
- `Add` service: client sends two integers, server returns their sum
- TF2 broadcaster: publishes `world→frame1→frame2` transforms (frame2 rotates at 10°/100ms)
- Launch file: starts both nodes with one command

**Run:**
```bash
colcon build --packages-select my_cliserv_package my_pubsub_package
source install/setup.bash
ros2 run my_cliserv_package server_node           # Terminal 1
ros2 run my_cliserv_package client_node 5 7       # Terminal 2 → prints: 5 + 7 = 12
ros2 run my_tf_package broadcaster_node           # Terminal 3 – TF2
rviz2                                              # Terminal 4 – visualise frames
ros2 launch my_pubsub_package pubsub_launch.py    # OR: launch both nodes at once
```

---

### [05_computer_vision](./05_computer_vision/) — EU_05: OpenCV Image Processing
**What it does:** Grayscale conversion, binary thresholding, blur filters (Average/Gaussian/Median), Canny edge detection, perspective transformation.

**Run locally:**
```bash
cd 05_computer_vision/
python3 image_processing_solution.py        # requires robots.png in same folder
python3 perspective_transformation_solution.py  # requires paper.jpeg
```
**Run on Colab:** Upload `EU_05_CV_Colab.ipynb`

---

### [06_navigation_slam](./06_navigation_slam/) — EU_06: SLAM + Nav2
**What it does:** ROS2 package with SLAM Toolbox launch file, Nav2 navigation launch file, and configuration YAMLs for a TurtleBot3 in Gazebo.

**Colab Notebook covers:** Occupancy grids, A*/Dijkstra/BFS path planning, 1D Kalman Filter, SLAM simulation.

**Run on VM:**
```bash
colcon build --packages-select rof_ex6
source install/setup.bash

# Phase 1: Mapping
ros2 launch rof_ex6 slam_launch.py

# Phase 2: Navigation (after saving map)
ros2 launch rof_ex6 navigation_launch.py
```

---

### [09_ai_machine_learning](./09_ai_machine_learning/) — EU_09: AI in Robotics
**What it does:**
- `keras_example_solution.py`: CNN from scratch on MNIST (Conv2D → MaxPool → Dense → Softmax)
- `keras_retrain_solution.py`: Transfer learning with VGG16 (freeze early layers, retrain head)
- `YOLO_example.py`: Real-time webcam object detection with YOLOv8

**Run locally:**
```bash
cd 09_ai_machine_learning/
python3 keras_example_solution.py    # trains CNN on MNIST
python3 YOLO_example.py              # opens webcam for YOLO detection
```
**Run on Colab (recommended — GPU):** Upload `EU_09_AI_Colab.ipynb`

---

### [10_12_logistics_capstone](./10_12_logistics_capstone/) — EU_10-12: Capstone Task
**What it does:** FlexBE state machine orchestrating a logistics workflow on the iRobot Create 3:
Start → Navigate to A → Check for object (YOLO) → Navigate to B (found) or C (not found) → Return to Start

**Components:**
- `state_machine/logistics_task_sm.py`: FlexBE behavior combining Nav2 + YOLO
- `perception/yolo_subscriber.py`: ROS2 node displaying live YOLO detections from robot camera

**Run on VM (with robot):**
```bash
export ROS_DOMAIN_ID=<lab_id>
colcon build --packages-select rof_ex10_12
source install/setup.bash
ros2 run rof_ex10_12 yolo_subscriber    # view robot camera + YOLO
```


## 🔗 Key Documentation Links

| Topic | Link |
|-------|------|
| ROS2 Humble Docs | https://docs.ros.org/en/humble/ |
| Nav2 Documentation | https://navigation.ros.org/ |
| SLAM Toolbox | https://github.com/SteveMacenski/slam_toolbox |
| FlexBE | https://github.com/FlexBE/flexbe_behavior_engine |
| OpenCV Python | https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html |
| Keras / TensorFlow | https://keras.io/guides/ |
| Ultralytics YOLOv8 | https://docs.ultralytics.com/ |
| TurtleBot3 | https://emanual.robotis.com/docs/en/platform/turtlebot3/ |

---

## ⚠️ Important Notes

- Always run `source install/setup.bash` in every new terminal before using ROS2 commands
- For Gazebo on VirtualBox: `export SVGA_VGPU10=0` must be set (already added to `~/.bashrc` by setup)
- EU_06, EU_08, EU_10-12 **require the VM** — they cannot run in Colab
- EU_05, EU_09, EU_10-12 Colab notebooks are **self-contained** — no ROS2 needed
- For EU_10-12 on the real robot: set `ROS_DOMAIN_ID` to match the robot's domain ID

---

*FAU Erlangen-Nürnberg · Institute FAPS · Robotics Frameworks WS 2025/26*
