# Codex 调研记录：ROS2 虚拟机环境摸底与攻击链思路

## 1. 调研背景

本次调研的目标不是直接完成最终实验，而是先把远程虚拟机中的 `ROS2 + myCobot 280` 环境结构摸清楚，回答以下几个核心问题：

1. 当前 `test.launch.py` 启动出来的到底是什么；
2. 目前能否通过 ROS2 命令控制模型，而不是只能拖滑块；
3. 环境里是否存在更强的控制链路，例如 `MoveIt2 / trajectory / controller / 实机同步桥接`；
4. 在现有条件下，哪一条攻击链最容易落地。

---

## 2. 远程虚拟机接入情况

通过主机上的 `WSL Ubuntu-24.04` 和 `sshpass` 成功连接目标虚拟机：

- 远程地址：`what@192.168.29.129`
- 登录用户：`what`
- 远程主机名：`ubuntu`

连通性验证命令：

```bash
sshpass -p 123456 ssh -o StrictHostKeyChecking=no what@192.168.29.129 'echo connected && hostname && whoami'
```

验证结果：

- 可以正常登录；
- 可以远程执行命令；
- 后续可继续通过该方式检查 ROS2 环境与工作区文件。

---

## 3. 远端 ROS2 基本环境

远端虚拟机中安装的 ROS2 版本不是 `jazzy`，而是：

- `foxy`

远端工作区位置：

- `~/colcon_ws`

远端源码目录：

- `~/colcon_ws/src`

其中关键仓库为：

- `~/colcon_ws/src/mycobot_ros2`

---

## 4. 当前运行的 test.launch.py 到底是什么

用户本地已经验证可以通过：

```bash
ros2 launch mycobot_280 test.launch.py
```

启动一个带模型显示的 ROS2 环境。

进一步读取源码文件：

- `/home/what/colcon_ws/src/mycobot_ros2/mycobot_280/mycobot_280_arduino/launch/test.launch.py`

其核心逻辑非常明确，只包含以下节点：

1. `robot_state_publisher`
2. `joint_state_publisher` 或 `joint_state_publisher_gui`
3. `rviz2`

也就是说，当前 `test.launch.py` 的本质是：

**关节状态发布 + 模型姿态显示**

而不是：

- Gazebo 物理仿真；
- MoveIt 规划执行；
- ros2_control 控制器；
- 真实执行器控制链。

---

## 5. 当前运行态已验证的 ROS2 数据流

用户已在虚拟机中执行并确认：

```bash
ros2 topic list
ros2 topic list -t
ros2 topic type /joint_states
ros2 interface show sensor_msgs/msg/JointState
ros2 topic info /joint_states -v
```

观测结果表明：

- `/joint_states` 的消息类型是 `sensor_msgs/msg/JointState`
- 发布者是：`joint_state_publisher`
- 订阅者是：`robot_state_publisher`

因此当前数据流可以明确写成：

`joint_state_publisher -> /joint_states -> robot_state_publisher -> RViz`

这也和用户的实际观察一致：

- 当拖动 `Joint State Publisher GUI` 滑块时；
- `/joint_states` 的 `position` 会发生变化；
- RViz 中机械臂姿态同步变化。

---

## 6. 当前环境能说明什么，不能说明什么

### 能说明的内容

当前环境已经足够证明：

1. 机械臂模型已成功加载到 ROS2 + RViz 环境；
2. 机械臂关节名称、关节拓扑、姿态显示链路是通的；
3. `/joint_states` 是一个关键的可观察、可操纵话题；
4. 外部节点如果能够发布伪造的 `JointState`，就有机会影响模型姿态显示。

### 不能直接说明的内容

当前 `test.launch.py` 还不能直接说明：

1. 存在真实运动控制器；
2. 存在物理执行器级别的仿真；
3. 存在 Gazebo 中的动力学响应；
4. 已经可以通过 ROS2 对仿真机械臂执行真实轨迹控制。

因此，当前阶段最准确的表述应该是：

**已验证 ROS2 虚拟环境中的关节状态发布链路可被识别和分析，并能影响模型姿态显示。**

---

## 7. 远端工作区中发现的更强控制线索

虽然当前运行的是轻量显示 launch，但远端源码中还发现了以下关键包：

### 7.1 `mycobot_280_moveit2`

路径：

- `/home/what/colcon_ws/src/mycobot_ros2/mycobot_280/mycobot_280_moveit2`

其中包含：

- `launch/demo.launch.py`
- `launch/move_group.launch.py`
- `launch/moveit_rviz.launch.py`
- `launch/spawn_controllers.launch.py`
- `config/moveit_controllers.yaml`
- `config/ros2_controllers.yaml`

这说明环境中不仅有 RViz 模型显示，还预留了 **MoveIt2 + 控制器** 这条更完整的控制链。

### 7.2 `mycobot_280_moveit2_control`

路径：

- `/home/what/colcon_ws/src/mycobot_ros2/mycobot_280/mycobot_280_moveit2_control`

其中包含：

- `sync_plan.py`
- `sync_plan_arduino.py`

并且 `setup.py` 中已经定义了可执行入口：

- `sync_plan`
- `sync_plan_arduino`

这说明这里不是单纯的辅助代码，而是设计成可以直接运行的 ROS2 控制桥接脚本。

---

## 8. sync_plan_arduino.py 的关键含义

源码显示，`sync_plan_arduino.py` 的核心逻辑是：

1. 订阅 `joint_states`
2. 将 `joint_states` 中的弧度值转成角度值
3. 读取串口设备 `/dev/ttyUSB*` 或 `/dev/ttyACM*`
4. 使用 `pymycobot` 连接真实机械臂
5. 调用 `self.mc.send_angles(data_list, 35)` 将 ROS2 中的关节状态同步到实机

