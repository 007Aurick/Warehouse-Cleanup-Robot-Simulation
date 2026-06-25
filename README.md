# 🤖 Amazon Warehouse Robot Simulation
> Autonomous warehouse robot simulation using ROS 2, Gazebo, SLAM Toolbox, and a LiDAR camera for intelligent package sorting.
---
Table of Contents
Overview
System Architecture
Features
Prerequisites
Installation
Project Structure
Configuration
Running the Simulation
Package Sorting Pipeline
SLAM & Navigation
LiDAR Camera Integration
Topics & Services
Troubleshooting
Contributing
License
---
Overview
This project simulates an autonomous mobile robot (AMR) operating inside an Amazon-style fulfillment warehouse. The robot navigates the warehouse floor using SLAM (Simultaneous Localization and Mapping), avoids dynamic obstacles, and uses a LiDAR camera (e.g., Intel RealSense L515 or similar) to detect, classify, and sort packages to their designated drop zones.
The simulation environment is built in Gazebo and the entire software stack runs on ROS 2 (Humble / Iron).
---
System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                        ROS 2 Stack                          │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  LiDAR Cam   │───▶│  SLAM        │───▶│  Nav2        │  │
│  │  (Perception)│    │  Toolbox     │    │  Planner     │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                                        │          │
│         ▼                                        ▼          │
│  ┌──────────────┐                        ┌──────────────┐  │
│  │  Package     │                        │  Robot       │  │
│  │  Classifier  │───────────────────────▶│  Controller  │  │
│  └──────────────┘                        └──────────────┘  │
│                                                             │
└───────────────────────────┬─────────────────────────────────┘
                            │
                  ┌─────────▼─────────┐
                  │      Gazebo       │
                  │    Simulation     │
                  └───────────────────┘
```
---
Features
Fully simulated Amazon-style warehouse environment in Gazebo
Autonomous navigation powered by Nav2 stack
Real-time map building with SLAM Toolbox
LiDAR point cloud processing for 3D package detection
Package classification by size, shape, and label using sensor fusion
Multi-zone drop-off routing logic
Dynamic obstacle avoidance (human workers, forklifts)
RViz2 visualization for live map, robot pose, and sensor feeds
Configurable shelf layouts and package spawn patterns
Modular robot URDF with differential drive and sensor mounts
---
Prerequisites
Dependency	Version	Notes
Ubuntu	22.04 LTS	Recommended OS
ROS 2	Humble Hawksbill	LTS release
Gazebo	Fortress (11)	Classic or Ignition
Python	3.10+	For perception nodes
SLAM Toolbox	Latest	`apt` install
Nav2	Latest	Navigation stack
PCL (Point Cloud Library)	1.12+	LiDAR processing
OpenCV	4.x	Image processing
---
Installation
1. Clone the Repository
```bash
git clone https://github.com/your-org/amazon-warehouse-robot-sim.git
cd amazon-warehouse-robot-sim
```
2. Install ROS 2 Dependencies
```bash
sudo apt update && sudo apt install -y \
  ros-humble-slam-toolbox \
  ros-humble-nav2-bringup \
  ros-humble-navigation2 \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-ros2-control \
  ros-humble-robot-state-publisher \
  ros-humble-joint-state-publisher \
  ros-humble-pcl-ros \
  ros-humble-sensor-msgs \
  ros-humble-vision-msgs \
  python3-colcon-common-extensions
