from sensor_msgs.msg import JointState

EXPECTED_JOINT_NAMES = [
    "joint2_to_joint1",
    "joint3_to_joint2",
    "joint4_to_joint3",
    "joint5_to_joint4",
    "joint6_to_joint5",
    "joint6output_to_joint6",
]

JOINT_LIMITS = {
    "joint2_to_joint1": (-2.9322, 2.9322),
    "joint3_to_joint2": (-2.3562, 2.3562),
    "joint4_to_joint3": (-2.6180, 2.6180),
    "joint5_to_joint4": (-2.5307, 2.5307),
    "joint6_to_joint5": (-2.8798, 2.8798),
    "joint6output_to_joint6": (-3.14159, 3.14159),
}


def validate_single_publisher(node, topic_name: str):
    publisher_count = node.count_publishers(topic_name)
    if publisher_count != 1:
        return False, f"expected exactly 1 publisher on {topic_name}, found {publisher_count}"
    return True, "ok"


def validate_joint_state_message(msg: JointState, now_nanoseconds: int, max_age_seconds: float = 0.5):
    if len(msg.name) != len(EXPECTED_JOINT_NAMES):
        return False, "unexpected joint count"

    if len(msg.position) != len(msg.name):
        return False, "joint_names and positions size mismatch"

    if set(msg.name) != set(EXPECTED_JOINT_NAMES):
        return False, "unexpected joint name set"

    stamp_ns = msg.header.stamp.sec * 1_000_000_000 + msg.header.stamp.nanosec
    if stamp_ns == 0:
        return False, "zero timestamp is not allowed"

    age_ns = now_nanoseconds - stamp_ns
    max_age_ns = int(max_age_seconds * 1_000_000_000)
    if age_ns < 0:
        return False, "future timestamp is not allowed"
    if age_ns > max_age_ns:
        return False, f"stale message age {age_ns / 1_000_000_000:.3f}s exceeds {max_age_seconds:.3f}s"

    joint_state_dict = {name: msg.position[i] for i, name in enumerate(msg.name)}
    for joint_name in EXPECTED_JOINT_NAMES:
        lower, upper = JOINT_LIMITS[joint_name]
        value = joint_state_dict[joint_name]
        if value < lower or value > upper:
            return False, f"{joint_name} out of range: {value:.4f} not in [{lower:.4f}, {upper:.4f}]"

    return True, "ok"
