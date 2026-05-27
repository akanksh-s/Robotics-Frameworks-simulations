# EU_06 – Navigation of Mobile Robots with ROS2

> **Robotics Frameworks (RoF) · FAU Erlangen-Nürnberg · Winter Semester 2025/26**
> Lecturer: Matthias Kalenberg

---

## 📖 Theory Overview

### Three Core Navigation Tasks

```
           ┌─────────────────┐
           │   Path Planning │  ← How to get from A to B?
           │  and Execution  │
           └────────┬────────┘
                    │
     ┌──────────────┼──────────────┐
     │              │              │
┌────▼────┐   ┌────▼────┐   ┌────▼────┐
│Mapping  │   │Localiz. │   │Execution│
│ Where   │   │ Where   │   │ Motion  │
│ are the │   │  am I?  │   │ Control │
│obstacles│   │         │   │         │
└─────────┘   └─────────┘   └─────────┘
```

### The Nav2 Metapackage
**Navigation2 (Nav2)** is the ROS2 navigation stack that integrates all three components:

| Component | Package | Role |
|---|---|---|
| **SLAM Toolbox** | `slam_toolbox` | Simultaneous Localization and Mapping |
| **Global Costmap** | `nav2_costmap_2d` | Inflated obstacle map for path planning |
| **Global Planner** | `nav2_planner` (NavFn/A*) | Computes optimal path from A to B |
| **Local Planner** | `nav2_controller` (DWB) | Generates `/cmd_vel` to follow the path |
| **BT Navigator** | `nav2_bt_navigator` | Behavior Tree orchestrating all components |
| **Map Server** | `nav2_map_server` | Loads pre-built maps for localization |
| **ACML** | `nav2_amcl` | Particle filter localization in a known map |

### TF Frame Chain
```
map → odom → base_footprint → base_link → sensors (lidar, camera)
```
- **map ↔ odom**: Published by slam_toolbox (corrects for odometry drift)
- **odom ↔ base_footprint**: Published by the robot's odometry (wheel encoders)
- **base_footprint ↔ sensors**: Published by static TF from URDF

### Control Interface
```
geometry_msgs/Twist → /cmd_vel
  linear.x  = forward/backward speed (m/s)
  angular.z = rotation speed (rad/s)

nav_msgs/Odometry → /odom
  pose.pose.position.x/y  = robot position
  pose.pose.orientation   = quaternion (yaw = heading)
```

---

## 📁 File Structure

```
EU_06_Navigation/
├── README.md                            # This file
├── launch/
│   ├── slam_launch.py                   # Launches slam_toolbox for mapping
│   └── navigation_launch.py            # Launches full Nav2 stack
└── config/
    ├── slam_params.yaml                 # SLAM toolbox configuration
    └── navigation_params.yaml          # Nav2 stack configuration

lecture-6-navigation-i-main/
└── LU6-NavigationI.ipynb               # Jupyter notebook: Kalman Filter & Localization
```

---

## 🔨 Setup Instructions

### Install Dependencies
```bash
sudo apt install ros-humble-navigation2
sudo apt install ros-humble-nav2-bringup
sudo apt install ros-humble-slam-toolbox
sudo apt install ros-humble-turtlebot3-gazebo
sudo apt install ros-humble-rqt-robot-steering
```

### Create the `rof_navigation` Package
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python rof_navigation
cd rof_navigation
mkdir launch config

# Copy slam_launch.py → launch/
# Copy navigation_launch.py → launch/
# Copy slam_params.yaml → config/
# Copy navigation_params.yaml → config/

# Edit package.xml: add <exec_depend>ros2launch</exec_depend>
# Edit setup.py: add launch and config data_files entries
```

---

## ▶️ Step-by-Step Navigation Workflow

### Phase 1 — Mapping (build the map)
```bash
# Terminal 1: Start Gazebo simulation
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/ros2_ws/src/rof_gazebo/models
ros2 launch rof_gazebo t3_simulation_faps.launch.py

# Terminal 2: Start SLAM (builds map from LIDAR data)
ros2 launch rof_navigation slam_launch.py

# Terminal 3: Visualise in RViz2
ros2 launch nav2_bringup rviz_launch.py

# Terminal 4: Drive the robot to build the map
ros2 run rqt_robot_steering rqt_robot_steering

# → Drive around the entire environment to map it
```

### Phase 2 — Save the Map
```bash
# In RViz / rqt:
rqt
# Plugins → Services → Service Caller
# Service: /slam_toolbox/serialize_map
# filename: '/home/robot/map'
# → Call → Returns 0 (success)
# This creates map.data and map.posegraph in ~/
```

### Phase 3 — Localization + Navigation (use the saved map)
```bash
# Edit config/slam_params.yaml:
#   mode: localization
#   map_file_name: /home/robot/map
#   map_start_pose: [0.0, 0.0, 0.0]

# Terminal 1: Gazebo
ros2 launch rof_gazebo t3_simulation_faps.launch.py

# Terminal 2: SLAM in localization mode
ros2 launch rof_navigation slam_launch.py

# Terminal 3: Nav2 stack
ros2 launch rof_navigation navigation_launch.py

# Terminal 4: RViz (set 2D Nav Goal to command the robot)
ros2 launch nav2_bringup rviz_launch.py

# → In RViz: click "2D Nav Goal" → click on destination on the map
# → Robot autonomously navigates to the goal!
```

---

## 📓 Jupyter Notebook (LU6-NavigationI.ipynb)

The notebook covers:
- **Localization** — Probability-based position estimation
- **Mapping** — Occupancy grid construction from LIDAR data
- **Kalman Filter** — Optimal state estimation (position + velocity) from noisy sensor data

```bash
# Install dependencies
pip install ipykernel numpy matplotlib filterpy ipywidgets

# Launch Jupyter
jupyter notebook LU6-NavigationI.ipynb
```

---

## 📝 Task Summary (from EU_06 PDF)

> **Exercise Tasks:**
> 1. **Step 1** — Set up and run the FAPS simulation world with TurtleBot3
> 2. **Step 2** — Use SLAM Toolbox to map the environment while driving manually
> 3. **Step 3** — Save the generated map via the `/slam_toolbox/serialize_map` service
> 4. **Step 4** — Switch to localization mode and run Nav2 for autonomous navigation
> 5. **Homework** — Extend the launch files to send automated navigation goals programmatically

---

## 🔗 References
- [Nav2 Documentation](https://navigation.ros.org/)
- [SLAM Toolbox GitHub](https://github.com/SteveMacenski/slam_toolbox)
- [Nav2 Bringup params](https://github.com/ros-navigation/navigation2/blob/humble/nav2_bringup/params/nav2_params.yaml)
- [TurtleBot3 Navigation](https://emanual.robotis.com/docs/en/platform/turtlebot3/navigation/)
