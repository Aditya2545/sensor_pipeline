#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_pipeline.msg import SensorReading
from collections import deque

class SensorFilter(Node):
    def __init__(self):
        super().__init__('sensor_filter')

        # Declare parameters
        self.declare_parameter('window_size', 5)
        self.declare_parameter('temp_min', -10.0)
        self.declare_parameter('temp_max', 60.0)
        self.declare_parameter('humidity_min', 0.0)
        self.declare_parameter('humidity_max', 100.0)

        window = self.get_parameter('window_size').value
        self.temp_min    = self.get_parameter('temp_min').value
        self.temp_max    = self.get_parameter('temp_max').value
        self.humid_min   = self.get_parameter('humidity_min').value
        self.humid_max   = self.get_parameter('humidity_max').value

        # Rolling windows for moving average
        self.temp_window  = deque(maxlen=window)
        self.humid_window = deque(maxlen=window)
        self.pres_window  = deque(maxlen=window)

        self.sub = self.create_subscription(
            SensorReading, '/raw_sensor', self.filter_callback, 10)
        self.pub = self.create_publisher(
            SensorReading, '/filtered_sensor', 10)

        self.dropped = 0
        self.passed  = 0

        self.get_logger().info(
            f'Sensor filter started — window size: {window}')

    def filter_callback(self, msg):
        # Step 1: Validate — drop out-of-range readings
        if not (self.temp_min <= msg.temperature <= self.temp_max):
            self.dropped += 1
            self.get_logger().warn(
                f'Dropped reading — temperature {msg.temperature:.2f} out of range')
            return

        if not (self.humid_min <= msg.humidity <= self.humid_max):
            self.dropped += 1
            self.get_logger().warn(
                f'Dropped reading — humidity {msg.humidity:.2f} out of range')
            return

        # Step 2: Add to rolling windows
        self.temp_window.append(msg.temperature)
        self.humid_window.append(msg.humidity)
        self.pres_window.append(msg.pressure)

        # Step 3: Publish smoothed message
        filtered = SensorReading()
        filtered.stamp     = msg.stamp
        filtered.sensor_id = msg.sensor_id
        filtered.temperature = sum(self.temp_window)  / len(self.temp_window)
        filtered.humidity    = sum(self.humid_window) / len(self.humid_window)
        filtered.pressure    = sum(self.pres_window)  / len(self.pres_window)
        filtered.status      = msg.status

        self.pub.publish(filtered)
        self.passed += 1

        self.get_logger().debug(
            f'Filtered: temp={filtered.temperature:.2f} '
            f'(passed={self.passed} dropped={self.dropped})')

def main(args=None):
    rclpy.init(args=args)
    node = SensorFilter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
