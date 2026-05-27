# EU_10-12 – Practical Task

> **Robotics Frameworks (RoF) · FAU Erlangen-Nürnberg · Winter Semester 2025/26**
> Lecturers: Ziegler & Engelhardt

---

## 📖 Overview

This is the **capstone exercise** integrating all previously learned skills:

| EU | Skill Used |
|---|---|
| EU_05 | Object detection via AI (YOLO) |
| EU_06 | Robot navigation using Nav2 stack |
| EU_08 | FlexBE state machines for robot behavior |

The exercise takes place at the **FAPS laboratory (Egerlandstraße 7-9, Erlangen)** using a real **iRobot Create 3** robot.

---

## 🤖 The Robot: iRobot Create 3

| Component | Details |
|---|---|
| **Platform** | iRobot Create® 3 (commercial robotics platform) |
| **Compute** | NVIDIA Jetson Orin Nano (8GB) |
| **Sensors** | USB Camera (front top) + RPLIDAR (center) |
| **Connectivity** | Wi-Fi, Bluetooth, Ethernet over USB |
| **OS/Framework** | Ubuntu + ROS2 Humble |
| **Battery** | 26 Wh 4S Li-Ion, charges via Home Base Dock |

**Key topics on the iRobot:**
```
/cmd_vel          geometry_msgs/Twist       → Velocity command (input to robot)
/odom             nav_msgs/Odometry         → Wheel odometry
/scan             sensor_msgs/LaserScan     → RPLIDAR 360° scan
/camera/image_raw sensor_msgs/Image         → Front camera
/yolo/detections  yolo_msgs/DetectionArray  → YOLO detections (on Jetson)
```

---

## 📁 File Structure

```
EU_10_12_Practical_Task/
├── README.md                           # This file
├── perception/
│   └── yolo_subscriber.py              # Task 3: Subscribe to YOLO detections from iRobot
└── state_machine/
    └── logistics_task_sm.py            # Task 4: Full logistics FlexBE state machine
```

---

## 🧠 Logistics Task State Machine

```
         ┌──────────────┐
         │  Start (S)   │
         └──────┬───────┘
                │ navigate
         ┌──────▼───────┐
         │   NavToA     │  → Drive to Position A
         └──────┬───────┘
                │ arrived
         ┌──────▼───────┐
         │  CheckObject │  → YOLO: is there an object?
         └──┬───────────┘
       found │   │ not_found
    ┌────────▼┐  └──────────►┌───────────┐
    │  NavToB │               │  NavToC   │  → Drive to C (no-object branch)
    └────┬────┘               └─────┬─────┘
         │                          │ arrived
         │                   ┌──────▼──────┐
         │                   │  Wait 10s   │  → Unloading simulation
         │                   └──────┬──────┘
         │                          │ done
         └──────────────────►┌──────▼──────┐
                             │ReturnToStart│  → Drive back to S
                             └──────┬──────┘
                                    │ arrived
                             ┌──────▼──────┐
                             │  StopAtHome │  → Confirm stopped
                             └──────┬──────┘
                                    │
                                 finished
```

---

## ▶️ Step-by-Step Workflow

### Prerequisites
1. Ensure EU_05, EU_06, EU_08 exercises are completed on your USB stick
2. Clone the required message package:
   ```bash
   cd ~/ros2_ws/src
   git clone https://git.faps.uni-erlangen.de/heengelhardt/yolo_msgs
   cd ~/ros2_ws && colcon build --packages-select yolo_msgs
   source install/setup.bash
   ```
3. Connect to the lab Wi-Fi; set correct ROS_DOMAIN_ID:
   ```bash
   # Add to ~/.bashrc (get actual ID from lab supervisor):
   export ROS_DOMAIN_ID=<lab_id>
   source ~/.bashrc
   ```

---

### Task 1 — Familiarize with iRobot Create 3
```bash
# Test connectivity:
ros2 topic list                                     # Should show iRobot topics

# View the TF tree:
ros2 run rqt_tf_tree rqt_tf_tree

# Check the graph:
rqt_graph
```

---

### Task 2 — Move the Robot
```bash
# Option A: Publish Twist directly
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.1, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.5}}"

# Option B: rqt robot steering plugin
sudo apt install ros-humble-rqt-robot-steering
ros2 run rqt_robot_steering rqt_robot_steering
# → Set topic to /cmd_vel, adjust speed and rotation sliders
```

---

### Task 2 — Navigation with Nav2
```bash
# Reuse your rof_navigation package from EU_06, but set use_sim_time:=false
# for the real robot!

# Terminal 1: SLAM (mapping mode)
ros2 launch rof_navigation slam_launch.py use_sim_time:=false

# Terminal 2: Nav2
ros2 launch rof_navigation navigation_launch.py use_sim_time:=false

# Terminal 3: RViz visualization
ros2 launch nav2_bringup rviz_launch.py

# → Drive around to build the map, then set navigation goals via RViz
# → Tune parameters: resolution, max_x, min_x, max_theta, min_theta
```

**Key parameter changes for real robot (in navigation_params.yaml):**
```yaml
use_sim_time: false     # ← CRITICAL: must be false on real robot
max_vel_x: 0.2         # Reduce speed for lab safety
```

---

### Task 3 — Object Perception (YOLO)
```bash
# Run the YOLO subscriber to see detections from iRobot camera
cd EU_10_12_Practical_Task/perception
python3 yolo_subscriber.py
# → Two windows appear: raw camera + YOLO annotated detections
# → Place objects in front of camera to test, find objects for logistics task
```

---

### Task 4 — Full Logistics State Machine

**Edit `logistics_task_sm.py` first:**
- Set `goal_x`, `goal_y`, `goal_yaw` to actual positions in your lab map
- Set `object_class` to the object you chose in Task 3

```bash
# Copy logistics_task_sm.py into your FlexBE behaviors package:
cp state_machine/logistics_task_sm.py \
   ~/ros2_ws/src/rof_behaviors/rof_flexbe_behaviors/logistics_task_sm.py

cd ~/ros2_ws && colcon build && source install/setup.bash

# Start FlexBE:
ros2 launch flexbe_app flexbe_full.launch.py

# In FlexBE App:
# → Behavior Dashboard → load 'logistics_task'
# → Runtime Control → Start Execution
# → Watch the robot complete the logistics workflow!
```

---

## 💡 Bonus Challenges (from EU_10-12 PDF)
- **Enable start-from-any-position**: Use AMCL to initialise robot pose in the saved map
- **Disturbance test**: Place unexpected objects in the robot's path and observe obstacle avoidance

---

## 📝 Task Summary (from EU_10-12 PDF)

| Task | Goal |
|---|---|
| **Task 1** | Familiarise with iRobot hardware; connect and list topics |
| **Task 2** | Navigate using Nav2; use SLAM to build a map of the lab |
| **Task 3** | Detect objects using YOLO camera on the iRobot |
| **Task 4** | Implement the full logistics state machine: A → detect → B or C → unload → Start |

---

## 🔗 References
- [iRobot Create 3 Documentation](https://iroboteducation.github.io/create3_docs/)
- [YOLO ROS (yolo_ros)](https://github.com/mgonzs13/yolo_ros)
- [Nav2 Real Robot Setup](https://navigation.ros.org/setup_guides/index.html)
- [FlexBE Documentation](https://flexbe.github.io/)
