# Environment Setup

This section provides the core setup pipeline for:
- PX4 Autopilot (SITL)
- ROS 2 Humble
- Micro XRCE-DDS Agent (PX4 ↔ ROS2 bridge)

---

## 1. Setup Directory

Create a dedicated workspace for setup scripts:

```bash
mkdir -p ~/px4_ros2_setup/scripts
cd ~/px4_ros2_setup
````

Place the following file in this directory:

* `scripts/setup-xrce.sh`

---

## 2. Make Script Executable

```bash
chmod +x scripts/setup-xrce.sh
```


## 3. Install PX4 Autopilot

Follow the official PX4 documentation:

[https://docs.px4.io/main/en/dev_setup/dev_env_linux_ubuntu.html](https://docs.px4.io/main/en/dev_setup/dev_env_linux_ubuntu.html)

**Requirements:**

* Ubuntu 22.04
* Complete Gazebo + SITL setup

**Verification:**

```bash
cd ~/PX4-Autopilot
make px4_sitl
```

---

## 4. Install ROS 2 Humble

Follow the official ROS 2 documentation:

[https://docs.ros.org/en/humble/Installation.html](https://docs.ros.org/en/humble/Installation.html)

**Requirements:**

* Ubuntu 22.04
* Desktop installation

**Verification:**

```bash
source /opt/ros/humble/setup.bash
ros2 topic list
```

---

## 5. Micro XRCE-DDS Agent Setup

Run the setup script:

```bash
./scripts/setup-xrce.sh
```

**Functionality:**

* Clones and builds Micro XRCE-DDS Agent
* Installs DDS bridge for PX4–ROS2 communication

---

## 6. Verification

### XRCE Agent

```bash
MicroXRCEAgent udp4 -p 8888
```

---

## Notes

* Recommended OS: Ubuntu 22.04
* Always source ROS 2 before running ROS-based commands:

  ```bash
  source /opt/ros/humble/setup.bash
  ```
* A system reboot after installation is recommended

---

## System Capability After Setup

This setup enables:

* PX4 SITL simulation
* ROS 2 middleware integration
* DDS-based PX4–ROS communication

Applications:

* Offboard control
* Multi-vehicle simulation
* Sensor integration
* Custom autonomy pipelines

---

# 2. PX4 Custom Model Setup

Below are the files and folders to be placed inside `~/PX4-Autopilot` to enable the custom drone.

### Steps

1. Copy model files:

```bash
cp -r PX4-directories/models/* ~/PX4-Autopilot/Tools/simulation/gz/models/
```

2. Copy ROMFS airframe scripts:

```bash
cp -r PX4-directories/'ROMFS scripts'/* ~/PX4-Autopilot/ROMFS/px4fmu_common/init.d-posix/airframes/
```

3. Replace the `CMakeLists.txt` in the destination directory with the provided one.

---

### Build and Test

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500_lidar_depth_f #friendly
```
And

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500_lidar_depth_e #enemy
```

If it fails:

```bash
rm -rf build
make px4_sitl gz_x500_lidar_depth_e
```

---

# 3. ROS 2 Workspace Setup

## 3.1 Install ROS-Gazebo Harmonic Bridge

```bash
sudo apt update
sudo apt install ros-humble-ros-gzharmonic
```

---

## 3.2 Create Workspace

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

---

## 3.3 Clone Required Package

```bash
cd ~/ros2_ws/src
git clone https://github.com/PX4/px4_msgs.git
```

---

## 3.4 Add Custom Package

Copy the package provided in this repository (`Custom_ROS/*`) into:

```bash
cp -r Custom_ROS/* ~/ros2_ws/src/

```

## 3.5 Build Workspace

### IMP : Convert all the nodes inside the custom packages to executables using 

```bash
chmod +x {code.py}
```

The above step must be completed before building

```bash
cd ~/ros2_ws
colcon build --symlink-install
```

---

## 3.6 Source Workspace

```bash
source install/setup.bash
```

---

## 3.7 Launch

```bash
ros2 launch px4_multi_vehicle px4_multi_sim.launch.py
```

---

## Demo

The simulation must look like this
<img width="1919" height="1051" alt="image" src="https://github.com/user-attachments/assets/0d83838a-21b7-4006-a1df-da0c966c7ec8" />

## Validation
```bash
ros2 topic list
```
Enter the above command in the terminal to verify whether the topics are being published and the result must look like this:
```bash
/depth_camera/points
/parameter_events
/px4_1/fmu/in/actuator_motors
/px4_1/fmu/in/actuator_servos
/px4_1/fmu/in/arming_check_reply_v1
/px4_1/fmu/in/aux_global_position_v1
/px4_1/fmu/in/config_control_setpoints
/px4_1/fmu/in/config_overrides_request_v1
/px4_1/fmu/in/distance_sensor
/px4_1/fmu/in/fixed_wing_lateral_setpoint
/px4_1/fmu/in/fixed_wing_longitudinal_setpoint
/px4_1/fmu/in/goto_setpoint
/px4_1/fmu/in/landing_gear
/px4_1/fmu/in/lateral_control_configuration
/px4_1/fmu/in/longitudinal_control_configuration
/px4_1/fmu/in/manual_control_input
/px4_1/fmu/in/message_format_request
/px4_1/fmu/in/mode_completed
/px4_1/fmu/in/obstacle_distance
/px4_1/fmu/in/offboard_control_mode
/px4_1/fmu/in/onboard_computer_status
/px4_1/fmu/in/register_ext_component_request_v1
/px4_1/fmu/in/rover_attitude_setpoint
/px4_1/fmu/in/rover_position_setpoint
/px4_1/fmu/in/rover_rate_setpoint
/px4_1/fmu/in/rover_speed_setpoint
/px4_1/fmu/in/rover_steering_setpoint
/px4_1/fmu/in/rover_throttle_setpoint
/px4_1/fmu/in/sensor_optical_flow
/px4_1/fmu/in/telemetry_status
/px4_1/fmu/in/trajectory_setpoint
/px4_1/fmu/in/unregister_ext_component
/px4_1/fmu/in/vehicle_attitude_setpoint_v1
/px4_1/fmu/in/vehicle_command
/px4_1/fmu/in/vehicle_command_mode_executor
/px4_1/fmu/in/vehicle_mocap_odometry
/px4_1/fmu/in/vehicle_rates_setpoint
/px4_1/fmu/in/vehicle_thrust_setpoint
/px4_1/fmu/in/vehicle_torque_setpoint
/px4_1/fmu/in/vehicle_visual_odometry
/px4_1/fmu/out/airspeed_validated_v1
/px4_1/fmu/out/arming_check_request_v1
/px4_1/fmu/out/battery_status_v1
/px4_1/fmu/out/collision_constraints
/px4_1/fmu/out/estimator_status_flags
/px4_1/fmu/out/failsafe_flags
/px4_1/fmu/out/gimbal_device_attitude_status
/px4_1/fmu/out/home_position_v1
/px4_1/fmu/out/manual_control_setpoint
/px4_1/fmu/out/message_format_response
/px4_1/fmu/out/mode_completed
/px4_1/fmu/out/position_setpoint_triplet
/px4_1/fmu/out/register_ext_component_reply_v1
/px4_1/fmu/out/sensor_combined
/px4_1/fmu/out/timesync_status
/px4_1/fmu/out/transponder_report
/px4_1/fmu/out/vehicle_attitude
/px4_1/fmu/out/vehicle_command_ack_v1
/px4_1/fmu/out/vehicle_control_mode
/px4_1/fmu/out/vehicle_global_position
/px4_1/fmu/out/vehicle_gps_position
/px4_1/fmu/out/vehicle_land_detected
/px4_1/fmu/out/vehicle_local_position_v1
/px4_1/fmu/out/vehicle_odometry
/px4_1/fmu/out/vehicle_status_v2
/px4_1/fmu/out/vtol_vehicle_status
/px4_1/fmu/out/wind
/px4_2/fmu/in/actuator_motors
/px4_2/fmu/in/actuator_servos
/px4_2/fmu/in/arming_check_reply_v1
/px4_2/fmu/in/aux_global_position_v1
/px4_2/fmu/in/config_control_setpoints
/px4_2/fmu/in/config_overrides_request_v1
/px4_2/fmu/in/distance_sensor
/px4_2/fmu/in/fixed_wing_lateral_setpoint
/px4_2/fmu/in/fixed_wing_longitudinal_setpoint
/px4_2/fmu/in/goto_setpoint
/px4_2/fmu/in/landing_gear
/px4_2/fmu/in/lateral_control_configuration
/px4_2/fmu/in/longitudinal_control_configuration
/px4_2/fmu/in/manual_control_input
/px4_2/fmu/in/message_format_request
/px4_2/fmu/in/mode_completed
/px4_2/fmu/in/obstacle_distance
/px4_2/fmu/in/offboard_control_mode
/px4_2/fmu/in/onboard_computer_status
/px4_2/fmu/in/register_ext_component_request_v1
/px4_2/fmu/in/rover_attitude_setpoint
/px4_2/fmu/in/rover_position_setpoint
/px4_2/fmu/in/rover_rate_setpoint
/px4_2/fmu/in/rover_speed_setpoint
/px4_2/fmu/in/rover_steering_setpoint
/px4_2/fmu/in/rover_throttle_setpoint
/px4_2/fmu/in/sensor_optical_flow
/px4_2/fmu/in/telemetry_status
/px4_2/fmu/in/trajectory_setpoint
/px4_2/fmu/in/unregister_ext_component
/px4_2/fmu/in/vehicle_attitude_setpoint_v1
/px4_2/fmu/in/vehicle_command
/px4_2/fmu/in/vehicle_command_mode_executor
/px4_2/fmu/in/vehicle_mocap_odometry
/px4_2/fmu/in/vehicle_rates_setpoint
/px4_2/fmu/in/vehicle_thrust_setpoint
/px4_2/fmu/in/vehicle_torque_setpoint
/px4_2/fmu/in/vehicle_visual_odometry
/px4_2/fmu/out/airspeed_validated_v1
/px4_2/fmu/out/arming_check_request_v1
/px4_2/fmu/out/battery_status_v1
/px4_2/fmu/out/collision_constraints
/px4_2/fmu/out/estimator_status_flags
/px4_2/fmu/out/failsafe_flags
/px4_2/fmu/out/gimbal_device_attitude_status
/px4_2/fmu/out/home_position_v1
/px4_2/fmu/out/manual_control_setpoint
/px4_2/fmu/out/message_format_response
/px4_2/fmu/out/mode_completed
/px4_2/fmu/out/position_setpoint_triplet
/px4_2/fmu/out/register_ext_component_reply_v1
/px4_2/fmu/out/sensor_combined
/px4_2/fmu/out/timesync_status
/px4_2/fmu/out/transponder_report
/px4_2/fmu/out/vehicle_attitude
/px4_2/fmu/out/vehicle_command_ack_v1
/px4_2/fmu/out/vehicle_control_mode
/px4_2/fmu/out/vehicle_global_position
/px4_2/fmu/out/vehicle_gps_position
/px4_2/fmu/out/vehicle_land_detected
/px4_2/fmu/out/vehicle_local_position_v1
/px4_2/fmu/out/vehicle_odometry
/px4_2/fmu/out/vehicle_status_v2
/px4_2/fmu/out/vtol_vehicle_status
/px4_2/fmu/out/wind
/rosout
/world/default/model/x500_lidar_depth_e_2/link/camera_link/sensor/IMX214/camera_info
/world/default/model/x500_lidar_depth_e_2/link/camera_link/sensor/IMX214/image
/world/default/model/x500_lidar_depth_e_2/link/lidar_down_sensor_link/sensor/lidar_down/scan
/world/default/model/x500_lidar_depth_e_2/link/lidar_front_sensor_link/sensor/lidar_front/scan
/world/default/model/x500_lidar_depth_f_1/link/camera_link/sensor/IMX214/camera_info
/world/default/model/x500_lidar_depth_f_1/link/camera_link/sensor/IMX214/image
/world/default/model/x500_lidar_depth_f_1/link/lidar_down_sensor_link/sensor/lidar_down/scan
/world/default/model/x500_lidar_depth_f_1/link/lidar_front_sensor_link/sensor/lidar_front/scan
```'



