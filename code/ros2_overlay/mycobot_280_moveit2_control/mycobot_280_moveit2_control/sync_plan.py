import math
import os
import time

import pymycobot
import rclpy
from packaging import version
from pymycobot.mycobot import MyCobot
from rclpy.node import Node
from sensor_msgs.msg import JointState

from mycobot_280_moveit2_control.joint_state_security import (
    EXPECTED_JOINT_NAMES,
    validate_joint_state_message,
    validate_single_publisher,
)

# min low version require
MAX_REQUIRE_VERSION = '3.5.3'

current_verison = pymycobot.__version__
print('current pymycobot library version: {}'.format(current_verison))
if version.parse(current_verison) > version.parse(MAX_REQUIRE_VERSION):
    raise RuntimeError(
        'The version of pymycobot library must be less than {} . '
        'The current version is {}. Please downgrade the library version.'.format(
            MAX_REQUIRE_VERSION, current_verison
        )
    )
else:
    print('pymycobot library version meets the requirements!')


class Slider_Subscriber(Node):
    def __init__(self):
        super().__init__("control_sync_plan")
        self.declare_parameter("trusted_topic", "_joint_states_trusted")
        self.trusted_topic = self.get_parameter("trusted_topic").get_parameter_value().string_value

        self.subscription = self.create_subscription(
            JointState,
            self.trusted_topic,
            self.listener_callback,
            10
        )
        self.subscription

        self.robot_m5 = os.popen("ls /dev/ttyUSB*").readline()[:-1]
        self.robot_wio = os.popen("ls /dev/ttyACM*").readline()[:-1]
        if self.robot_m5:
            port = self.robot_m5
        else:
            port = self.robot_wio
        self.get_logger().info("port:%s, baud:%d" % (port, 115200))
        self.mc = MyCobot(port, 115200)
        time.sleep(0.05)
        if self.mc.get_fresh_mode() == 0:
            self.mc.set_fresh_mode(1)
            time.sleep(0.05)

        self.rviz_order = EXPECTED_JOINT_NAMES

    def listener_callback(self, msg):
        ok, reason = validate_single_publisher(self, self.trusted_topic)
        if not ok:
            self.get_logger().warn(f"reject JointState: {reason}")
            return

        ok, reason = validate_joint_state_message(msg, self.get_clock().now().nanoseconds)
        if not ok:
            self.get_logger().warn(f"reject JointState: {reason}")
            return

        joint_state_dict = {name: msg.position[i] for i, name in enumerate(msg.name)}
        data_list = []
        for joint in self.rviz_order:
            if joint in joint_state_dict:
                radians_to_angles = round(math.degrees(joint_state_dict[joint]), 3)
                data_list.append(radians_to_angles)

        if len(data_list) != len(self.rviz_order):
            self.get_logger().warn("reject JointState: incomplete joint list after reordering")
            return

        print('data_list: {}'.format(data_list))
        self.mc.send_angles(data_list, 35)


def main(args=None):
    rclpy.init(args=args)
    slider_subscriber = Slider_Subscriber()

    rclpy.spin(slider_subscriber)

    slider_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
