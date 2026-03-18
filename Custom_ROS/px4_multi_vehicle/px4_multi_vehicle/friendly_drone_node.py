import rclpy
from rclpy.node import Node

from px4_msgs.msg import VehicleOdometry
from px4_msgs.msg import OffboardControlMode
from px4_msgs.msg import TrajectorySetpoint
from px4_msgs.msg import VehicleCommand


class FriendlyDroneNode(Node):

    def __init__(self):
        super().__init__('friendly_drone_node')

        self.namespace = "/px4_1"

        qos = rclpy.qos.QoSProfile(
            depth=10,
            reliability=rclpy.qos.ReliabilityPolicy.BEST_EFFORT,
            durability=rclpy.qos.DurabilityPolicy.VOLATILE
        )

        self.odom_sub = self.create_subscription(
            VehicleOdometry,
            self.namespace + "/fmu/out/vehicle_odometry",
            self.odom_callback,
            qos
        )

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

        self.get_logger().info("Friendly drone node started")

    def odom_callback(self, msg):
        self.position = msg.position

    def control_loop(self):

        offboard = OffboardControlMode()
        offboard.position = True
        offboard.timestamp = self.get_clock().now().nanoseconds // 1000
        self.offboard_pub.publish(offboard)

        traj = TrajectorySetpoint()
        traj.position = [0.0, 0.0, -5.0]
        traj.timestamp = offboard.timestamp

        self.traj_pub.publish(traj)


def main(args=None):
    rclpy.init(args=args)
    node = FriendlyDroneNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()