```
3. Install Python Dependencies
```bash
pip install -r requirements.txt
```
4. Build the Workspace
```bash
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```
---
Project Structure
```
amazon-warehouse-robot-sim/
├── src/
│   ├── warehouse_description/       # Robot URDF & meshes
│   │   ├── urdf/
│   │   │   ├── robot.urdf.xacro
│   │   │   └── sensors/
│   │   │       └── lidar_camera.xacro
│   │   └── meshes/
│   ├── warehouse_gazebo/            # Simulation world & launch files
│   │   ├── worlds/
│   │   │   └── amazon_warehouse.world
│   │   ├── models/
│   │   │   ├── shelves/
│   │   │   ├── packages/
│   │   │   └── drop_zones/
│   │   └── launch/
│   │       └── warehouse_sim.launch.py
│   ├── warehouse_slam/              # SLAM configuration & launch
│   │   ├── config/
│   │   │   └── slam_toolbox_params.yaml
│   │   └── launch/
│   │       └── slam.launch.py
│   ├── warehouse_navigation/        # Nav2 configuration
│   │   ├── config/
│   │   │   ├── nav2_params.yaml
│   │   │   └── costmap_params.yaml
│   │   └── launch/
│   │       └── navigation.launch.py
│   ├── package_perception/          # LiDAR-based package detection
│   │   ├── package_perception/
│   │   │   ├── lidar_processor.py
│   │   │   ├── package_classifier.py
│   │   │   └── drop_zone_router.py
│   │   └── config/
│   │       └── classifier_params.yaml
│   └── warehouse_bringup/           # Top-level launch files
│       └── launch/
│           └── full_simulation.launch.py
├── maps/                            # Pre-built warehouse maps
│   └── warehouse_map.yaml
├── scripts/
│   ├── spawn_packages.py
│   └── visualize_zones.py
├── requirements.txt
├── package.xml
└── README.md
```
---
Configuration
SLAM Toolbox (`slam_toolbox_params.yaml`)
```yaml
slam_toolbox:
  ros__parameters:
    solver_plugin: solver_plugins::CeresSolver
    ceres_linear_solver: SPARSE_NORMAL_CHOLESKY
    mode: mapping                   # Use 'localization' on known maps
    map_update_interval: 5.0
    max_laser_range: 20.0
    resolution: 0.05
    minimum_travel_distance: 0.5
    minimum_travel_heading: 0.5
    scan_buffer_size: 10
    loop_search_maximum_distance: 3.0
    do_loop_closing: true
```
LiDAR Camera Parameters (`classifier_params.yaml`)
```yaml
lidar_processor:
  ros__parameters:
    point_cloud_topic: /lidar_camera/points
    min_cluster_size: 50
    max_cluster_size: 5000
    cluster_tolerance: 0.05         # 5 cm Euclidean distance
    voxel_leaf_size: 0.02           # Downsampling resolution
    ground_removal_threshold: 0.15  # Meters above ground

package_classifier:
  ros__parameters:
    size_thresholds:
      small:  [0.15, 0.15, 0.15]   # Max XYZ in meters
      medium: [0.40, 0.40, 0.40]
      large:  [0.80, 0.80, 0.80]
    drop_zones:
      small:  "zone_A"
      medium: "zone_B"
      large:  "zone_C"
      unknown: "zone_inspection"
```
---
Running the Simulation
Full Simulation (All-in-One)
```bash
source install/setup.bash
ros2 launch warehouse_bringup full_simulation.launch.py
```
Step-by-Step Launch
```bash
# Terminal 1 — Gazebo world + robot
ros2 launch warehouse_gazebo warehouse_sim.launch.py

# Terminal 2 — SLAM
ros2 launch warehouse_slam slam.launch.py

# Terminal 3 — Navigation
ros2 launch warehouse_navigation navigation.launch.py

# Terminal 4 — Package Perception
ros2 run package_perception lidar_processor

# Terminal 5 — RViz2
rviz2 -d config/warehouse.rviz
```
Spawn Packages into the World
```bash
python3 scripts/spawn_packages.py --count 20 --random-seed 42
```
---
Package Sorting Pipeline
The sorting pipeline runs in three stages:
Detection — The LiDAR camera continuously publishes a `PointCloud2` stream. The `lidar_processor` node applies ground removal, voxel downsampling, and Euclidean cluster extraction to isolate individual package candidates.
Classification — Each cluster's bounding box is computed. The `package_classifier` node bins packages into `small`, `medium`, `large`, or `unknown` categories based on configured dimension thresholds.
Routing — The `drop_zone_router` node generates a Nav2 goal for the appropriate drop zone and dispatches the robot. The robot confirms delivery by re-scanning the drop area for the package's point cloud signature.
```
PointCloud2 ──▶ Ground Removal ──▶ Clustering ──▶ BBox Estimation
                                                         │
                                                ┌────────┴──────────┐
                                                │ Package Classifier │
                                                └────────┬──────────┘
                                                         │
                                               small / medium / large
                                                         │
                                                ┌────────▼──────────┐
                                                │  Drop Zone Router  │
                                                └────────┬──────────┘
                                                         │
                                                   Nav2 Goal Pose
