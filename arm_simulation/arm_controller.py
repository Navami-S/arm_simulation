import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray

class ArmController(Node):
    def __init__(self):
        super().__init__('arm_controller')

        self.publisher = self.create_publisher(JointState, '/joint_states', 10)

        self.subscription = self.create_subscription(
            Float64MultiArray,
            '/arm_angles',
            self.arm_angles_callback,
            10
        )
        self.get_logger().info('Simulation node started! Waiting for /arm_angles...')

    def arm_angles_callback(self, msg):
        angles = list(msg.data)
        self.get_logger().info(f'Received angles: {angles}')

        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5']
        joint_state.position = angles

        self.publisher.publish(joint_state)

def main(args=None):
    rclpy.init(args=args)
    node = ArmController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()