这件事非常重要。

它说明：

**在该项目代码设计里，`/joint_states` 不只是一个“显示模型姿态”的话题，它还可能成为“驱动真实机械臂动作”的桥接输入。**

换句话说，如果系统部署了该桥接脚本，那么伪造 `/joint_states` 的影响将不再局限于 RViz 显示，而是可能继续传导到真实机械臂。

---

## 9. MoveIt2 控制链的关键含义

在 `moveit_controllers.yaml` 中发现：

- 存在控制器：`arm_group_controller`
- 控制器类型：`FollowJointTrajectory`
- joints 包括：
  - `joint2_to_joint1`
  - `joint3_to_joint2`
  - `joint4_to_joint3`
  - `joint5_to_joint4`
  - `joint6_to_joint5`
  - `joint6output_to_joint6`

在 `ros2_controllers.yaml` 中进一步发现：

- `arm_group_controller` 类型为 `joint_trajectory_controller/JointTrajectoryController`
- 同时存在 `joint_state_broadcaster`

这说明：

**该工作区里实际上存在一套预配置的轨迹控制链，理论上可以从简单的 `/joint_states` 显示链，升级到 `FollowJointTrajectory` 这一层。**

因此，后续如果启动 `mycobot_280_moveit2 demo.launch.py` 成功，就有机会验证：

1. `MoveIt2` 是否能起来；
2. `follow_joint_trajectory` action 是否存在；
3. 能否通过轨迹控制接口驱动模型动作。

---

## 10. 当前最稳妥的攻击链思路

基于当前已经完成的验证和源码证据，现阶段最稳妥、最容易写进报告的一条攻击链是：

### 攻击链 A：关节状态注入导致显示层状态欺骗

1. 攻击者进入同一 ROS2 Domain 或可访问同一 ROS2 网络环境；
2. 通过 `ros2 topic list` 枚举系统话题；
3. 发现 `/joint_states`；
4. 通过 `ros2 topic type` 和 `ros2 interface show` 学会构造合法 `JointState` 消息；
5. 向 `/joint_states` 发布伪造关节状态；
6. `robot_state_publisher` 接收该状态并更新坐标变换；
7. RViz 中的机械臂姿态显示被攻击者篡改；
8. 造成操作员对机械臂当前状态的误判。

这条链的优点：

- 当前环境已经能验证前半段；
- 攻击路径短，证据留存容易；
- 不依赖更复杂的控制器或 Gazebo；
- 可以非常诚实地写成“状态欺骗 / 监控误导”风险。

### 攻击链 B：关节状态注入经桥接节点传导到实机

在源码层面，还存在更进一步的可能：

1. 攻击者伪造 `/joint_states`；
2. `sync_plan_arduino.py` 订阅该消息；
3. 桥接节点将弧度转换为角度；
4. 桥接节点通过 `pymycobot` 向串口实机发送角度控制命令；
5. 真实机械臂执行非预期姿态变化。

这条链更强，也更贴近“物理层影响”，但当前仍需后续补充验证：

- 是否成功运行 `sync_plan_arduino`；
- 是否完成实机串口连通；
- 是否能复现从 ROS2 消息到实机动作的闭环。

因此，现阶段比较安全的写法是：

**攻击链 A 作为已验证主链，攻击链 B 作为源码支持下的扩展链路与后续验证方向。**

---

## 11. 下一步建议

### 建议 1：先完成“命令行控制姿态”的最小实验

当前最优先的是，不再通过滑块，而是直接通过命令行向 `/joint_states` 发布消息，让模型姿态变化。

这一步一旦成功，就能把“仅会看 topic”升级成“能主动操纵 topic”。

建议实验目标：

1. 关闭或停用 GUI 发布者，避免和命令行发布打架；
2. 使用 `ros2 topic pub` 向 `/joint_states` 发送一组固定姿态；
3. 记录前后 RViz 截图；
4. 保存命令和对应消息内容。

### 建议 2：尝试启动 MoveIt2 demo

建议在远端虚拟机中进一步尝试：

```bash
source /opt/ros/foxy/setup.bash
source ~/colcon_ws/install/setup.bash
ros2 launch mycobot_280_moveit2 demo.launch.py
```

重点观察：

1. 是否能正常启动；
2. `ros2 action list` 中是否出现 `follow_joint_trajectory`；
3. `ros2 topic list` 中是否出现 trajectory/controller 相关接口；
4. 是否可以通过 MoveIt2 或 action 接口驱动机械臂模型。

### 建议 3：报告中先不要把当前环境写成“完整仿真控制系统”

更稳妥的表述应该分层：

1. 当前已验证：`JointState` 级别的显示链与可操纵性；
2. 当前已发现：MoveIt2 与 trajectory controller 的配置基础；
3. 当前待补充：真实轨迹控制实验与实机桥接验证。

这样报告会更真实，也更经得起答辩问询。

---

## 12. 当前阶段的结论

截至目前，可以形成如下阶段性结论：

1. 远端虚拟机中的 `mycobot_280 test.launch.py` 只是轻量级的 RViz 姿态显示链；
2. `/joint_states` 是该链路中的核心可观察、可注入话题；
3. 当前已经具备构造“状态欺骗”攻击链的实验基础；
4. 工作区中还存在 `MoveIt2` 与 `sync_plan_arduino` 等更强控制桥接能力；
5. 因此，本项目后续最合理的推进路径是：
   - 先完成 `/joint_states` 注入实验；
   - 再尝试 `MoveIt2/trajectory` 控制链；
   - 最后视实机联调情况决定是否扩展到“消息注入 -> 实机动作”的物理层攻击链。

