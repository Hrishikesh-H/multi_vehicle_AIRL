from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node


def generate_launch_description():

    # Micro XRCE-DDS Agent (PX4 ↔ ROS2 bridge)
    microxrce_agent = ExecuteProcess(
        cmd=[
            "MicroXRCEAgent", "udp4", "-p", "8888"
        ],
        output="screen"
    )

    # PX4 instance 1
    px4_1 = ExecuteProcess(
        cmd=[
            "bash", "-c",
            "cd ~/IISc_AIRL/PX4-Autopilot && "
            "PX4_SYS_AUTOSTART=4001 "
            "PX4_SIM_MODEL=gz_x500_lidar_depth_f "
            "./build/px4_sitl_default/bin/px4 -i 1"
        ],
        output="screen"
    )

    # PX4 instance 2
    px4_2 = ExecuteProcess(
        cmd=[
            "bash", "-c",
            "cd ~/IISc_AIRL/PX4-Autopilot && "
            "PX4_GZ_STANDALONE=1 "
            "PX4_SYS_AUTOSTART=4001 "
            "PX4_GZ_MODEL_POSE='0,10' "
            "PX4_SIM_MODEL=gz_x500_lidar_depth_e "
            "./build/px4_sitl_default/bin/px4 -i 2"
        ],
        output="screen"
    )

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            # Depth point cloud
            "/depth_camera/points@sensor_msgs/msg/PointCloud2@gz.msgs.PointCloudPacked",

            # Drone 1 camera
            "/world/default/model/x500_lidar_depth_f_1/link/camera_link/sensor/IMX214/image@sensor_msgs/msg/Image@gz.msgs.Image",
            "/world/default/model/x500_lidar_depth_f_1/link/camera_link/sensor/IMX214/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo",

            # Drone 1 lidar
            "/world/default/model/x500_lidar_depth_f_1/link/lidar_front_sensor_link/sensor/lidar_front/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan",
            "/world/default/model/x500_lidar_depth_f_1/link/lidar_down_sensor_link/sensor/lidar_down/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan",

            # Drone 2 camera
            "/world/default/model/x500_lidar_depth_e_2/link/camera_link/sensor/IMX214/image@sensor_msgs/msg/Image@gz.msgs.Image",
            "/world/default/model/x500_lidar_depth_e_2/link/camera_link/sensor/IMX214/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo",

            # Drone 2 lidar
            "/world/default/model/x500_lidar_depth_e_2/link/lidar_front_sensor_link/sensor/lidar_front/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan",
            "/world/default/model/x500_lidar_depth_e_2/link/lidar_down_sensor_link/sensor/lidar_down/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan",
        ],
        output="screen"
    )

    friendly_node = Node(
        package="px4_multi_vehicle",
        executable="friendly_node",
        output="screen"
    )

    enemy_node = Node(
        package="px4_multi_vehicle",
        executable="enemy_drone_node",
        output="screen"
    )

    return LaunchDescription([
        px4_1,
        px4_2,
        microxrce_agent,
        bridge,
        friendly_node,
        enemy_node
    ])