```
---
SLAM & Navigation
The robot builds a 2D occupancy grid map using SLAM Toolbox while simultaneously localizing itself within it. LiDAR scan data is fused with odometry to produce a consistent global map.
Once mapping is complete, save the map with:
```bash
ros2 run nav2_map_server map_saver_cli -f maps/warehouse_map
```
Switch SLAM Toolbox to localization mode for subsequent runs:
```yaml
# slam_toolbox_params.yaml
mode: localization
map_file_name: /path/to/maps/warehouse_map
```
Nav2 handles global path planning (NavFn), local trajectory control (DWB), and recovery behaviors (spin, back-up, wait).
---
LiDAR Camera Integration
The simulation uses a combined LiDAR + RGB-D camera sensor model mounted on the robot's front chassis. The sensor publishes:
Topic	Type	Description
`/lidar_camera/points`	`sensor_msgs/PointCloud2`	3D point cloud
`/lidar_camera/scan`	`sensor_msgs/LaserScan`	2D scan slice for SLAM
`/lidar_camera/image_raw`	`sensor_msgs/Image`	RGB image
`/lidar_camera/depth/image_raw`	`sensor_msgs/Image`	Depth image
In a real-world deployment this maps to sensors such as the Intel RealSense L515, Ouster OS1, or Velodyne VLP-16.
---
Topics & Services
Subscribed Topics
Topic	Type	Node
`/lidar_camera/points`	`PointCloud2`	`lidar_processor`
`/odom`	`nav_msgs/Odometry`	SLAM, Nav2
`/tf`, `/tf_static`	`tf2_msgs/TFMessage`	All nodes
Published Topics
Topic	Type	Node
`/map`	`nav_msgs/OccupancyGrid`	SLAM Toolbox
`/detected_packages`	`vision_msgs/Detection3DArray`	`package_classifier`
`/cmd_vel`	`geometry_msgs/Twist`	Nav2 controller
`/robot_status`	`std_msgs/String`	`drop_zone_router`
Services
Service	Type	Description
`/slam_toolbox/save_map`	`slam_toolbox/SaveMap`	Persist the current map
`/package_sorter/reset`	`std_srvs/Trigger`	Reset sorting state
`/drop_zone_router/get_status`	`std_srvs/Trigger`	Query routing queue
---
Troubleshooting
Gazebo crashes on launch
Make sure `GAZEBO_MODEL_PATH` includes the project models directory:
```bash
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$(pwd)/src/warehouse_gazebo/models
```
SLAM map is drifting
Reduce the robot's maximum speed in `nav2_params.yaml` and ensure the LiDAR scan topic matches the SLAM Toolbox configuration (`scan_topic` parameter).
No point cloud published
Verify the LiDAR plugin is loaded in Gazebo by checking:
```bash
ros2 topic echo /lidar_camera/points --no-arr
```
If no messages appear, check the sensor plugin tag in `lidar_camera.xacro`.
Nav2 goal rejected
Ensure the costmap has finished inflating after the map is loaded. Add a short `ros2 sleep` before publishing goals in automation scripts.
---
Contributing
Fork the repository
Create a feature branch (`git checkout -b feature/your-feature`)
Commit your changes (`git commit -m 'Add some feature'`)
Push to the branch (`git push origin feature/your-feature`)
Open a Pull Request
Please follow the ROS 2 code style guidelines and include unit tests for new nodes.
---
License
This project is licensed under the Apache 2.0 License — see the LICENSE file for details.
---
Built with ROS 2 Humble · Gazebo Fortress · SLAM Toolbox · Nav2 · PCL
