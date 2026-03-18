import rclpy
from rclpy.node import Node

from px4_msgs.msg import VehicleOdometry
from px4_msgs.msg import OffboardControlMode
from px4_msgs.msg import TrajectorySetpoint
from px4_msgs.msg import VehicleCommand

from sensor_msgs.msg import Image, LaserScan


class FriendlyDroneNode(Node):

    def __init__(self):
        super().__init__('friendly_drone_node')

        self.namespace = "/px4_1"

        qos = rclpy.qos.QoSProfile(
            depth=10,
            reliability=rclpy.qos.ReliabilityPolicy.BEST_EFFORT,
            durability=rclpy.qos.DurabilityPolicy.VOLATILE
        )

        # PX4 subscriptions
        self.odom_sub = self.create_subscription(
            VehicleOdometry,
            self.namespace + "/fmu/out/vehicle_odometry",
            self.odom_callback,
            qos
        )

        # Sensor subscriptions (ADDED)
        self.camera_sub = self.create_subscription(
            Image,
            "/world/default/model/x500_lidar_depth_1/link/camera_link/sensor/IMX214/image",
            self.camera_callback,
            10
        )

        self.lidar_front_sub = self.create_subscription(
            LaserScan,
            "/world/default/model/x500_lidar_depth_1/link/lidar_front_sensor_link/sensor/lidar_front/scan",
            self.lidar_front_callback,
            10
        )

        self.lidar_down_sub = self.create_subscription(
            LaserScan,
            "/world/default/model/x500_lidar_depth_1/link/lidar_down_sensor_link/sensor/lidar_down/scan",
            self.lidar_down_callback,
            10
        )

        # PX4 publishers
        self.offboard_pub = self.create_publisher(
            OffboardControlMode,
            self.namespace + "/fmu/in/offboard_control_mode",
            10
        )

        self.traj_pub = self.create_publisher(
            TrajectorySetpoint,
            self.namespace + "/fmu/in/trajectory_setpoint",
            10
        )

        self.cmd_pub = self.create_publisher(
            VehicleCommand,
            self.namespace + "/fmu/in/vehicle_command",
            10
        )

        self.timer = self.create_timer(0.1, self.control_loop)

        # State variables
        self.position = None
        self.lidar_front = None
        self.lidar_down = None
        self.last_image = None

        self.offboard_counter = 0
        self.armed = False
        self.offboard_enabled = False

        self.get_logger().info("Friendly drone node started")

    # ===================== CALLBACKS =====================

    def odom_callback(self, msg):
        self.position = msg.position

    def camera_callback(self, msg):
        self.last_image = msg

    def lidar_front_callback(self, msg):
        self.lidar_front = msg

    def lidar_down_callback(self, msg):
        self.lidar_down = msg

    # ===================== PX4 COMMANDS =====================

    def arm(self):
        msg = VehicleCommand()
        msg.command = VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM
        msg.param1 = 1.0
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True
        msg.timestamp = self.get_clock().now().nanoseconds // 1000
        self.cmd_pub.publish(msg)

    def set_offboard_mode(self):
        msg = VehicleCommand()
        msg.command = VehicleCommand.VEHICLE_CMD_DO_SET_MODE
        msg.param1 = 1.0  # custom mode
        msg.param2 = 6.0  # OFFBOARD
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True
        msg.timestamp = self.get_clock().now().nanoseconds // 1000
        self.cmd_pub.publish(msg)

    # ===================== CONTROL LOOP =====================

    def control_loop(self):

        if self.position is None:
            return

        timestamp = self.get_clock().now().nanoseconds // 1000

        # Publish offboard heartbeat
        offboard = OffboardControlMode()
        offboard.position = True
        offboard.timestamp = timestamp
        self.offboard_pub.publish(offboard)

        # Send trajectory setpoint
        traj = TrajectorySetpoint()
        traj.position = [0.0, 0.0, -5.0]
        traj.timestamp = timestamp
        self.traj_pub.publish(traj)

        # PX4 requires few setpoints before switching
        if self.offboard_counter < 20:
            self.offboard_counter += 1
            return

        # Enable OFFBOARD mode
        if not self.offboard_enabled:
            self.set_offboard_mode()
            self.offboard_enabled = True
            self.get_logger().info("Switched to OFFBOARD mode")
            return

        # Arm the drone
        if not self.armed:
            self.arm()
            self.armed = True
            self.get_logger().info("Drone armed")
            return


def main(args=None):
    rclpy.init(args=args)
    node = FriendlyDroneNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()