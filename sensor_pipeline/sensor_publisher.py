#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_pipeline.msg import SensorReading
import random
import math

class SensorPublisher(Node):
    def __init__(self):
        super().__init__('sensor_publisher')

        # Declare parameters — these can be overridden from launch file
        self.declare_parameter('publish_rate', 2.0)
        self.declare_parameter('sensor_id', 'sensor_001')
        self.declare_parameter('add_noise', True)

        rate = self.get_parameter('publish_rate').value
        self.sensor_id = self.get_parameter('sensor_id').value
        self.add_noise = self.get_parameter('add_noise').value

        self.publisher_ = self.create_publisher(SensorReading, '/raw_sensor', 10)
        self.timer = self.create_timer(1.0 / rate, self.publish_reading)

        self.tick = 0.0
        self.get_logger().info(
            f'Sensor publisher started — ID: {self.sensor_id}, rate: {rate} Hz')

    def publish_reading(self):
        msg = SensorReading()
        msg.stamp = self.get_clock().now().to_msg()
        msg.sensor_id = self.sensor_id

        # Simulate realistic sensor data with a sine wave base + optional noise
        base_temp     = 22.0 + 5.0 * math.sin(self.tick * 0.1)
        base_humidity = 55.0 + 10.0 * math.cos(self.tick * 0.08)
        base_pressure = 1013.25 + 2.0 * math.sin(self.tick * 0.05)

        if self.add_noise:
            msg.temperature = base_temp     + random.gauss(0, 0.5)
            msg.humidity    = base_humidity + random.gauss(0, 1.0)
            msg.pressure    = base_pressure + random.gauss(0, 0.3)
        else:
            msg.temperature = base_temp
            msg.humidity    = base_humidity
            msg.pressure    = base_pressure

        # Determine sensor status based on thresholds
        if msg.temperature > 30.0:
            msg.status = 'WARNING_HIGH_TEMP'
        elif msg.temperature < 10.0:
            msg.status = 'WARNING_LOW_TEMP'
        else:
            msg.status = 'OK'

        self.publisher_.publish(msg)
        self.tick += 1.0

        self.get_logger().debug(
            f'Published: temp={msg.temperature:.2f} '
            f'hum={msg.humidity:.2f} status={msg.status}')

def main(args=None):
    rclpy.init(args=args)
    node = SensorPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
