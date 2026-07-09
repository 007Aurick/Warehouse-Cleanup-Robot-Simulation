# 🦾 TeleArm — SLAM-Mapped Mobile Manipulator

> A teleoperated mobile robot that maps its environment in real time and performs on-demand pick-and-place using a mounted robotic arm — all visualized live in RViz2.

![ROS2](https://img.shields.io/badge/ROS2-Humble-blue?logo=ros&logoColor=white)
![Gazebo](https://img.shields.io/badge/Gazebo-Simulation-orange?logo=gazebo&logoColor=white)
![RViz2](https://img.shields.io/badge/RViz2-Visualization-9cf)
![SLAM](https://img.shields.io/badge/SLAM-slam__toolbox-green)
![Status](https://img.shields.io/badge/status-in%20development-yellow)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 📖 Overview

**TeleArm** combines three core ROS2 concepts into one working robot:

- 🕹️ **Manual driving** via teleop keyboard control
- 🗺️ **Live SLAM mapping** of the environment using LiDAR
- 🦾 **On-command pick-and-place** using a mounted robotic arm

Drive the robot around a warehouse-style environment, watch the map build live in RViz2, and press a single key to trigger the arm's pick-and-place sequence wherever you've stopped. No autonomous navigation, no object detection required — just clean, understandable ROS2 fundamentals stacked together.

---

## ✨ Features

- 🚗 Manual teleoperation of a differential-drive mobile base (`/cmd_vel`)
- 📡 Real-time SLAM mapping using `slam_toolbox` + LiDAR scan data
- 🌲 Full TF tree: `map → odom → base_link → arm_base_link → ... → gripper`
- 🦾 Fixed-mount robotic arm riding on top of the mobile base
- ⌨️ Single keypress trigger (`spacebar`) to execute a scripted pick-and-place pose sequence
- 🖥️ Fully visualized in RViz2 — robot model, TF frames, LiDAR scan, and occupancy grid map

---

## 🧠 How It Works

```
🕹️ Teleop Keys ──► /cmd_vel ──► Base Drives ──► Odometry ──► TF (base position)
                                                     │
📡 LiDAR ───────────────────────────────────────────┼──► slam_toolbox ──► 🗺️ Live Map
                                                     │
⌨️ Spacebar ──► /trigger_pickplace ──► Arm Node ──► /joint_states ──► TF (arm position)
                                                     │
                                          🖥️ RViz2 renders everything together
```

- **Driving** and **arm control** are fully independent systems that just happen to share the same robot chassis.
- SLAM has **zero awareness** of the arm — it only processes LiDAR scan data and odometry.
- The arm is mounted via a **fixed joint** on top of the base, so it moves along with the robot but operates on its own separate TF branch.

---

## 🛠️ Tech Stack

| Component            | Tool/Package                        |
|-----------------------|--------------------------------------|
| Middleware            | ROS2 (Humble)                        |
| Simulation             | Gazebo                              |
| Mapping                 | `slam_toolbox`                     |
| Visualization           | RViz2                               |
| Robot Description      | URDF / Xacro                        |
| Teleoperation           | `teleop_twist_keyboard`             |
| Arm Control             | Custom joint-state publisher node   |

---

## 📂 Project Structure

```
telearm_ws/
├── telearm_description/     # URDF/Xacro files for base + arm
│   ├── urdf/
│   └── meshes/
├── telearm_bringup/         # Launch files (SLAM, teleop, RViz configs)
├── telearm_arm_control/     # Pick-and-place trigger + pose sequence node
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- ROS2 Humble
- Gazebo
- `slam_toolbox`
- `teleop_twist_keyboard`

### Build
```bash
cd ~/telearm_ws
colcon build --symlink-install
source install/setup.bash
```

### Run
```bash
# Terminal 1 — launch simulation + robot
ros2 launch telearm_bringup telearm_sim.launch.py

# Terminal 2 — start SLAM
ros2 launch telearm_bringup slam.launch.py

# Terminal 3 — teleop keyboard
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# Terminal 4 — arm control node
ros2 run telearm_arm_control pick_place_trigger
```

Drive around with `WASD`, watch the map build in RViz2, and press **spacebar** to trigger the arm's pick-and-place sequence. 🦾📦

---

## 🎯 Roadmap

- [x] Manual teleop driving
- [x] Live SLAM mapping
- [x] Arm mounted on mobile base
- [x] Keypress-triggered pick-and-place
- [ ] 📷 Camera-based object detection (auto-trigger instead of keypress)
- [ ] 🎨 Color-based sorting into multiple bins
- [ ] 🤖 MoveIt2 integration for real motion planning

---

## 🤝 Contributing

Pull requests, issues, and suggestions are welcome! This is a learning project, so feedback that helps simplify or clarify things is especially appreciated. 🙌

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [ros2_control_demos](https://github.com/ros-controls/ros2_control_demos)
- [ROBOTIS OpenManipulator](https://github.com/ROBOTIS-GIT/open_manipulator)
- [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)

---

<p align="center">Built with ⚙️, ☕, and way too many terminal windows.</p>