---

# 13. `/joint_states` 注入实验：失败原因与成功原因整理

本节单独记录一次完整的排查过程，目的不是重复实验结论，而是说明：

1. 为什么最开始使用 `ros2 topic pub` 注入时失败；
2. 为什么后来改用 Python publisher 后成功；
3. 这说明攻击链真正成立的技术条件是什么。

这样做的意义在于，后续无论写报告、答辩还是复现实验，都可以直接引用这一节，而不必重新解释“为什么一开始明明 topic 在变，模型却不动”。

## 13.1 初始失败现象

最初的实验方式是直接使用命令行向 `/joint_states` 持续发布一组伪造关节状态，例如：

```bash
ros2 topic pub -r 10 /joint_states sensor_msgs/msg/JointState "{name: ['joint2_to_joint1', 'joint3_to_joint2', 'joint4_to_joint3', 'joint5_to_joint4', 'joint6_to_joint5', 'joint6output_to_joint6'], position: [0.4, -0.8, 0.9, -0.5, 0.3, 0.0], velocity: [], effort: []}"
```

当时观察到的现象是：

1. 终端中显示消息正在持续发布；
2. `ros2 topic info /joint_states -v` 表明确实存在一个发布者；
3. `ros2 topic echo /joint_states` 时，能看到 `position` 随注入消息发生变化；
4. 但是 RViz 中的机械臂模型姿态没有变化。

也就是说，当时已经可以确认：

- 伪造消息确实进入了 `/joint_states`；
- 关节名和消息字段也并非完全错误；
- 但“消息进入 topic”并没有自动等价于“模型姿态更新成功”。

## 13.2 失败时排除过的错误方向

在初始失败阶段，曾依次考虑过几种可能性：

### 1. 是否存在两个 publisher 打架

这是最先怀疑的原因，因为如果 `joint_state_publisher_gui` 仍在持续发布自己的关节状态，而攻击者同时用命令行发布 `/joint_states`，两者可能会互相覆盖。

但随后通过：

```bash
ros2 topic info /joint_states -v
```

观察到当时的发布者只有：

- `_ros2cli_xxxx`

订阅者只有：

- `robot_state_publisher`

因此可以排除“多个 publisher 冲突”是主要原因。

### 2. 是否 joint 名称写错

又进一步核对了实际启动的包和 URDF：

- 当前实际运行的是 `mycobot_280 test.launch.py`
- 对应模型是 `mycobot_280_m5.urdf`

其中定义的 6 个 revolute joint 名称为：

- `joint2_to_joint1`
- `joint3_to_joint2`
- `joint4_to_joint3`
- `joint5_to_joint4`
- `joint6_to_joint5`
- `joint6output_to_joint6`

而这与注入消息中使用的 `name` 完全一致。

因此可以排除“关节名写错”是主要原因。

### 3. 是否消息根本没发进去

通过监听 `/joint_states` 可以看到 `position` 确实已经变成注入值，因此也可以排除“消息没有发进去”。

综上，失败的根因必须位于更深一层，也就是：

**为什么 `robot_state_publisher` 没有把这组 JointState 进一步转化为 RViz 中可见的姿态变化。**

## 13.3 初始失败的真正关键点：时间戳

进一步观察 `ros2 topic pub` 打印出的消息内容，可以看到其中的 `header.stamp` 为：

- `sec = 0`
- `nanosec = 0`

也就是说，命令行直接构造的 `JointState` 使用的是一个零时间戳，而不是真正的当前时间。

与此同时，检查 `robot_state_publisher` 参数后发现：

- `ignore_timestamp = False`

这说明默认情况下，`robot_state_publisher` 会关心输入消息的时间戳合法性。

因此，当时即使：

1. `/joint_states` 中的 `position` 看上去已经被成功注入；
2. `robot_state_publisher` 也确实在订阅这个 topic；

依然有可能因为输入 `JointState` 的 `header.stamp` 为无效零值，而导致该状态无法形成正常、实时的 TF 更新链路，最终表现为：

**topic 在变，但 RViz 中的机械臂不动。**

通俗解释就是：

最开始的注入只是“把数字塞进了 JointState”，但没有把它变成“让显示系统信服的实时关节状态”。

## 13.4 为什么仅修改 ignore_timestamp 仍不足以解决问题

之后还尝试过：

```bash
ros2 param set /robot_state_publisher ignore_timestamp true
```

但是即使这样设置后，模型姿态仍然没有立即发生预期变化。

这说明：

- 单纯让 `robot_state_publisher` “不忽略时间戳问题”，并不等于系统就会自动把零时间戳消息当成高质量实时状态来处理；
- 更本质的问题仍然在于：
  **攻击者必须构造一条真正像“当前时刻 JointState”那样的合法消息。**

也就是说，`ignore_timestamp` 的修改最多只是辅助排查手段，不适合当作最终实验成立的关键条件。

## 13.5 成功复现的关键改动

后续将注入方式从：

- `ros2 topic pub`

改成了：

- 使用 Python 编写一个 ROS2 publisher 节点

其核心改动只有一个，但非常关键：

```python
msg.header.stamp = self.get_clock().now().to_msg()
```

也就是在每次发布伪造 `JointState` 时，显式填入**当前系统时间戳**。

在这一改动之后，实验现象发生了根本变化：

1. `/joint_states` 依旧收到伪造的 `position`；
2. `robot_state_publisher` 开始据此更新姿态；
3. RViz 中的机械臂模型成功发生明显变化；
4. 攻击链 A 得以真正跑通。

## 13.6 成功复现的技术原因总结

这次成功的关键不在于“Python 比命令行更强”，而在于：

