#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2023 University of Leeds
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import rclpy
import board
import busio
import adafruit_icm20x
from rclpy.node import Node
import time

from sensor_msgs.msg import Imu
from sensor_msgs.msg import Temperature
from sensor_msgs.msg import MagneticField

PUBLISH_RATE = 200  # per second
PUBLISH_INTERVAL_S = 1 / PUBLISH_RATE
SLOW_PUBLISH_INTERVAL_S = 1.0

i2c_bus0=(busio.I2C(board.SCL_1, board.SDA_1))

icm = adafruit_icm20x.ICM20948(i2c_bus0, 0x68)

class ImuNode(Node):
    def __init__(self):
        # Initialise the Node.
        super().__init__("imu_icm20948")
        self.get_logger().info("IMU has started!")
        # Set up Publishers
        self.imu_raw_publisher_ = self.create_publisher(Imu, "imu/data_raw", 10)
        self.imu_mag_publisher_ = self.create_publisher(MagneticField, "imu/mag", 10)
        # Timers.
        self.data_timer_ = self.create_timer(PUBLISH_INTERVAL_S, self._publish_all)

    def _setup_imu(self):
        """
        Set up the IMU.
        Note: Most of the default settings are fine but this is provided so that
        the user can change settings if they want to.
        """
        # Set the accelerometer range
        icm.accelerometer_range = AccelRange.RANGE_4G

        # Set sample rate to max
        icm.accelerometer_data_rate = 1125
        
        # Set the gyro DPS setting
        icm.gyro_range = GyroRange.RANGE_500_DPS

        # Set the gyro rate max
        icm.gyro_data_rate = 1100
        pass
    
    def _publish_all(self):
        # Get all readings.
        self._publish_raw()
        self._publish_magnetic()

    def _publish_raw(self):
        msg = Imu()
        # Note: raw gyroscope data is reported in degrees per second.
        ax, ay, az = icm.acceleration
        vx, vy, vz = icm.gyro
	
        msg.angular_velocity.x = float(vx)
        msg.angular_velocity.y = float(vy)
        msg.angular_velocity.z = float(vz)
        # Note: raw acceleration is reported in degrees per second.
        msg.linear_acceleration.x = float(ax)
        msg.linear_acceleration.y = float(ay)
        msg.linear_acceleration.z = float(az)
        msg.header.frame_id = "robot_imu"
        msg.header.stamp = self.get_clock().now().to_msg() 
        # Publish the message.
        self.imu_raw_publisher_.publish(msg)

    def _publish_magnetic(self):
        msg = MagneticField()
        x, y, z = icm.magnetic
        # Convert from micro-Teslas to Teslas.
        msg.magnetic_field.x = float(x) / 1000.0
        msg.magnetic_field.y = float(y) / 1000.0
        msg.magnetic_field.z = float(z) / 1000.0
        # Publish the message.
        msg.header.frame_id = "robot_mag"
        msg.header.stamp = self.get_clock().now().to_msg()
        self.imu_mag_publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ImuNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()


if __name__ == "__main__":
    main()
