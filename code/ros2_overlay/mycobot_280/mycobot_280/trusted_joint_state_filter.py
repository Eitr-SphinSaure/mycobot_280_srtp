from sensor_msgs.msg import JointState

import rclpy
from rclpy.node import Node

from mycobot_280.joint_state_security import (
    validate_joint_state_message,
    validate_single_publisher,
)


class TrustedJointStateFilter(Node):
    def __init__(self):
        super().__init__("trusted_joint_state_filter")
        self.declare_parameter("raw_topic", "_joint_states_authorized_source")
        self.declare_parameter("trusted_topic", "_joint_states_trusted")
        self.declare_parameter("max_message_age_seconds", 0.5)
        self.declare_parameter("enforce_single_publisher", True)

        self.raw_topic = self.get_parameter("raw_topic").get_parameter_value().string_value
        self.trusted_topic = self.get_parameter("trusted_topic").get_parameter_value().string_value
        self.max_message_age_seconds = (
            self.get_parameter("max_message_age_seconds").get_parameter_value().double_value
        )
        self.enforce_single_publisher = (
            self.get_parameter("enforce_single_publisher").get_parameter_value().bool_value
        )

        self.publisher = self.create_publisher(JointState, self.trusted_topic, 10)
        self.subscription = self.create_subscription(
            JointState,
            self.raw_topic,
            self.listener_callback,
            10,
        )

        self.get_logger().info(
            f"trusted filter enabled: raw_topic={self.raw_topic}, trusted_topic={self.trusted_topic}, "
            f"single_publisher={self.enforce_single_publisher}, max_age={self.max_message_age_seconds:.3f}s"
        )

    def listener_callback(self, msg: JointState):
        if self.enforce_single_publisher:
            ok, reason = validate_single_publisher(self, self.raw_topic)
            if not ok:
                self.get_logger().warn(f"drop raw JointState: {reason}")
                return

        ok, reason = validate_joint_state_message(
            msg,
            self.get_clock().now().nanoseconds,
            self.max_message_age_seconds,
        )
        if not ok:
            self.get_logger().warn(f"drop raw JointState: {reason}")
            return

        trusted_msg = JointState()
        trusted_msg.header = msg.header
        trusted_msg.name = list(msg.name)
        trusted_msg.position = list(msg.position)
        trusted_msg.velocity = list(msg.velocity)
        trusted_msg.effort = list(msg.effort)
        self.publisher.publish(trusted_msg)


def main(args=None):
    rclpy.init(args=args)
    node = TrustedJointStateFilter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