**Python publisher 允许攻击者构造一个时间戳有效、格式完整、语义上更接近真实运行状态的 `JointState` 消息。**

因此，从技术上看，本次成功说明了以下几点：

1. `/joint_states` 确实可以被外部节点伪造发布；
2. 仅仅伪造 `position` 数组还不够；
3. 要让显示链接受并生效，攻击消息还必须满足更完整的消息合法性条件；
4. 其中最关键的一项就是：`header.stamp` 必须反映当前时刻，而不能长期为零。

## 13.7 对攻击链 A 的修正版表述

经过这次实验后，攻击链 A 的写法应当比原先更严谨。

原先容易写成：

1. 枚举 `/joint_states`
2. 构造 `JointState`
3. 发布消息
4. RViz 姿态被篡改

但更准确的版本应该是：

1. 攻击者进入同一 ROS2 Domain 或网络环境；
2. 枚举并识别关键话题 `/joint_states`；
3. 分析其消息类型为 `sensor_msgs/msg/JointState`；
4. 按照系统当前关节名称和消息格式，构造合法的伪造 `JointState`；
5. 为伪造消息填充有效的当前时间戳；
6. 持续发布该关节状态；
7. `robot_state_publisher` 接收后更新 TF；
8. RViz 中机械臂姿态显示被攻击者成功篡改。

这才是本次实验真正复现出来的完整攻击步骤。

## 13.8 对报告写作的启示

这次实验还有一个很值得写进报告的方法论意义：

**ROS2 环境中的安全实验不能只停留在“能发 topic 消息”这一层，而必须关注消息在目标节点语义上的可接受性。**

也就是说：

- 从“发送消息”到“系统采纳消息”之间，仍然存在一层隐含条件；
- 这些条件可能包括：
  - 时间戳是否有效；
  - 消息字段是否完整；
  - 关节名称是否匹配；
  - QoS 和更新时序是否合理。

本次实验就是一个非常典型的例子：

- 初始失败并不是攻击方向错了；
- 而是注入消息还不够“像真的”；
- 当消息足够接近真实运行状态时，攻击链才真正成立。

## 13.9 当前可直接引用的结论

基于这轮排查与复现，可以形成如下可直接引用的结论：

1. 在 `mycobot_280 test.launch.py` 启动的 ROS2 虚拟环境中，外部节点能够向 `/joint_states` 注入伪造关节状态；
2. 若仅使用 `ros2 topic pub` 直接发送零时间戳消息，虽然 topic 内容发生变化，但 RViz 中姿态未必会更新；
3. 当攻击者构造带有效当前时间戳的 `JointState` 消息后，`robot_state_publisher` 会接受该状态并更新姿态显示；
4. 因此，攻击链 A 的真正成立条件不是“能发消息”，而是“能构造一条语义上足够真实的 JointState 消息”；
5. 该实验最终成功证明：ROS2 中的 `/joint_states` 话题可被利用来实施显示层状态欺骗。

## 13.10 竞争性 Publisher 并存时的状态振荡现象

在后续实验中，又观察到一个比“单次状态欺骗”更值得记录的现象：

- 上午运行攻击脚本时，曾忘记关闭原先的 `GUI publisher`；
- 结果导致**正常 publisher** 与**攻击者 publisher** 同时向 `/joint_states` 发布消息；
- 在攻击脚本进入最终阶段 `attacker-defined pose locked` 之后，RViz 中的机械臂模型并没有稳定保持在攻击者指定姿态，而是在：
  - `safe_pose`
  - `end_pose`

之间反复切换。

### 现象说明

这一现象说明，当前 ROS2 显示链路中：

1. `/joint_states` 允许多个 publisher 同时存在；
2. `robot_state_publisher` 作为订阅者，并不会区分“哪一个 publisher 才是权威输入源”；
3. 它只会持续接收并处理先后到达的 JointState 消息；
4. 因此当两个不同姿态源并存时，最终表现出来的是：
   **状态竞争（state competition）或状态振荡（state oscillation）**

而不是某一方天然拥有独占控制权。

### 这不是“线程锁问题”

这个现象很容易让人第一反应想到“是不是应该加锁”，但更准确地说：

- 这不是单进程内共享变量竞争的问题；
- 也不是传统意义上的线程同步问题；
- 它本质上是一个**分布式消息系统中的多源输入竞争问题**。

也就是说，问题不在于缺少 mutex，而在于：

**系统将同一 topic 上来自不同节点、但格式合法的消息视为等价输入，却缺少对消息源身份和优先级的鉴别机制。**

### 风险含义

这个现象意味着，当前环境的风险不仅仅是：

- 攻击者可以“单次伪造状态”；

而且还包括：

- 攻击者可以与正常发布者并存；
- 通过持续注入制造状态竞争；
- 导致显示层姿态来回跳变、不稳定、不可预测。

因此，这一观察可以被提炼为一条扩展风险：

**未授权竞争性 publisher 注入可导致系统状态振荡。**

### 与攻击链 A 的关系

如果说前面的攻击链 A 是：

`未授权 /joint_states 注入 -> 显示层状态欺骗`

那么这一现象对应的就是攻击链 A 的扩展版本：

`正常 publisher 与恶意 publisher 并存 -> /joint_states 状态竞争 -> 显示层姿态振荡/不稳定`

这条链与原始攻击链的区别在于：

1. 原始攻击链更强调“攻击者能否成功改变显示状态”；
2. 扩展链更强调“即使攻击者不能长期独占，也仍可通过持续注入破坏系统稳定性”。

### 为什么这个现象值得写进报告

这个现象有两个非常重要的研究价值：

#### 1. 它暴露了系统缺乏“单一权威状态源”设计

