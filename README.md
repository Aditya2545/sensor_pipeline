# Custom ROS 2 Sensor Pipeline

A production-style ROS 2 sensor data pipeline with custom messages,
moving-average filtering, CSV logging, unit tests, and CI/CD.

![CI](https://github.com/YOUR_USERNAME/sensor_pipeline/actions/workflows/ros2.yml/badge.svg)

## Demo

![Pipeline demo](media/pipeline_demo.gif)

## What it does

- Publishes simulated sensor data (temperature, humidity, pressure)
  on a custom `SensorReading.msg` type at configurable Hz
- Filters raw data using a moving average window — drops out-of-range readings
- Logs all filtered readings to a timestamped CSV file
- All parameters configurable from a single YAML file

## Tech stack

ROS 2 Humble · Python · Custom messages · rqt · pytest · GitHub Actions

## Setup

```bash
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
git clone https://github.com/YOUR_USERNAME/sensor_pipeline
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
ros2 launch sensor_pipeline pipeline.launch.py
```

## Monitor live data

```bash
ros2 topic echo /filtered_sensor
ros2 topic hz /raw_sensor
rqt
```

## Run tests

```bash
colcon test --packages-select sensor_pipeline
colcon test-result --verbose
```
