from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg = get_package_share_directory('sensor_pipeline')
    params = os.path.join(pkg, 'config', 'pipeline_params.yaml')

    return LaunchDescription([
        Node(
            package='sensor_pipeline',
            executable='sensor_publisher.py',
            name='sensor_publisher',
            output='screen',
            parameters=[params]
        ),
        Node(
            package='sensor_pipeline',
            executable='sensor_filter.py',
            name='sensor_filter',
            output='screen',
            parameters=[params]
        ),
        Node(
            package='sensor_pipeline',
            executable='data_logger.py',
            name='data_logger',
            output='screen',
            parameters=[params]
        ),
    ])