正常情况下，像 `/joint_states` 这样的关键状态话题，应该尽量有明确的权威来源，或者下游节点至少知道“谁才是可信输入源”。

但当前环境中，系统显然默认认为：

- 只要 topic 名称对；
- 消息类型对；
- 字段格式对；

那么任何节点都可以成为“状态提供者”。

这在多节点、开放网络、或者多机械臂部署场景中是非常脆弱的。

#### 2. 它说明攻击者即使不能完全夺取控制权，也能制造不稳定

安全风险不一定总表现为“完全接管”。

在很多实际系统里，攻击者只要能够：

- 持续干扰状态流；
- 让显示层、监控层、甚至下游控制层读到来回跳变的数据；

就已经足以造成：

- 操作员误判；
- 上层逻辑紊乱；
- 系统行为不稳定。

因此，从安全分析角度看：

**状态竞争本身就是一种攻击效果，不必等到“完全独占控制”才算攻击成立。**

### 如果下游继续信任 `/joint_states`，风险会进一步放大

结合前文已经分析过的 `sync_plan_arduino.py`：

- 该桥接脚本会订阅 `/joint_states`
- 然后直接把 JointState 转换成实机角度命令

这意味着，如果未来系统中真的运行了类似桥接节点，那么这种竞争性 publisher 注入的影响就可能从：

- 显示层姿态振荡

进一步扩展为：

- 实机接收交替姿态指令
- 控制层不稳定
- 甚至物理动作异常抖动

目前这一点还没有实机闭环验证，因此应保持严谨表述：

**当前实验已验证显示层状态振荡；若下游执行层继续信任该话题，则同类问题可能进一步扩展为控制层不稳定甚至物理层异常动作。**

### 对防护思路的启示

这一现象也说明，防护措施不应简单理解为“加并发锁”，而应从 ROS2 分布式系统设计层面考虑，包括但不限于：

1. 不要把 `/joint_states` 直接当作控制输入；
2. 为关键控制链设计单一权威输入源；
3. 对多机械臂系统做命名空间隔离；
4. 做 ROS Domain / 网络隔离；
5. 引入节点认证、访问控制、SROS2 / DDS Security；
6. 在下游增加输入源白名单、仲裁机制或合理性检查。

### 可直接引用的结论

基于该观察，可形成如下简洁结论：

1. 在当前 ROS2 虚拟环境中，`/joint_states` 允许多个 publisher 并存；
2. 当正常 publisher 与攻击者 publisher 同时存在时，`robot_state_publisher` 不会区分消息源可信度；
3. 系统会因竞争性 JointState 注入而出现姿态振荡；
4. 这说明系统不仅存在状态欺骗风险，还存在状态竞争与稳定性破坏风险；
5. 若下游节点继续信任该话题，风险还有可能从显示层扩展到控制层。

## 14. XSB 结项阶段可补充执行的命令

参考中期 `reference/code/instruction.md` 里的用法，结项阶段的 XSB 部分不建议只停留在“跑出 `yes`”，而应该补出两层内容：

1. 直接查询：证明规则确实能推出目标结论；
2. `spy` 跟踪：证明这些结论是沿着什么推理链一步步得到的。

这样做的好处是，最后答辩时可以同时展示：

- 规则文件已经成功装载；
- 关键攻击结论可以被查询得到；
- 推理路径不是“拍脑袋解释”，而是能在 XSB 调试视图里看到的。

### 14.1 基础装载与核心查询

如果在 `~/XSB/bin` 目录下运行，并且已经把文件拷贝或改名为 `joint.xsb`，可以直接执行：

```bash
./xsb
['joint.xsb'].
misleadPoseDisplay(attacker_host, mycobot_vm).
oscillatingPoseDisplay(attacker_host, mycobot_vm).
physicalLayerRisk(attacker_host, mycobot_vm).
policyViolation(attacker_host, Action, Resource).
halt.
```

如果不改名，而是直接使用结项文件原名，则把第一条改成：

```prolog
['mycobot_jointstate_attack.xsb'].
```

这一组命令的作用分别是：

1. `misleadPoseDisplay(attacker_host, mycobot_vm).`
   用于证明“伪造 `/joint_states` 可导致 RViz 姿态显示被误导”。
2. `oscillatingPoseDisplay(attacker_host, mycobot_vm).`
   用于证明“正常 publisher 与恶意 publisher 并存时会导致状态振荡”。
3. `physicalLayerRisk(attacker_host, mycobot_vm).`
   用于证明“如果下游桥接节点继续信任 `/joint_states`，风险可以继续向物理层传导”。
4. `policyViolation(attacker_host, Action, Resource).`
   用于统一收口，展示该攻击最终落在什么策略违规上。

### 14.2 中间能力链查询

为了让 XSB 部分不只停留在最终结论，还可以补查中间推理节点：

```bash
./xsb
['joint.xsb'].
enumerateTopic(attacker_host, mycobot_vm, Topic).
learnMessageSchema(attacker_host, joint_states_topic).
forgeValidJointState(attacker_host, joint_states_topic).
injectForgedJointState(attacker_host, mycobot_vm, joint_states_topic).
tamperTFStream(attacker_host, mycobot_vm).
competingPublisherState(attacker_host, mycobot_vm, joint_states_topic).
propagateToBridge(attacker_host, mycobot_vm).
halt.
```

这一组命令的意义是把整条链拆开验证：

1. `enumerateTopic/3`
   证明攻击者先具备 ROS2 域内的话题枚举能力。
2. `learnMessageSchema/2`
   证明攻击者不仅看到了 topic，还掌握了消息类型和格式。
