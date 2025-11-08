# ROS 2 driver for ICM20948 IMU

This ROS 2 driver of the ICM20948 implements a ROS2 wrapper around the Adafruit ICM20X library: https://github.com/adafruit/Adafruit_CircuitPython_ICM20X/tree/main

## ROS Interfaces

This implementation has one node, `imu_icm20948`, that publishes on the following data:

| Message | Topic | Default Rate |
|:--|:--|:--|
| [sensor_msgs/msg/Imu](https://docs.ros2.org/latest/api/sensor_msgs/msg/Imu.html) | "imu/data_raw" | 200 Hz |
| [sensor_msgs/msg/MagneticField](https://docs.ros2.org/latest/api/sensor_msgs/msg/MagneticField.html) | "imu/mag" | 200 Hz |
| [sensor_msgs/msg/Temperature](https://docs.ros2.org/latest/api/sensor_msgs/msg/Temperature.html) | "imu/temp" | 1 Hz |

Note: If you need a position estimate (Quaternion), the package `[IMU tools for ROS](https://github.com/CCNYRoboticsLab/imu_tools/tree/humble)` should be installed and launched.  Two filters are provided, Madgwick and complimentary (recommended).

## Installation on the Jetson Nano/TX2/Xavier

Prerequisite: You willd need ROS2 Humble installed natively (via yocto meta-tegrademo) or in a docker container.  

Run the following (if not native, you can add these dependencies to your docker file -just remove the sudo prefix):

```bash
sudo pip3 install adafruit-circuitpython-icm20x
sudo apt install i2c-tools
```

## Configuration ##
Connect the IMU to the I2C-0 bus on the Jetson 40 pin gpio (we assume i2c bus 0 for this driver)

```bash
sudo i2cdetect -y 0
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```
Bus permissions (access I2C buses without `sudo`) .
```bash
sudo adduser $USER dialout
```
Log out and in again.  Verify that `i2cdetect -y 0` works without `sudo``.

**Note: If using certain boards where pullups are weak, this driver may only run if the bus clock speed on the jetson has been reduced to 100khz**
```
vi /sys/bus/i2c/devices/i2c-0/bus_clk_rate
```
Change 400000 to 100000

## Clone and Build ##
Create a local ros2 workspace overlay, clone this repo into the src folder (e.g. ~/ros_ws/src), and colcon build

## Run the node ##

```
ros2 run icm20948_ros2 imu_node
```

Example of orientation covariance visualization using imu tools Madgwick filter:
https://youtu.be/U9o7lGz_AtM

## Acknowledgements

**This repo is forked from https://github.com/RealRobotics/icm20948-ros2 with some modifications to use the adafruit library**

&copy; 2023 University of Leeds.

The author, A. Blight, asserts his moral rights.
