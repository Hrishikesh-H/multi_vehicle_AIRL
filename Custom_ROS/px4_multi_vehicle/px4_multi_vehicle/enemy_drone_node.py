import rclpy
from rclpy.node import Node

from px4_msgs.msg import VehicleOdometry


class EnemyDroneNode(Node):

    def __init__(self):
        super().__init__('enemy_drone_node')

        self.namespace = "/px4_2"

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

        self.get_logger().info("Enemy drone node started")

    def odom_callback(self, msg):

        x, y, z = msg.position

        # self.get_logger().info(
        #     f"Enemy position: x={x:.2f}, y={y:.2f}, z={z:.2f}"
        # )


def main(args=None):
    rclpy.init(args=args)
    node = EnemyDroneNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()