3. `forgeValidJointState/2`
   证明攻击者具备构造“合法 JointState”的条件，而不是只能乱发数据。
4. `injectForgedJointState/3`
   证明真正的攻击动作已经成立。
5. `tamperTFStream/2`
   证明攻击并不是停留在 topic 层，而是进一步影响了 TF 更新链。
6. `competingPublisherState/3`
   证明竞争性 publisher 的前提条件已经满足。
7. `propagateToBridge/2`
   证明如果桥接节点存在，则风险还可以继续往下游传播。

这组查询很适合写进报告的“推理过程”或“攻击路径分解”部分。

### 14.3 用 `spy` 展示显示层欺骗的推理路径

中期的 `instruction.md` 已经说明了 `spy(...)`、`notrace.`、`halt.` 这一套调试方式。结项阶段最值得补的第一条调试链是显示层欺骗：

```bash
./xsb
['joint.xsb'].
spy(injectForgedJointState/3).
spy(tamperTFStream/2).
spy(misleadPoseDisplay/2).
misleadPoseDisplay(attacker_host, mycobot_vm).
notrace.
halt.
```

这组命令的作用是把如下逻辑明确展示出来：

`可达 ROS2 域 -> 可枚举 topic -> 可构造合法 JointState -> 可注入 /joint_states -> robot_state_publisher 更新 TF -> RViz 显示被误导`

如果答辩时需要一个“最像中期风格”的 XSB 演示，这一组最合适。

### 14.4 用 `spy` 展示竞争性 publisher 状态振荡

为了对应你这次新发现的“safe_pose 和 end_pose 来回切换”现象，可以专门补一条竞争状态链：

```bash
./xsb
['joint.xsb'].
spy(competingPublisherState/3).
spy(oscillatingPoseDisplay/2).
oscillatingPoseDisplay(attacker_host, mycobot_vm).
notrace.
halt.
```

这一组命令的作用是：

1. 展示“正常 publisher + 恶意 publisher 并存”这一前提被规则识别到；
2. 展示规则如何把它进一步推到“姿态振荡/状态不稳定”的结论上。

这部分很适合补足报告里“为什么这不是普通显示错误，而是系统稳定性风险”的论证。

### 14.5 用 `spy` 展示向物理层传播的潜在风险

如果你想把 `sync_plan_arduino` 这条源码证据也体现在 XSB 操作上，可以再补：

```bash
./xsb
['joint.xsb'].
spy(propagateToBridge/2).
spy(physicalLayerRisk/2).
physicalLayerRisk(attacker_host, mycobot_vm).
notrace.
halt.
```

它的意义不是证明“实机已经被控制”，而是证明：

- 在规则层面，攻击并不一定止步于 RViz；
- 只要存在信任 `/joint_states` 的桥接节点，风险就具备继续向控制层/物理层传播的条件。

这和前面实验部分的边界说明是匹配的：

- 实验上，当前已验证显示层攻击；
- 推理上，当前已证明存在向下游扩展的条件。

### 14.6 结项阶段最值得保留的 XSB 演示顺序

如果时间有限，不必把所有命令都演示一遍。最推荐保留下面三组：

#### 方案 A：核心结论

```bash
./xsb
['joint.xsb'].
misleadPoseDisplay(attacker_host, mycobot_vm).
oscillatingPoseDisplay(attacker_host, mycobot_vm).
policyViolation(attacker_host, Action, Resource).
halt.
```

用于快速展示“能推出什么结论”。

#### 方案 B：显示层欺骗推理链

```bash
./xsb
['joint.xsb'].
spy(injectForgedJointState/3).
spy(tamperTFStream/2).
spy(misleadPoseDisplay/2).
misleadPoseDisplay(attacker_host, mycobot_vm).
notrace.
halt.
```

用于展示“为什么这个结论成立”。

#### 方案 C：竞争性 publisher 扩展链

```bash
./xsb
['joint.xsb'].
spy(competingPublisherState/3).
spy(oscillatingPoseDisplay/2).
oscillatingPoseDisplay(attacker_host, mycobot_vm).
notrace.
halt.
```

用于展示“这次结项相比中期新增了什么更有研究味道的内容”。

### 14.7 建议写法

如果后面要把 XSB 结果写进报告或答辩稿，可以按下面这个口径概括：

1. 基础查询证明了 `/joint_states` 伪造、竞争性 publisher 振荡、以及向物理层传播风险都能在规则层面推出。
2. `spy` 调试结果进一步展示了这些结论的推理链并非人工解释，而是由事实与规则自动联结得到。
3. 因此，XSB 部分不仅复用了中期的推理框架，还完成了从“传统攻击图示例”到“ROS2 机械臂消息注入场景”的迁移。

## 15. 防护对照实验：先在 XSB 里证明“原理上能拦住”，再考虑代码落地

当前最适合补的一组增强实验，不是继续扩攻击链，而是做一个**防护对照**：

1. 在当前未防护版本里，`misleadPoseDisplay(...)` 和 `oscillatingPoseDisplay(...)` 都能成立；
2. 在加入防护假设之后，这两个结论应当不再成立；
3. 这样可以说明：  
   现有攻击链之所以成立，不只是因为“攻击者很强”，更是因为系统确实缺少关键的认证、授权或输入仲裁机制。

这里要分清两层：

- `XSB` 负责证明“什么样的防护原理上能把攻击链截断”；
- 代码修改负责真正把这种防护机制落实到 ROS2 节点和话题处理逻辑里。

本节只整理**如何改**，不动任何代码。

### 15.1 在 XSB 里怎么改，才能做出“防护后攻击失效”的对照

当前结项版 `xsb` 中，攻击链能成立的关键事实之一是：

