# ⚙️ Environment Setup

This section provides the **core setup pipeline** for:
- PX4 Autopilot (SITL)
- ROS 2 Humble
- Micro XRCE-DDS Agent (PX4 ↔ ROS2 bridge)

---

## 📁 Step 1 — Create Setup Directory

Create a dedicated folder:

```bash
mkdir -p ~/px4_ros2_setup
cd ~/px4_ros2_setup
````

Place the following file in this directory:

* `3-setup-xrce.sh`

---

## ▶️ Step 2 — Make Script Executable

```bash
chmod +x 3-setup-xrce.sh
```

---

## 🚀 Step 3 — Install PX4 Autopilot (Official Method)

Install PX4 using the official documentation:

👉 [https://docs.px4.io/main/en/dev_setup/dev_env_linux_ubuntu.html](https://docs.px4.io/main/en/dev_setup/dev_env_linux_ubuntu.html)

**Requirements:**

* Ubuntu 22.04
* Follow the **Gazebo + SITL** setup instructions

After installation, verify:

```bash
cd ~/PX4-Autopilot
make px4_sitl
```

---

## 🚀 Step 4 — Install ROS 2 Humble (Official Method)

Install ROS 2 Humble using the official guide:

👉 [https://docs.ros.org/en/humble/Installation.html](https://docs.ros.org/en/humble/Installation.html)

**Requirements:**

* Ubuntu 22.04
* Follow the *Desktop Install* instructions

After installation, verify:

```bash
source /opt/ros/humble/setup.bash
ros2 topic list
```

---

## 🚀 Step 5 — Micro XRCE-DDS Agent Setup

Run the setup script:

```bash
./3-setup-xrce.sh
```

**What it does:**

* Clones and builds Micro XRCE-DDS Agent
* Installs DDS bridge for PX4–ROS2 communication

---

## ✅ Verification

### XRCE Agent

```bash
MicroXRCEAgent udp4 -p 8888
```

---

## 📌 Notes

* Recommended OS: **Ubuntu 22.04**
* Ensure ROS 2 is sourced before running ROS-related commands:

  ```bash
  source /opt/ros/humble/setup.bash
  ```
* Reboot after installation to avoid environment issues

---

## 🔧 What This Setup Enables

This setup provides:

* PX4 SITL simulation environment
* ROS 2 middleware integration
* DDS bridge for real-time communication

This is required for:

* Offboard control
* Multi-vehicle simulation
* Sensor integration
* Custom autonomy algorithms

---

## ➡️ Next Steps

Proceed with:

* ROS 2 workspace setup (`colcon`)
* PX4–ROS2 interface configuration
* Multi-vehicle simulation setup

```
```
