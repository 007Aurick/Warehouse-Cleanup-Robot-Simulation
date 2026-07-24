#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import LaserScan


class DiffDrivePublisher(Node):
    def __init__(self):
        super().__init__('diff_drive_publisher')
        self.publisher = self.create_publisher(
            TwistStamped,
            '/diff_drive_base_controller/cmd_vel',
            10,
        )
        self.subscriber = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        self.latest_scan = None
        self.timer = self.create_timer(0.05, self.publish_command)
        self.ticks = 0
        self.state = 'forward'
        self.obstacle_threshold = 1.5   # meters
        self.forward_speed = 0.1
        self.reverse_speed = -0.2
        self.turn_speed = 0.5
        self.backup_ticks = 20          # ~1.0s at 0.05s timer
        self.turn_ticks = 63   

        

    def scan_callback(self, msg):
        self.latest_scan = msg

    def get_front_distance(self):
        # No scan yet → treat as "unknown / far" (or blocked if you prefer)
        if self.latest_scan is None:
            return float('inf')

        n = len(self.latest_scan.ranges)
        center = n // 2
        window = 15
        front_ranges = self.latest_scan.ranges[center - window:center + window]
        front_ranges = [
            r for r in front_ranges
            if r > 0.0 and r != float('inf')
        ]
        return min(front_ranges) if front_ranges else float('inf')


    def publish_command(self):
        lin, ang = 0.0, 0.0
        front_distance = self.get_front_distance()

        if self.state == 'forward':
            if front_distance > self.obstacle_threshold:
                lin,ang = self.forward_speed, 0.0
            else:
                self.state = 'reverse'
                self.ticks = 0
        elif self.state == 'reverse':
            lin,ang = self.reverse_speed, 0.0
            self.ticks += 1
            if self.ticks >= self.backup_ticks:
                self.state = 'turn'
                self.ticks = 0
        elif self.state == 'turn':
            lin,ang = 0.0, self.turn_speed
            self.ticks += 1
            if self.ticks >= self.turn_ticks:
                self.state = 'forward'
                self.ticks = 0
           

        command = TwistStamped()
        command.header.stamp = self.get_clock().now().to_msg()
        command.twist.linear.x = lin
        command.twist.angular.z = ang
        self.publisher.publish(command)


def main(args=None):
    rclpy.init(args=args)
    node = DiffDrivePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
