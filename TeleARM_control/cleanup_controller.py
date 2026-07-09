import rcply
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped

class CleanupController(Node):
    def __init__(self):
        super().__init__('cleanup_controller')
        self.publisher = self.create_publisher(TwistStamped, '/diff_drive_base_controller/cmd_vel', 10)
        self.timer = self.create_timer(0.05, self.publish_command)

    
    def publish_command(self):
        twist = TwistStamped()
        twist.header.stamp = self.get_clock().now().to_msg()
        twist.twist.linear.x = 0.5
        twist.twist.angular.z = 0.0
        self.publisher.publish(twist)
    

    def main(args=None):
        rclpy.init(args=args)
        node = DiffDriveBaseController()
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()