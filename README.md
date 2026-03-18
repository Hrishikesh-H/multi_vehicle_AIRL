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
make px4_sitl gz_x500_lidar_depth
```

If it fails:

```bash
rm -rf build
make px4_sitl gz_x500_lidar_depth
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

---

## 3.5 Build Workspace

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
<img width="1918" height="1056" alt="image" src="https://github.com/user-attachments/assets/f809713b-acfa-4079-a0f5-15c22c1e2a74" />