```prolog
noTopicAuth(mycobot_vm, joint_states_topic).
noPublisherACL(mycobot_vm, joint_states_topic).
```

这两句的含义分别是：

1. 该 topic 没有来源认证；
2. 该 topic 没有 publisher 访问控制。

而你现在的注入规则是：

```prolog
injectForgedJointState(AttackerHost, Vm, Topic) :-
    forgeValidJointState(AttackerHost, Topic),
    rosTopic(Vm, Topic),
    noTopicAuth(Vm, Topic),
    noPublisherACL(Vm, Topic).
```

这说明只要攻击者会伪造合法 `JointState`，并且系统又没有认证/ACL，这条注入链就会成立。

#### 做法 A：最小改法，直接去掉“无防护”事实

最简单的防护对照方式，就是复制一份新的规则文件，例如：

```text
mycobot_jointstate_defended.xsb
```

然后在新文件里：

1. 删除或注释掉这两句：

```prolog
noTopicAuth(mycobot_vm, joint_states_topic).
noPublisherACL(mycobot_vm, joint_states_topic).
```

2. 新增对应的“已防护”事实，例如：

```prolog
topicAuthEnabled(mycobot_vm, joint_states_topic).
publisherACLEnabled(mycobot_vm, joint_states_topic).
```

这一步本身还不会自动改变查询结果，因为你当前规则只看 `noTopicAuth` 和 `noPublisherACL`。  
但只要上面两条“不安全事实”被移除，`injectForgedJointState(...)` 就失去成立条件，后面的：

- `tamperTFStream(...)`
- `misleadPoseDisplay(...)`
- `propagateToBridge(...)`
- `physicalLayerRisk(...)`

都会跟着断掉。

然后你可以直接跑：

```prolog
?- misleadPoseDisplay(attacker_host, mycobot_vm).
?- oscillatingPoseDisplay(attacker_host, mycobot_vm).
?- physicalLayerRisk(attacker_host, mycobot_vm).
```

预期结果应该变成：

- 不再返回 `yes`
- 而是查询失败

这就构成了一组很清楚的对照实验：

- 未防护版：攻击成立
- 防护假设版：攻击链被截断

#### 做法 B：更规范的改法，把“防护条件”显式写进规则

如果你希望报告里显得更清楚，可以再进一步，把规则写成“攻击链在什么条件下才成立”。

例如把：

```prolog
injectForgedJointState(AttackerHost, Vm, Topic) :-
    forgeValidJointState(AttackerHost, Topic),
    rosTopic(Vm, Topic),
    noTopicAuth(Vm, Topic),
    noPublisherACL(Vm, Topic).
```

保留不变，同时再新增一组“防护导致失败”的解释性规则，例如：

```prolog
blockedInjectionByAuth(Vm, Topic) :-
    topicAuthEnabled(Vm, Topic).

blockedInjectionByACL(Vm, Topic) :-
    publisherACLEnabled(Vm, Topic).
```

然后再增加一个辅助查询，例如：

```prolog
defenseEffective(Vm, Topic) :-
    blockedInjectionByAuth(Vm, Topic).

defenseEffective(Vm, Topic) :-
    blockedInjectionByACL(Vm, Topic).
```

这样后面你除了查询“攻击不成立”，还能显式查询：

```prolog
?- defenseEffective(mycobot_vm, joint_states_topic).
```

它的意义是：

- 不只是看攻击链失败；
- 还可以给出“失败是因为哪种防护生效了”。

这个版本更适合写报告，因为解释会更直接。

#### 做法 C：针对竞争性 publisher，单独加“单一权威源”约束

`oscillatingPoseDisplay(...)` 这条链目前成立，核心在于：

```prolog
competingPublisherState(AttackerHost, Vm, Topic) :-
    legitimatePublisher(_, Topic),
    maliciousPublisher(AttackerHost, Topic),
    rosTopic(Vm, Topic),
    noTopicAuth(Vm, Topic),
    noPublisherACL(Vm, Topic).
```

如果你想专门模拟“系统只接受一个权威 publisher”，可以在防护版里新增：

```prolog
singleAuthoritativePublisher(joint_states_topic, joint_state_publisher_gui).
```

再把 `competingPublisherState/3` 改成更严格的版本，例如要求：

- 只有当 topic 没有权威源约束时，竞争状态才成立。

思路上可以改成：

```prolog
noSingleAuthority(Topic).

competingPublisherState(AttackerHost, Vm, Topic) :-
    legitimatePublisher(_, Topic),
    maliciousPublisher(AttackerHost, Topic),
    rosTopic(Vm, Topic),
    noTopicAuth(Vm, Topic),
    noPublisherACL(Vm, Topic),
    noSingleAuthority(Topic).
```

这样防护版只要不再声明 `noSingleAuthority(joint_states_topic).`，而改成：

```prolog
singleAuthoritativePublisher(joint_states_topic, joint_state_publisher_gui).
```

那么：

```prolog
?- oscillatingPoseDisplay(attacker_host, mycobot_vm).
```

理论上也会断掉。

这组修改对应的安全思想是：

- 不是简单“禁止所有 publisher”；
- 而是系统必须知道谁才是唯一可信的权威状态源。

### 15.2 建议你实际做一个什么样的 XSB 对照实验

如果追求最省事、最适合结项阶段，我建议你只做两份文件：

1. `mycobot_jointstate_attack.xsb`
   代表当前未防护版本
2. `mycobot_jointstate_defended.xsb`
   代表加入认证/ACL/单一权威源假设后的防护版本

然后各跑一次下面这些查询：

