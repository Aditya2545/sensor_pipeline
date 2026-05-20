#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_pipeline.msg import SensorReading
import csv
import os
from datetime import datetime

class DataLogger(Node):
    def __init__(self):
        super().__init__('data_logger')

        self.declare_parameter('log_dir', os.path.expanduser('~/sensor_logs'))
        self.declare_parameter('log_interval', 1.0)

        log_dir = os.path.expanduser(self.get_parameter('log_dir').value)
	os.makedirs(log_dir, exist_ok=True)

        # Create a new CSV file with a timestamp in the name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_path = os.path.join(log_dir, f'sensor_{timestamp}.csv')

        with open(self.log_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'ros_time', 'sensor_id',
                'temperature', 'humidity', 'pressure', 'status'
            ])

        self.sub = self.create_subscription(
            SensorReading, '/filtered_sensor', self.log_callback, 10)

        self.count = 0
        self.get_logger().info(f'Data logger started — writing to {self.log_path}')

    def log_callback(self, msg):
        ros_time = f"{msg.stamp.sec}.{msg.stamp.nanosec:09d}"
        with open(self.log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                ros_time,
                msg.sensor_id,
                f'{msg.temperature:.4f}',
                f'{msg.humidity:.4f}',
                f'{msg.pressure:.4f}',
                msg.status
            ])
        self.count += 1
        if self.count % 10 == 0:
            self.get_logger().info(f'Logged {self.count} readings to {self.log_path}')

def main(args=None):
    rclpy.init(args=args)
    node = DataLogger()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