```prolog
?- misleadPoseDisplay(attacker_host, mycobot_vm).
?- oscillatingPoseDisplay(attacker_host, mycobot_vm).
?- physicalLayerRisk(attacker_host, mycobot_vm).
?- policyViolation(attacker_host, Action, Resource).
```

预期叙述可以写成：

1. 未防护模型中，上述攻击查询均可成立；
2. 在引入 topic 认证、publisher ACL 或单一权威 publisher 假设后，相关攻击链不再可达；
3. 说明这些防护机制在规则层面具备阻断当前攻击链的理论有效性。

这已经足够构成一组很像样的“防护前/防护后”对照实验。

### 15.3 如果真要在代码层落地，应该改哪里

这一部分不要求你现在就实现，但需要在报告里说明：  
**XSB 只能证明“原理上有效”，真正落地还得回到 ROS2 节点与控制链实现中。**

针对你当前这个项目，最值得改的不是 RViz，而是这些位置：

#### 位置 1：所有直接信任 `/joint_states` 的下游节点

你当前场景里最关键的风险点是：

- `robot_state_publisher` 从 `/joint_states` 派生 TF；
- `sync_plan_arduino.py` 订阅 `/joint_states` 后直接转成实机角度命令。

其中真正更危险的是第二类，也就是：

**任何把 `/joint_states` 当成控制输入的节点。**

如果后面要改代码防护，第一优先级应该是：

- 不要让下游控制节点“只要收到 JointState 就信”；
- 必须先验证消息来源是否来自预期节点。

#### 位置 2：桥接节点 `sync_plan_arduino.py`

如果要做最小可实现的代码防护，这个文件是最值得改的。

因为它当前的设计逻辑本质上是：

- 订阅 `/joint_states`
- 收到就转角度
- 然后 `send_angles(...)`

这意味着它默认把 `/joint_states` 当成可信控制源。

如果要改，方向应该是：

1. **不要直接订阅通用 `/joint_states` 作为执行输入**
   更合理的是单独定义一个更明确的控制 topic，例如：
   - `/trusted_joint_command`
   - `/arm_controller_command`

2. **限制允许发送该控制 topic 的节点**
   也就是让控制输入源和普通状态广播源分开。

3. **在桥接节点内部做白名单校验**
   即使消息进来了，也先检查：
   - 是否来自预期 namespace；
   - 是否符合预期发布频率；
   - 是否符合预期 joint 名称集合；
   - 是否存在异常跳变；
   - 是否带有效时间戳。

4. **加入输入仲裁逻辑**
   如果系统中可能同时存在 GUI、仿真器、脚本等多个来源，那么桥接层必须决定：
   - 只认一个来源；
   - 或者不同模式下只开启某一种来源。

#### 位置 3：话题命名和系统结构本身

你现在的风险不只是某一行代码写错，而是结构上混用了“状态反馈”和“控制输入”。

因此更合理的代码层改法是：

1. `/joint_states`
   只保留为状态反馈
2. `/joint_command` 或 `/trajectory_command`
   单独作为控制输入
3. 桥接节点只消费控制输入，不消费通用状态反馈

这样一来，攻击者就不能只靠伪造状态反馈 topic 来驱动执行层。

这是结构性修复，比简单加判断更根本。

### 15.4 如果在 ROS2 层进一步做正式防护，应该考虑什么机制

如果你不是只做项目演示，而是真的做系统防护，代码之外还应该配合这些机制：

#### 1. SROS2 / DDS Security

这是最标准的方向，对应你在规则里写的：

- `topicAuthEnabled(...)`
- `publisherACLEnabled(...)`

现实里它们可以通过：

- 节点身份认证
- 证书
- topic 级访问控制策略

来实现。

也就是说，规则中的“topic 认证”和“publisher ACL”并不是空想，而是能映射到 ROS2 安全栈的。

#### 2. Namespace 隔离

如果多台机械臂都在同一网络里，至少应该把它们分成：

- `/arm1/joint_states`
- `/arm2/joint_states`

而不是共用一套裸露的全局 topic。

这不能完全解决恶意 publisher 问题，但能显著降低“串台”和误注入的概率。

#### 3. 单一权威源设计

从工程上看，这往往比“所有消息都签名”更重要。

系统必须明确：

- 谁是唯一合法的状态源；
- 谁是唯一合法的控制源；
- 谁只能看，不能发；
- 谁可以发，但只能发某一类 topic。

否则系统即使形式上是分布式的，实际上也是“谁都能抢话筒”。

### 15.5 建议如何写进报告

如果后面要把这部分写进结项报告，可以按下面这个结构组织：

1. **规则层防护对照**
   在 XSB 模型中引入 topic 认证、publisher ACL 和单一权威 publisher 假设后，原有攻击链不再成立。

2. **工程层含义**
   说明这些规则并非抽象设定，而是分别对应 ROS2 系统中的认证、授权、命名隔离和控制链拆分机制。

3. **实现建议**
   优先改造 `sync_plan_arduino.py` 这类直接信任 `/joint_states` 的桥接节点，将状态反馈和控制输入解耦。

4. **边界说明**
   本阶段仅完成了规则层防护有效性的对照分析，尚未在代码层完成完整改造与复验。

### 15.6 最后判断

如果你现在时间有限，那么最划算的顺序是：

1. 先做 XSB 防护前/防护后对照；
2. 再在报告里写出“如果落到代码层，最应该改哪些节点、改什么逻辑”；
3. 不必现在真的去改 ROS2 代码，也不必为了防护实验再把工程线拉得过长。

这样你最后就能形成一个比较完整的闭环：

- 已证明攻击能成立；
- 已证明为什么成立；
- 已证明加入哪类防护后，规则层会断链；
- 已说明如果要真正落地，应当修改哪些代码位置与系统结构。
