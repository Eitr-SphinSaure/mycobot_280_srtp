当前目录下有两个pdf，分别是我们项目的开题和中期答辩。简要说一下当前形势：我在中期复现了一个简单的MULVAL，并拿到了机械臂实机，但还没有setup起来。除此之外，我还有一台完整的虚拟机可以仿真运行。今天是5月7日，我们要在5月12日前提交一份报告，在5月15日下午答辩。请你先读一下这里的两份slides，然后给我拟定一份为期五天的研究计划

what@ubuntu:~/colcon_ws$ ifconfig
ens33: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.29.129  netmask 255.255.255.0  broadcast 192.168.29.255
        inet6 fe80::7500:725e:10d2:72b6  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:3b:4b:26  txqueuelen 1000  (Ethernet)
        RX packets 208  bytes 66664 (66.6 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2965  bytes 870993 (870.9 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 3230  bytes 861128 (861.1 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 3230  bytes 861128 (861.1 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0


ssh what@192.168.29.129
123456
plink -P 22 -pw 123456 what@192.168.29.129

sshpass 


name:
- joint2_to_joint1
- joint3_to_joint2
- joint4_to_joint3
- joint5_to_joint4
- joint6_to_joint5
- joint6output_to_joint6
position:
- -2.9322~2.9322
- -2.3562~2.3562
- -2.618~2.618
- -2.5307~2.5307
- -2.8798~2.8798
- -3.14159~3.14159

name:
- joint2_to_joint1
- joint3_to_joint2
- joint4_to_joint3
- joint5_to_joint4
- joint6_to_joint5
- joint6output_to_joint6
position:
- 2.9322
- 2.3562
- 2.618
- 2.5307
- 2.8798
- 3.14159

```bash
what@ubuntu:~/colcon_ws$ ros2 launch mycobot_280_moveit2 demo.launch.py
[INFO] [launch]: All log files can be found below /home/what/.ros/log/2026-05-09-06-41-03-308243-ubuntu-2142
[INFO] [launch]: Default logging verbosity is set to INFO
Task exception was never retrieved
future: <Task finished name='Task-2' coro=<LaunchService._process_one_event() done, defined at /opt/ros/foxy/lib/python3.8/site-packages/launch/launch_service.py:226> exception=InvalidLaunchFileError('py')>
Traceback (most recent call last):
  File "/opt/ros/foxy/lib/python3.8/site-packages/launch/launch_description_sources/any_launch_file_utilities.py", line 53, in get_launch_description_from_any_launch_file
    return loader(launch_file_path)
  File "/opt/ros/foxy/lib/python3.8/site-packages/launch/launch_description_sources/python_launch_file_utilities.py", line 62, in get_launch_description_from_python_launch_file
    launch_file_module = load_python_launch_file_as_module(python_launch_file_path)
  File "/opt/ros/foxy/lib/python3.8/site-packages/launch/launch_description_sources/python_launch_file_utilities.py", line 37, in load_python_launch_file_as_module
    loader.exec_module(mod)
  File "<frozen importlib._bootstrap_external>", line 848, in exec_module
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
  File "/home/what/colcon_ws/install/mycobot_280_moveit2/share/mycobot_280_moveit2/launch/demo.launch.py", line 1, in <module>
    from moveit_configs_utils import MoveItConfigsBuilder
ModuleNotFoundError: No module named 'moveit_configs_utils'

The above exception was the direct cause of the following exception:

---

## 图 2-2 草稿：ROS2 显示链结构图

### 版本 A：适合直接照着在 PPT 里重画

```text
+---------------------------+
| joint_state_publisher_gui |
| 作用：发布关节状态         |
+---------------------------+
             |
             | 发布 JointState
             v
+---------------------------+
|       /joint_states       |
| 类型：sensor_msgs/        |
|       msg/JointState      |
+---------------------------+
             |
             | 订阅
             v
+---------------------------+
|   robot_state_publisher   |
| 作用：根据关节状态计算 TF  |
+---------------------------+
             |
             | 发布 TF
             v
+---------------------------+
|            /tf            |
| 类型：tf2_msgs/TFMessage  |
+---------------------------+
             |
             | 订阅
             v
+---------------------------+
|           RViz            |
| 作用：显示机械臂姿态       |
+---------------------------+
```

### 版本 B：适合做成更像论文图的左右分区结构

```text
┌───────────────────────┐
│      状态发布层       │
│ joint_state_publisher │
│         _gui          │
└──────────┬────────────┘
           │ 发布
           │ JointState
           v
┌───────────────────────┐
│     关键状态话题      │
│     /joint_states     │
└──────────┬────────────┘
           │ 订阅
           v
┌───────────────────────┐
│      状态解释层       │
│ robot_state_publisher │
└──────────┬────────────┘
           │ 发布 TF
           v
┌───────────────────────┐
│      变换结果话题     │
│         /tf           │
└──────────┬────────────┘
           │ 订阅
           v
┌───────────────────────┐
│       显示可视化层     │
│         RViz          │
└───────────────────────┘
```

### PPT 排版建议

1. 从上到下画五个矩形框，保持垂直主链，最清楚。
2. 节点框和 topic 框用不同颜色区分：
   - 节点：浅蓝色
   - topic：浅橙色
3. 箭头上标注动作词：
   - `发布 JointState`
   - `订阅`
   - `发布 TF`
   - `订阅`
4. 在 `/joint_states` 框旁边加一个红色小标注：
   - `关键攻击面`
5. 图题建议：
   - `ROS2 显示链的正常消息流结构`

### 图中建议保留的信息

- `joint_state_publisher_gui`
- `/joint_states`
- `robot_state_publisher`
- `/tf`
- `RViz`
- `JointState` 和 `TF` 的消息类型或语义

### 这张图主要说明的问题

- 正常情况下，机械臂姿态显示依赖于 `JointState -> TF -> RViz` 这条消息链。
- `/joint_states` 位于显示链上游，是后续攻击与防护分析的关键位置。
- 后文的消息伪造、本体振荡和可信 topic 防护，都是围绕这条链展开的。

---

## 图 2-4 草稿：XSB / MulVAL 风格推理流程图

### 设计目标

这张图不是画 ROS2 运行链本身，而是画“我们如何把实验现象翻译成规则推理，再得到攻击结论与防护结论”的过程。

它在报告里的作用是：

1. 让读者在进入第四节之前先看懂 XSB 在本文中扮演什么角色；
2. 说明本文不是只做实验现象展示，而是形成了“事实输入 -> 规则推理 -> 结果查询 -> 防护对照”的闭环。

### 推荐结构：左到右五段式流程图

```text
+------------------+
| 事实输入层       |
| Facts            |
|                  |
| - 主机/节点      |
| - topic          |
| - 发布订阅关系   |
| - 消息类型       |
| - 攻击者能力     |
+------------------+
         |
         | 规则建模
         v
+------------------+
| 规则推理层       |
| Rules            |
|                  |
| - 枚举 topic     |
| - 学习消息结构   |
| - 伪造状态消息   |
| - 状态传播       |
| - 竞争性发布     |
+------------------+
         |
         | 推理得到
         v
+------------------+
| 攻击链查询层     |
| Queries          |
|                  |
| - misleadPose... |
| - oscillating... |
| - physical...    |
+------------------+
         |
         | 进一步判断
         v
+------------------+
| 策略违规判断层   |
| Policy Violation |
|                  |
| - publish        |
| - destabilize    |
| - influence      |
+------------------+
         |
         | 加入防护条件后对照
         v
+------------------+
| 防护对照层       |
| Defense Compare  |
|                  |
| - topicAuth...   |
| - publisherACL.. |
| - defenseEff...  |
+------------------+
```

### 推荐结构：更适合 PPT 的视觉版本

如果你想让这张图更“论文风”一点，可以把它设计成：

- 第一列：`事实输入`
- 第二列：`攻击版规则模型`
- 第三列：`攻击版查询结果`
- 第四列：`防护版规则模型`
- 第五列：`防护版查询结果`

相当于把“推理流程”和“前后对照”合在一张图里。

可以写成：

```text
事实输入
  ↓
攻击版规则模型
  ↓
攻击版查询结果（yes）
  ↓
防护版规则模型
  ↓
防护版查询结果（no / defenseEffective = yes）
```

这个版本比五段式更适合你后面讲“攻击版和防护版是如何对照的”。

### 图中建议保留的关键词

为了和正文第四节完全一致，图里建议直接出现这些词：

- `事实输入`
- `规则推理`
- `攻击链查询`
- `策略违规判断`
- `防护前后对照`

如果空间足够，还可以把几个代表性谓词放进去：

- `enumerateTopic(...)`
- `forgeValidJointState(...)`
- `misleadPoseDisplay(...)`
- `oscillatingPoseDisplay(...)`
- `policyViolation(...)`
- `defenseEffective(...)`

### 颜色建议

建议用三种颜色就够：

- 蓝色：事实输入 / 基础信息
- 橙色：攻击版规则与攻击版查询
- 绿色：防护版规则与防护结果

这样读者一眼就能看出：

- 蓝色是“系统描述”
- 橙色是“攻击推理”
- 绿色是“防护推理”

### 我更推荐你最终采用的版本

如果只做一张，我建议你用这个结构：

```text
事实输入
   ↓
攻击版规则模型
   ↓
攻击链查询 / 策略违规判断
   ↓
防护版规则模型
   ↓
防护有效性结论
```

因为它最贴合你正文的逻辑顺序，而且做起来最快。

### 图题建议

- `图 2-4 XSB / MulVAL 风格攻击路径推理流程`

或者更完整一点：

- `图 2-4 面向 ROS2 机械臂状态链的 XSB / MulVAL 风格推理流程`

### 图注建议

可以在图下补一句：

- `该图展示了本文如何将 ROS2 场景中的节点、话题、消息类型与攻击者能力抽象为事实，并通过规则推理、攻击链查询与防护对照得到形式化结论。`

### 这张图主要说明的问题

- 本文不是只做实验现象展示，而是做了形式化推理闭环；
- XSB 在本文中的作用是“解释攻击为何成立、解释防护为何断链”；
- 第四节的攻击版模型和防护版模型都可以由这张图提前建立阅读框架。

---

## 图 3-1 草稿：系统场景与信任边界图

### 设计目标

这张图的重点不是再画一遍“正常显示链”，而是要把**攻击者处在什么位置、攻击是通过哪条链影响 RViz、信任边界为什么过宽，以及防护后边界如何收缩**表达清楚。

所以这张图最适合做成：

- **上半部分：未防护场景**
- **下半部分：防护后场景**

形成一个上下对照图。

---

### 版本 A：推荐结构（上下对照）

```text
【上：未防护场景】

攻击者节点
    |
    | 可接入同一 ROS2 Domain
    v
 joint_state_publisher_gui ----> /joint_states ----> robot_state_publisher ----> /tf ----> RViz
                                  ^
                                  |
                            恶意 publisher 可直接注入

标注：
- /joint_states：关键状态链
- 信任边界过宽：下游默认信任该 topic


【下：防护后场景】

攻击者节点
    |
    | 可接入同一 ROS2 Domain
    v
 joint_state_publisher_gui
            |
            v
 /_joint_states_authorized_source
            |
            v
 trusted_joint_state_filter
            |
            v
 /_joint_states_trusted ----> robot_state_publisher ----> /tf ----> RViz

标注：
- 原始输入与可信输出分离
- trusted_joint_state_filter 形成新的信任边界
- 攻击者不能再直接命中下游显示链
```

---

### 版本 B：更适合 PPT 的排版草稿

你可以把它画成两条平行的横向链路：

#### 上：未防护

```text
攻击者
  ↓
（同域接入）

joint_state_publisher_gui  --->  /joint_states  --->  robot_state_publisher  --->  /tf  --->  RViz
                                   ↑
                                   └──── 恶意消息可直接注入
```

#### 下：防护后

```text
攻击者
  ↓
（同域接入）

joint_state_publisher_gui
        ↓
/_joint_states_authorized_source
        ↓
trusted_joint_state_filter
        ↓
/_joint_states_trusted  --->  robot_state_publisher  --->  /tf  --->  RViz
```

这样做的好处是：

- 上下结构一致，读者容易比较
- 一眼就能看出防护到底加在了哪里

---

### 图中建议保留的关键元素

#### 未防护部分

- `attacker`
- `joint_state_publisher_gui`
- `/joint_states`
- `robot_state_publisher`
- `/tf`
- `RViz`
- 一条指向 `/joint_states` 的攻击箭头

#### 防护后部分

- `attacker`
- `joint_state_publisher_gui`
- `/_joint_states_authorized_source`
- `trusted_joint_state_filter`
- `/_joint_states_trusted`
- `robot_state_publisher`
- `/tf`
- `RViz`

---

### 必须标出来的两个概念

这张图最关键的不是节点名，而是这两个概念：

#### 1. 关键状态链

建议在未防护图里的 `/joint_states` 旁边标：

- `关键状态链`

或者：

- `关键攻击面`

#### 2. 信任边界

建议在防护图里把 `trusted_joint_state_filter` 用醒目的颜色单独突出，并标：

- `新的信任边界`

或者：

- `可信过滤边界`

---

### 颜色建议

为了和你前面图 2-2 保持一致，建议延续：

- 蓝色：ROS2 节点
- 橙色：topic

然后新增：

- 红色：攻击者与恶意注入箭头
- 绿色：`trusted_joint_state_filter` 或可信 topic

这样视觉上就会很清楚：

- 红色代表风险
- 绿色代表防护

---

### 图题建议

- `图 3-1 系统场景与信任边界对照图`

或者更具体一点：

- `图 3-1 未防护与防护后 ROS2 状态链的系统场景与信任边界对照`

---

### 图注建议

图下可以加一句：

- `上图展示未防护状态链中攻击者可通过 /joint_states 直接影响下游显示链；下图展示加入可信过滤节点后，系统信任边界由原始状态话题收缩到过滤节点与可信 topic 之间。`

---

### 这张图主要说明的问题

1. 攻击者不是直接篡改 `RViz`，而是通过状态链间接影响显示结果；
2. 风险根源不是“某一个节点有 bug”，而是**信任边界放得过宽**；
3. 防护的关键不是简单屏蔽消息，而是**重构信任链**；
4. 这张图会和第六节代码防护后的消息流图形成前后呼应。

---

### 我最推荐你最终采用的画法

如果你只做一个版本，我建议：

- 上半张：未防护横向链
- 下半张：防护后横向链
- `/joint_states` 用红框标“关键攻击面”
- `trusted_joint_state_filter` 用绿框标“新的信任边界”

这是最容易画、最容易讲、也最适合答辩的一版。

---

## 图 3-2 草稿：消息伪造攻击链时序图

### 设计目标

这张图要说明的不是“系统正常怎么跑”，而是：

**攻击者如何沿着 `JointState -> TF -> RViz` 这条链，一步步完成显示层状态欺骗。**

所以最适合画成：

- **时序图**
- 从左到右放参与者
- 从上到下放攻击步骤

---

### 推荐参与者（从左到右）

```text
攻击者    ROS2发现机制/CLI    /joint_states    robot_state_publisher    RViz
```

如果你觉得“ROS2发现机制/CLI”太抽象，也可以简化成：

```text
攻击者    ROS2系统    /joint_states    robot_state_publisher    RViz
```

但我更建议保留“ROS2发现/CLI”这一列，因为这样更容易解释：

- `ros2 topic list`
- `ros2 topic type`
- `ros2 interface show`

这些动作是怎么发生的。

---

### 推荐时序图草稿

```text
攻击者        ROS2发现/CLI        /joint_states        robot_state_publisher        RViz
  |                |                    |                       |                    |
  |---topic枚举--->|                    |                       |                    |
  |<--发现目标-----|                    |                       |                    |
  |                |                    |                       |                    |
  |---查询类型---->|                    |                       |                    |
  |<--JointState---|                    |                       |                    |
  |                |                    |                       |                    |
  |---构造合法消息--------------------------------------------->|                    |
  |                |---发布 forged JointState----------------->|                    |
  |                |                    |----被订阅/处理------->|                    |
  |                |                    |                       |---更新 TF--------->|
  |                |                    |                       |                    |
  |--------------------------------------------------------------------------误导显示-->|
```

---

### 更适合 PPT 重画的五步版

如果你不想画太复杂的时序线，也可以做成“参与者固定 + 关键动作编号”的版本：

#### 参与者列

```text
攻击者 | ROS2话题发现 | /joint_states | robot_state_publisher | RViz
```

#### 动作步骤

```text
① 发现 topic
攻击者 -> ROS2话题发现
说明：通过 `ros2 topic list` 识别 `/joint_states`

② 学习消息格式
攻击者 -> ROS2话题发现
说明：通过 `ros2 topic type` 和 `ros2 interface show` 获取 `sensor_msgs/msg/JointState`

③ 构造合法 JointState
攻击者
说明：匹配关节名称、关节范围，并写入有效时间戳

④ 发布伪造消息
攻击者 -> /joint_states -> robot_state_publisher
说明：伪造消息进入姿态更新链

⑤ 误导显示
robot_state_publisher -> RViz
说明：TF 被更新，RViz 中机械臂姿态被篡改
```

这个版本虽然不如标准时序图正规，但很好画，而且非常适合答辩讲解。

---

### 图中建议保留的关键词

建议直接把正文第四节里的术语提前放进图里，这样图文会更一致：

- `发现 topic`
- `学习消息格式`
- `构造合法 JointState`
- `发布 forged JointState`
- `更新 TF`
- `误导显示`

如果空间足够，还可以在小字里保留：

- `ros2 topic list`
- `ros2 topic type`
- `ros2 interface show`

---

### 建议怎么强调“攻击成立的关键”

这张图里最重要的不是“攻击者发了消息”，而是：

**攻击者发的是一条“会被目标链采信”的合法消息。**

所以建议在第 ③ 步旁边加一个小提示框：

```text
关键条件：
- 关节名称匹配
- 关节范围合法
- 时间戳有效
```

这个小框非常值钱，因为它正好把：

- 第五节实验
- 第四节 XSB 规则
- 第七节结果分析

三部分连起来了。

---

### 颜色建议

建议延续你前面图的风格：

- 蓝色：正常系统节点
- 橙色：关键 topic
- 红色：攻击者动作 / 恶意注入路径

其中：

- `/joint_states` 仍然可以用橙色高亮
- 第 ④ 步“发布 forged JointState”箭头可以用红色

这样读者会一眼知道哪一步是攻击真正发生的位置。

---

### 图题建议

- `图 3-2 基于 JointState 伪造的显示层状态欺骗攻击链时序图`

如果你想更简洁一点：

- `图 3-2 消息伪造攻击链时序图`

---

### 图注建议

可以在图下注明：

- `攻击者通过枚举 ROS2 话题、学习 JointState 消息结构并构造语义合法且时间戳有效的伪造状态消息，使 robot_state_publisher 更新 TF，最终误导 RViz 的机械臂姿态显示。`

---

### 这张图主要说明的问题

1. 攻击者不是直接修改 RViz，而是借助状态链间接影响显示结果；
2. 攻击链的关键不只是“能发消息”，而是“能构造一条会被采信的消息”；
3. 这张图可以直接作为第四节 XSB 规则建模的直观映射；
4. 它也能自然过渡到第五节实验设计与第七节实验结果。

---

### 我最推荐你最终采用的版本

如果时间紧，我建议你做：

- **五列参与者**
- **五个编号步骤**
- 第 ③ 步右侧加“关键条件”小框
- 第 ④ 步箭头用红色

这是最容易画、最容易讲、也最适合和正文对齐的一版。

---

## 图 4-1 草稿：XSB 建模映射图

### 设计目标

这张图的作用不是解释攻击过程本身，而是解释：

**ROS2 实验场景中的真实对象，是如何被抽象成 XSB 里的事实、规则和查询的。**

所以它最适合做成：

- **左右对照图**
- 左边放 ROS2 场景对象
- 右边放 XSB 建模元素
- 中间用箭头表示“映射关系”

这张图主要服务第四节开头，帮助读者理解：

- 第四节不是脱离实验重新“虚构”一个模型
- 而是把已经观察到的实验链条翻译成逻辑谓词和规则

---

### 推荐结构：左右映射图

```text
┌──────────────────────┐          ┌──────────────────────┐
│   ROS2 实验对象层     │   映射   │    XSB 建模元素层     │
└──────────────────────┘          └──────────────────────┘

joint_state_publisher_gui   --->   publishes(...)
robot_state_publisher       --->   subscribes(...), publishes(...)
RViz                        --->   subscribes(...)
/joint_states               --->   rosTopic(...), messageType(...)
/tf                         --->   rosTopic(...)
攻击者同域接入               --->   hacl(...), ros2DiscoveryEnabled(...)
显示链 / 信任关系            --->   trustsSubscriberInput(...)
桥接节点                    --->   bridgeNode(...)
```

---

### 更适合 PPT 的三列版

如果你想让逻辑更完整，可以做成三列：

```text
左：ROS2 实验对象
中：映射关系
右：XSB 谓词/规则
```

示意如下：

```text
【ROS2 对象】            【映射】              【XSB 元素】

攻击者节点         --->   主机/可达关系   --->   host(...), hacl(...)

ROS2 topic         --->   话题事实       --->   rosTopic(...), messageType(...)

发布者/订阅者       --->   通信关系       --->   publishes(...), subscribes(...)

显示链             --->   信任假设       --->   trustsSubscriberInput(...)

桥接节点           --->   下游传播条件   --->   bridgeNode(...)

攻击动作           --->   攻击规则       --->   enumerateTopic(...)
                                           forgeValidJointState(...)
                                           injectForgedJointState(...)

攻击结果           --->   查询结论       --->   misleadPoseDisplay(...)
                                           oscillatingPoseDisplay(...)
                                           policyViolation(...)
```
misleadPoseDisplay(...)
oscillatingPoseDisplay(...)
policyViolation(...)
这个版本更适合你后面讲“从实验到建模”的过程。

---

### 我最推荐你实际画的版本

我建议你画成 **四个大块**，而不是把每个谓词都单独展开，不然图会太密。

#### 左侧 4 个 ROS2 块

1. **节点对象**
   - `joint_state_publisher_gui`
   - `robot_state_publisher`
   - `RViz`
2. **话题对象**
   - `/joint_states`
   - `/tf`
3. **攻击者与环境**
   - `attacker`
   - `same ROS2 domain`
4. **扩展链对象**
   - `bridge node`

#### 右侧 4 个 XSB 块

1. **事实层 Facts**
   - `rosNode(...)`
   - `rosTopic(...)`
   - `publishes(...)`
   - `subscribes(...)`
   - `messageType(...)`
2. **能力与信任事实**
   - `hacl(...)`
   - `ros2DiscoveryEnabled(...)`
   - `trustsSubscriberInput(...)`
   - `bridgeNode(...)`
3. **攻击规则 Rules**
   - `enumerateTopic(...)`
   - `learnMessageSchema(...)`
   - `forgeValidJointState(...)`
   - `injectForgedJointState(...)`
4. **查询 Queries**
   - `misleadPoseDisplay(...)`
   - `oscillatingPoseDisplay(...)`
   - `physicalLayerRisk(...)`
   - `policyViolation(...)`

---

### 推荐箭头怎么连

建议不要每个小词都连线，否则会很乱。  
最好的方法是“一块对一块”。

例如：

```text
节点对象  -------------------->  事实层 Facts
话题对象  -------------------->  事实层 Facts
攻击者与环境  ---------------->  能力与信任事实
显示链与扩展链  -------------->  攻击规则 Rules
攻击结果观察  ---------------->  查询 Queries
```

如果你想再具体一点，可以补 2~3 条细线：

- `/joint_states` -> `rosTopic(...)`
- `joint_state_publisher_gui` -> `publishes(...)`
- `robot_state_publisher` -> `subscribes(...)`
- `attacker` -> `hacl(...)`

但不要超过 5 条细线，否则视觉上会乱。

---

### 图中建议保留的典型谓词

你不需要把所有谓词都写进去，只要放最有代表性的：

#### 事实层
- `rosTopic(...)`
- `publishes(...)`
- `subscribes(...)`
- `messageType(...)`

#### 能力/信任层
- `hacl(...)`
- `ros2DiscoveryEnabled(...)`
- `trustsSubscriberInput(...)`

#### 规则层
- `enumerateTopic(...)`
- `forgeValidJointState(...)`
- `injectForgedJointState(...)`

#### 查询层
- `misleadPoseDisplay(...)`
- `oscillatingPoseDisplay(...)`
- `policyViolation(...)`

---

### 颜色建议

建议继续保持和前面几张图一致的视觉语义：

- 蓝色：ROS2 系统对象
- 橙色：XSB 攻击建模元素
- 绿色：如果你想顺带点出防护版，也可以用来标 `defenseEffective(...)`

不过这张图的重点是攻击版建模映射，所以：

- 左边 ROS2 对象：蓝色
- 右边 XSB 模型：橙色
- 中间箭头：灰色或深蓝色

就足够了。

---

### 图题建议

- `图 4-1 ROS2 实验场景到 XSB 逻辑模型的映射关系图`

或者更简洁：

- `图 4-1 XSB 建模映射图`

---

### 图注建议

可以写成：

- `该图展示了本文如何将 ROS2 实验场景中的节点、话题、发布订阅关系、攻击者能力与下游信任关系，抽象为 XSB 中的事实、规则与查询，从而形成与实际实验链条一致的形式化推理模型。`

---

### 这张图主要说明的问题

1. 第四节的 XSB 建模不是脱离实验凭空建模；
2. ROS2 中的真实对象可以稳定地映射为逻辑谓词；
3. 攻击规则和攻击查询都来源于前面已经观察到的实验链；
4. 这张图能很好地为后面的“事实层 / 规则层 / 查询层”展开做铺垫。

---

### 我最推荐你最终采用的画法

如果你想效率最高，我建议：

- 左边 4 个蓝色大框：
  - 节点对象
  - 话题对象
  - 攻击者与环境
  - 扩展链对象
- 右边 4 个橙色大框：
  - Facts
  - 能力与信任事实
  - Rules
  - Queries
- 中间只画 4~6 条关键映射箭头

这样最简洁，也最符合你报告里第四节的结构。
Traceback (most recent call last):
  File "/opt/ros/foxy/lib/python3.8/site-packages/launch/launch_service.py", line 228, in _process_one_event
    await self.__process_event(next_event)
  File "/opt/ros/foxy/lib/python3.8/site-packages/launch/launch_service.py", line 248, in __process_event
    visit_all_entities_and_collect_futures(entity, self.__context))
  File "/opt/ros/foxy/lib/python3.8/site-packages/launch/utilities/visit_all_entities_and_collect_futures_impl.py", line 45, in visit_all_entities_and_collect_futures
    futures_to_return += visit_all_entities_and_collect_futures(sub_entity, context)
  File "/opt/ros/foxy/lib/python3.8/site-packages/launch/utilities/visit_all_entities_and_collect_futures_impl.py", line 45, in visit_all_entities_and_collect_futures
    futures_to_return += visit_all_entities_and_collect_futures(sub_entity, context)
  File "/opt/ros/foxy/lib/python3.8/site-packages/launch/utilities/visit_all_entities_and_collect_futures_impl.py", line 38, in visit_all_entities_and_collect_futures
    sub_entities = entity.visit(context)
  File "/opt/ros/foxy/lib/python3.8/site-packages/launch/action.py", line 108, in visit
    return self.execute(context)
  File "/opt/ros/foxy/lib/python3.8/site-packages/launch/actions/include_launch_description.py", line 130, in execute
    launch_description = self.__launch_description_source.get_launch_description(context)
  File "/opt/ros/foxy/lib/python3.8/site-packages/launch/launch_description_source.py", line 84, in get_launch_description
    self._get_launch_description(self.__expanded_location)
  File "/opt/ros/foxy/lib/python3.8/site-packages/launch/launch_description_sources/any_launch_description_source.py", line 53, in _get_launch_description
    return get_launch_description_from_any_launch_file(location)
  File "/opt/ros/foxy/lib/python3.8/site-packages/launch/launch_description_sources/any_launch_file_utilities.py", line 56, in get_launch_description_from_any_launch_file
    raise InvalidLaunchFileError(extension, likely_errors=exceptions)
launch.invalid_launch_file_error.InvalidLaunchFileError: Caught exception when trying to load file of format [py]: No module named 'moveit_configs_utils'
what@ubuntu:~/colcon_ws$ 

```
python3 -c "import importlib.util; print(importlib.util.find_spec('moveit_configs_utils'))"
ros2 pkg list | grep moveit


```bash
what@ubuntu:~/colcon_ws$ ros2 pkg list | grep moveit_configs_utils
what@ubuntu:~/colcon_ws$ apt-cache search moveit_configs_utils
what@ubuntu:~/colcon_ws$ apt-cache search ros-foxy-moveit
ros-foxy-moveit - Meta package that contains all essential packages of MoveIt 2
ros-foxy-moveit-chomp-optimizer-adapter - MoveIt planning request adapter utilizing chomp for solution optimization
ros-foxy-moveit-chomp-optimizer-adapter-dbgsym - debug symbols for ros-foxy-moveit-chomp-optimizer-adapter
ros-foxy-moveit-common - Common support functionality used throughout MoveIt
ros-foxy-moveit-core - Core libraries used by MoveIt
ros-foxy-moveit-core-dbgsym - debug symbols for ros-foxy-moveit-core
ros-foxy-moveit-kinematics - Package for all inverse kinematics solvers in MoveIt
ros-foxy-moveit-kinematics-dbgsym - debug symbols for ros-foxy-moveit-kinematics
ros-foxy-moveit-msgs - Messages, services and actions used by MoveIt
ros-foxy-moveit-msgs-dbgsym - debug symbols for ros-foxy-moveit-msgs
ros-foxy-moveit-planners - Meta package that installs all available planners for MoveIt
ros-foxy-moveit-planners-chomp - The interface for using CHOMP within MoveIt
ros-foxy-moveit-planners-chomp-dbgsym - debug symbols for ros-foxy-moveit-planners-chomp
ros-foxy-moveit-planners-ompl - MoveIt interface to OMPL
ros-foxy-moveit-planners-ompl-dbgsym - debug symbols for ros-foxy-moveit-planners-ompl
ros-foxy-moveit-plugins - Metapackage for MoveIt plugins.
ros-foxy-moveit-resources - Resources used for MoveIt testing
ros-foxy-moveit-resources-fanuc-description - Fanuc Resources used for MoveIt testing
ros-foxy-moveit-resources-fanuc-moveit-config - MoveIt Resources for testing: Fanuc M-10iA.
ros-foxy-moveit-resources-panda-description - panda Resources used for MoveIt testing
ros-foxy-moveit-resources-panda-moveit-config - MoveIt Resources for testing: Franka Emika Panda A project-internal configuration for testing in MoveIt.
ros-foxy-moveit-resources-pr2-description - PR2 Resources used for MoveIt! testing
ros-foxy-moveit-ros - Components of MoveIt that use ROS
ros-foxy-moveit-ros-benchmarks - Enhanced tools for benchmarks in MoveIt
ros-foxy-moveit-ros-benchmarks-dbgsym - debug symbols for ros-foxy-moveit-ros-benchmarks
ros-foxy-moveit-ros-move-group - The move_group node for MoveIt
ros-foxy-moveit-ros-move-group-dbgsym - debug symbols for ros-foxy-moveit-ros-move-group
ros-foxy-moveit-ros-occupancy-map-monitor - Components of MoveIt connecting to occupancy map
ros-foxy-moveit-ros-occupancy-map-monitor-dbgsym - debug symbols for ros-foxy-moveit-ros-occupancy-map-monitor
ros-foxy-moveit-ros-perception - Components of MoveIt connecting to perception
ros-foxy-moveit-ros-perception-dbgsym - debug symbols for ros-foxy-moveit-ros-perception
ros-foxy-moveit-ros-planning - Planning components of MoveIt that use ROS
ros-foxy-moveit-ros-planning-dbgsym - debug symbols for ros-foxy-moveit-ros-planning
ros-foxy-moveit-ros-planning-interface - Components of MoveIt that offer simpler interfaces to planning and execution
ros-foxy-moveit-ros-planning-interface-dbgsym - debug symbols for ros-foxy-moveit-ros-planning-interface
ros-foxy-moveit-ros-robot-interaction - Components of MoveIt that offer interaction via interactive markers
ros-foxy-moveit-ros-robot-interaction-dbgsym - debug symbols for ros-foxy-moveit-ros-robot-interaction
ros-foxy-moveit-ros-visualization - Components of MoveIt that offer visualization
ros-foxy-moveit-ros-visualization-dbgsym - debug symbols for ros-foxy-moveit-ros-visualization
ros-foxy-moveit-ros-warehouse - Components of MoveIt connecting to MongoDB
ros-foxy-moveit-ros-warehouse-dbgsym - debug symbols for ros-foxy-moveit-ros-warehouse
ros-foxy-moveit-runtime - moveit_runtime meta package contains MoveIt packages that are essential for its runtime (e.g.
ros-foxy-moveit-servo - Provides real-time manipulator Cartesian and joint servoing.
ros-foxy-moveit-servo-dbgsym - debug symbols for ros-foxy-moveit-servo
ros-foxy-moveit-simple-controller-manager - A generic, simple controller manager plugin for MoveIt.
ros-foxy-moveit-simple-controller-manager-dbgsym - debug symbols for ros-foxy-moveit-simple-controller-manager
what@ubuntu:~/colcon_ws$ ls
build  install  log  src
what@ubuntu:~/colcon_ws$ cd src/
what@ubuntu:~/colcon_ws/src$ ls
mycobot_ros2
what@ubuntu:~/colcon_ws/src$ cd mycobot_ros2/
what@ubuntu:~/colcon_ws/src/mycobot_ros2$ git branch -a
* humble
  remotes/origin/HEAD -> origin/humble
  remotes/origin/humble
what@ubuntu:~/colcon_ws/src/mycobot_ros2$ git branch --show-current
humble
what@ubuntu:~/colcon_ws/src/mycobot_ros2$ git log -1 --oneline
8e70efe (grafted, HEAD -> humble, origin/humble, origin/HEAD) update 280 rdkx5 ros2 code
what@ubuntu:~/colcon_ws/src/mycobot_ros2$ 

```


```bash
?- misleadPoseDisplay(attacker_host, mycobot_vm).
?- oscillatingPoseDisplay(attacker_host, mycobot_vm).
?- physicalLayerRisk(attacker_host, mycobot_vm).
?- policyViolation(attacker_host, Action, Resource).
```

```bash
what@ubuntu:~/XSB/bin$ ./xsb
[xsb_configuration loaded]
[sysinitrc loaded]
[xsbbrat loaded]

XSB Version 5.0.0 (Green Tea) of May 15, 2022
[x86_64-pc-linux-gnu 64 bits; mode: optimal; engine: slg-wam; scheduling: local]
[Build date: 2025-11-28]

| ?- ['joint.xsb'].
[Compiling ./joint.xsb]
% Specialising partially instantiated calls to hacl/3
% Specialising partially instantiated calls to subscribes/2
% Specialising partially instantiated calls to trustsSubscriberInput/2
% Specialising partially instantiated calls to publishes/2
% Specialising partially instantiated calls to bridgeNode/1
% Specialising partially instantiated calls to forwardsToPhysicalLayer/1
% Specialising partially instantiated calls to allowAuthority/2
[./joint.xsb compiled, cpu time used: 0.032 seconds]
[./joint.xsb loaded]

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


很好，接下来我们开始写报告。报告必须严格按照学术论文的规范来写（因为是报告而非Latex格式的论文，因此标准可以适当放宽）
首先，我要求你仔细阅读`reference`文件夹下我们立项和中期答辩时的文档，在`report/report.md`中先搭出一个骨架来，包括摘要，实验目的背景这些可以先填上，后面的大小标题可以组织起来，等我确认后再开始填充内容。请你先搭出这个骨架来。

## 图 4-2 草稿：攻击版规则层逻辑链图

这张图和图 4-1 的分工不一样。

- 图 4-1 讲的是：ROS2 实验对象如何映射到 XSB 元素；
- 图 4-2 讲的是：攻击版规则在 XSB 里是如何一步步从基础能力推出攻击结果的。

所以这张图最适合画成 **一条主链 + 两条支线**：

1. 主链：显示层状态欺骗
2. 支线 A：竞争性 publisher 振荡
3. 支线 B：下游传播到物理层的潜在风险

### 推荐画法

最合适的是 **主链横向、支线纵向挂接** 的逻辑链图。

#### 主链（横向）

从左到右画 6 个框：

```text
--------------------+
| enumerateTopic    |
+-------------------+
          |
          v
+--------------------+
| learnMessageSchema |
+--------------------+
          |
          v
+------------------------+
| forgeValidJointState   |
+------------------------+
          |
          v
+------------------------+
| injectForgedJointState |
+------------------------+
          |
          v
+----------------+
| tamperTFStream |
+----------------+
          |
          v
+---------------------+
| misleadPoseDisplay  |
+---------------------+
```

这条主链对应正文里的核心攻击链 A：

- 枚举关键 topic
- 学习消息结构
- 伪造合法 JointState
- 注入伪造状态
- 篡改 TF 链
- 最终误导 RViz 显示

### 支线 A：竞争性 publisher 风险

这条线建议从主链中段右下方另起一条支线，单独挂出来：

```text
 legitimatePublisher
          +
 maliciousPublisher
          |
          v
 competingPublisherState
          |
          v
 oscillatingPoseDisplay
```

如果你想图更工整，可以把 `legitimatePublisher` 和 `maliciousPublisher` 画成两个小框并列，再汇入 `competingPublisherState`。

这条支线的含义是：

- 不需要攻击者完全独占状态链
- 只要合法 publisher 和恶意 publisher 并存
- 且系统缺少来源约束
- 就能推出姿态振荡结论

### 支线 B：下游传播风险

这条线建议从 `injectForgedJointState` 向下再拉一条支线：

```text
 injectForgedJointState
          |
          v
   propagateToBridge
          |
          v
  physicalLayerRisk
```

如果你希望和 XSB 文件严格贴齐，也可以根据你最终规则里实际使用的谓词换成：

- `bridgeNode(...)`
- `forwardsToPhysicalLayer(...)`
- `physicalLayerRisk(...)`

也就是说，PPT 里这一支线有两种写法：

#### 写法 A：偏逻辑链表达
- `injectForgedJointState`
- `propagateToBridge`
- `physicalLayerRisk`

#### 写法 B：偏规则文件原名
- `injectForgedJointState`
- `bridgeNode / forwardsToPhysicalLayer`
- `physicalLayerRisk`

如果你问我推荐哪种：  
**正文图更建议写法 A**，因为更好懂；如果你想和 XSB 文件逐字对齐，再选写法 B。

### 图中可以额外标的小条件

为了避免主链看起来像“攻击者想发就能发”，建议在 `forgeValidJointState` 上方或旁边加一个小气泡框：

```text
关键条件：
- 关节名称匹配
- 关节范围合法
- 时间戳有效
```

这样读者会立刻明白：

- 主链不是简单的 topic 写入
- 而是“满足语义条件之后”的有效伪造

### 推荐最终排版

#### 版本 A：最推荐

- 中间一条横向主链
- 上方或下方一个小条件框，贴近 `forgeValidJointState`
- 右下方挂“竞争性 publisher”支线
- 左下方或下下方挂“物理层传播”支线

这种结构很适合 PPT，而且和第四节文字结构最一致。

#### 版本 B：如果你想更规整

把整张图分成三层：

1. 上层：输入与前提
   - `enumerateTopic`
   - `learnMessageSchema`
   - `forgeValidJointState`
2. 中层：核心攻击
   - `injectForgedJointState`
   - `tamperTFStream`
   - `misleadPoseDisplay`
3. 下层：扩展风险
   - `competingPublisherState`
   - `oscillatingPoseDisplay`
   - `physicalLayerRisk`

这个版本更像论文图，但 PPT 里稍微没版本 A 那么灵活。

### 直接照着画的 PPT 版

如果你现在是想“不要再看抽象说明，直接告诉我 PPT 怎么摆”，那就按下面这版来：

#### 第一步：先摆主链

在页面中间横向排 6 个框，从左到右：

1. `enumerateTopic(...)`
2. `learnMessageSchema(...)`
3. `forgeValidJointState(...)`
4. `injectForgedJointState(...)`
5. `tamperTFStream(...)`
6. `misleadPoseDisplay(...)`

箭头全部从左到右直连。

#### 第二步：加条件框

在 `forgeValidJointState(...)` 的上方放一个小白框，写：

```text
关键条件
- 关节名称匹配
- 关节范围合法
- 时间戳有效
```

再用一个短箭头或虚线把它指向 `forgeValidJointState(...)`。

#### 第三步：加竞争性 publisher 支线

在 `injectForgedJointState(...)` 右下方单独拉一条支线：

- 左边并排两个小框：
  - `legitimatePublisher(...)`
  - `maliciousPublisher(...)`
- 两个框一起汇入：
  - `competingPublisherState(...)`
- 再往右或往下接：
  - `oscillatingPoseDisplay(...)`

这条线建议用和主链不同的颜色，比如橙红色。

#### 第四步：加物理层传播支线

从 `injectForgedJointState(...)` 的下方再拉一条支线：

1. `propagateToBridge(...)`
2. `physicalLayerRisk(...)`

如果你想和 XSB 文件更严格对齐，也可以把中间那个框写成：

- `bridgeNode(...) / forwardsToPhysicalLayer(...)`

但如果只是为了报告可读性，`propagateToBridge(...)` 更直观。

#### 第五步：颜色分层

建议这样分：

- 蓝色：前提与基础能力
  - `enumerateTopic(...)`
  - `learnMessageSchema(...)`
  - `forgeValidJointState(...)`
- 橙色：显示层主攻击链
  - `injectForgedJointState(...)`
  - `tamperTFStream(...)`
  - `misleadPoseDisplay(...)`
- 红色：竞争性 publisher 支线
  - `competingPublisherState(...)`
  - `oscillatingPoseDisplay(...)`
- 灰色或深黄色：物理层传播支线
  - `propagateToBridge(...)`
  - `physicalLayerRisk(...)`

#### 第六步：图里一定要讲清楚的意思

这张图最核心要让读者一眼看懂三件事：

1. 攻击不是“直接误导 RViz”，而是通过一串规则一步步推出来的；
2. 主攻击链是“状态欺骗”；
3. 扩展风险包括“竞争性振荡”和“向物理层传播”。

#### 最终最推荐的布局

```text
主链：横向居中
支线 A：从 injectForgedJointState 右下挂接
支线 B：从 injectForgedJointState 下方挂接
条件框：放在 forgeValidJointState 上方
```

这样排出来最稳，也最像你正文第四节的结构。

### 配色建议

- 蓝色：基础能力与中间规则
- 橙色：显示层攻击结果主链
- 红色：竞争性 publisher 风险支线
- 灰色或深橙：物理层传播风险支线

这样读者能一眼区分：

- 哪条是主攻击链
- 哪条是扩展风险

### 图题建议

`图 4-2 攻击版规则层逻辑链`

### 图注建议

`图中主链展示了从 topic 枚举、消息学习、合法状态伪造到显示层状态欺骗的规则推理过程；下方支线分别展示了竞争性 publisher 导致状态振荡的扩展链，以及状态风险向下游桥接节点和潜在物理层传播的风险链。`

### 适合直接抄到 PPT 里的最终文字

#### 主链
- `enumerateTopic(...)`
- `learnMessageSchema(...)`
- `forgeValidJointState(...)`
- `injectForgedJointState(...)`
- `tamperTFStream(...)`
- `misleadPoseDisplay(...)`

#### 支线 A
- `legitimatePublisher(...)`
- `maliciousPublisher(...)`
- `competingPublisherState(...)`
- `oscillatingPoseDisplay(...)`

#### 支线 B
- `injectForgedJointState(...)`
- `propagateToBridge(...)`
- `physicalLayerRisk(...)`

#### 条件框
- 关节名称匹配
- 关节范围合法
- 时间戳有效

### 我更推荐的最终版本

如果你想效率最高，就用这个结构：

1. 一条横向主链；
2. `forgeValidJointState` 上方一个小条件框；
3. `competingPublisherState` 作为右下支线；
4. `physicalLayerRisk` 作为下方次支线。

这样最清楚，也最容易服务正文里的“主线 + 扩展线”叙述。

## 图 6-1 草稿：防护版 XSB 断链逻辑图

这张图最省事、也最好的画法，不是从零重新设计，而是**直接基于图 4-2 的攻击版规则层逻辑链做增强版**。

也就是说：

- 保留图 4-2 的主链和两条扩展链；
- 在被防护截断的位置加“防护条件”；
- 用叉号、虚线、变灰或 `blocked` 标记说明“攻击链在这里断掉了”。

这样读者会一眼看懂：

- 图 4-2：攻击为什么成立
- 图 6-1：防护后是哪一环不再成立

### 这张图想说明什么

图 6-1 不是要告诉读者“结果不同了”，而是要明确展示：

**防护引入后，攻击链并不是神秘地失效，而是在具体规则条件处被切断。**

### 最推荐的画法：图 4-2 的防护增强版

#### 主链仍然保留

主链仍然保留：

- `enumerateTopic(...)`
- `learnMessageSchema(...)`
- `forgeValidJointState(...)`
- `injectForgedJointState(...)`
- `tamperTFStream(...)`
- `misleadPoseDisplay(...)`

但要把前 3 个框和后 3 个框区分开：

- 前 3 个：保留正常颜色，表示这些前置能力在逻辑上仍可能存在；
- 后 3 个：变浅灰，表示防护后不再可达或不再成立。

#### 断链点 1：阻断消息注入

在：

- `forgeValidJointState(...) -> injectForgedJointState(...)`

这条连接上，加一个绿色防护框：

- `topicAuthEnabled(...)`
- `publisherACLEnabled(...)`

topicAuthEnabled(...)
publisherACLEnabled(...)

再加一个红色叉号或小字：

- `注入被阻断`

含义是：

- 攻击者即使学会了消息结构并能构造合法 `JointState`
- 也无法再顺利把伪造状态注入到关键 topic

所以后面的：

- `injectForgedJointState(...)`
- `tamperTFStream(...)`
- `misleadPoseDisplay(...)`

都应该显示为“失效/不可达”。

#### 断链点 2：阻断竞争性 publisher

保留支线 A：

- `legitimatePublisher(...)`
- `maliciousPublisher(...)`
- `competingPublisherState(...)`
- `oscillatingPoseDisplay(...)`

但在两个 publisher 汇入 `competingPublisherState(...)` 的位置，加一个绿色防护框：

- `singleAuthoritativePublisher(...)`

再加一个叉号或标注：

- `竞争输入被阻断`

然后把：

- `competingPublisherState(...)`
- `oscillatingPoseDisplay(...)`

都变灰，表示这条扩展链在防护版中不再成立。

#### 断链点 3：下游传播链自然失效

支线 B 最简单的处理方式是：

- 仍然保留：
  - `propagateToBridge(...)`
  - `physicalLayerRisk(...)`
- 但在前面补一条来源关系：
  - `injectForgedJointState(...) -> propagateToBridge(...)`

然后因为 `injectForgedJointState(...)` 已经被阻断，

- `propagateToBridge(...)`
- `physicalLayerRisk(...)`

也都变灰。

图里可以额外加一个小字：

- `由主链截断导致不可达`

### 直接照着画的 PPT 版

#### 第一步：复制图 4-2

直接复制一份图 4-2，不要重画框架。

#### 第二步：把攻击成功部分变灰

把以下框改成浅灰或半透明：

- `injectForgedJointState(...)`
- `tamperTFStream(...)`
- `misleadPoseDisplay(...)`
- `competingPublisherState(...)`
- `oscillatingPoseDisplay(...)`
- `propagateToBridge(...)`
- `physicalLayerRisk(...)`

这样读者一眼就知道：

**这些攻击结果在防护版里不再可达。**

#### 第三步：在主链切点加防护框

在 `forgeValidJointState(...)` 和 `injectForgedJointState(...)` 之间加一个绿色框，写：

```text
topicAuthEnabled(...)
publisherACLEnabled(...)
```

再在这个绿色框旁边放一个红色 `×`，或写：

- `blocked`

#### 第四步：在扩展链 A 切点加防护框

在两个 publisher 汇入 `competingPublisherState(...)` 的位置加一个绿色框，写：

```text
singleAuthoritativePublisher(...)
```

同样在旁边放一个 `×` 或写：

- `blocked`

#### 第五步：在支线 B 上加来源关系

如果版面允许，从 `injectForgedJointState(...)` 往下拉一条线到：

- `propagateToBridge(...)`

再接：

- `physicalLayerRisk(...)`

并把整条支线变灰。

### 推荐颜色

- 蓝色：前置能力仍存在
- 绿色：防护条件
- 浅灰：防护后不再成立的攻击规则
- 红色叉号：断链位置

这个配色会和图 4-2 形成很清楚的攻防对照。

### 建议加的标题标签

如果你愿意再加一点解释，可以在图里直接放两个小标签：

- `防护切点 1：消息注入被阻断`
- `防护切点 2：竞争性 publisher 被阻断`

这样图会更“会说话”。

### 图题建议

`图 6-1 防护版 XSB 断链逻辑图`

### 图注建议

`该图在图 4-2 攻击版规则层逻辑链的基础上，标出了防护版中使攻击链失效的关键切点。对于显示层状态欺骗主链，topic 级认证与 publisher ACL 阻断了伪造状态的注入；对于竞争性 publisher 风险链，单一权威 publisher 约束阻断了多源竞争输入。因此，防护版中的顶层攻击查询不再成立。`

### 最后一句最实用的建议

这张图不要重新发明结构，**直接复制图 4-2，然后把“防护条件”加在箭头上，把后续攻击结论灰掉**，这是最快也最稳的做法。

## 图 6-2 草稿：代码级防护后消息流图

这张图和图 6-1 的分工不一样：

- 图 6-1 讲的是：XSB 规则层里，攻击链在哪一环被切断；
- 图 6-2 讲的是：代码实现之后，ROS2 消息流在结构上是如何被重构的。

所以这张图不需要再强调“攻击为什么成立”，而是要明确展示：

**原始输入不再直接进入下游显示链，必须先经过可信过滤层，只有通过校验的消息才会进入可信 topic。**

### 最推荐的画法

最适合做成一张 **自左向右的流程/架构图**，主链清楚，必要时再加一个桥接分支。

### 主链应该怎么画

从左到右排 6 个框：

1. `joint_state_publisher_gui`
2. `/_joint_states_authorized_source`
3. `trusted_joint_state_filter`
4. `/_joint_states_trusted`
5. `robot_state_publisher`
6. `RViz`

箭头全部从左到右直连。

### 推荐的文字写法

#### 节点框

蓝色框可以写：

joint_state_publisher_gui
发布原始关节状态

trusted_joint_state_filter
执行单一 publisher / 时间戳 / 名称 / 范围检查

robot_state_publisher
仅订阅可信 JointState 并更新 TF

`RViz`  
显示机械臂姿态

#### topic 框

建议用不同颜色和节点区分：

/_joint_states_authorized_source
原始输入层: 未直接信任

/_joint_states_trusted
可信输出层: 仅转发通过校验的 JointState

### 图里一定要强调的两个概念

#### 1. 原始输入层

在 `/_joint_states_authorized_source` 上方或旁边加一个小红框：

- `原始输入`
- `待校验`

含义是：

- 这个 topic 不再是权威状态输入
- 它只是进入过滤器前的原始入口

#### 2. 可信输出层

在 `/_joint_states_trusted` 上方或旁边加一个小绿框：

- `可信输出`
- `通过校验后转发`

含义是：

- 只有通过过滤器检查的消息
- 才能进入真正影响下游的状态链

### 过滤器附近建议怎么表现

为了让读者一眼看懂这个节点的价值，建议在 `trusted_joint_state_filter` 旁边加一个小白色说明框：

```text
核心检查：
- 单一 publisher
- 时间戳有效
- 关节名称匹配
- 关节范围合法
```

这个框不要太大，够说明作用就行。

### 是否要补桥接节点分支

如果版面允许，我建议加。

最简单的画法是：

从 `/_joint_states_trusted` 再向下分一条支线到：

- `sync_plan_arduino`
- 或者更泛化一点写成：`bridge / downstream node`

然后在框内写：
sync_plan_arduino
仅订阅可信 JointState

这样这张图就能把“显示链”和“潜在下游链”一起收住。

如果你觉得图会太挤，也可以先不画这个分支，只保留主链。  
主链本身已经足够表达第六节最核心的设计思想。

### 推荐最终版布局

#### 版本 A：最推荐，最清楚

一条横向主链：

```text
joint_state_publisher_gui
        ->
/_joint_states_authorized_source
        ->
trusted_joint_state_filter
        ->
/_joint_states_trusted
        ->
robot_state_publisher
        ->
RViz
```

然后：

- 在 `/_joint_states_authorized_source` 上方加红色小标签：`原始输入`
- 在 `/_joint_states_trusted` 上方加绿色小标签：`可信输出`
- 在 `trusted_joint_state_filter` 上方或下方加一个白色说明框：`核心检查`

#### 版本 B：如果你想更像“架构图”

可以把图分成三列：

1. 输入层
   - `joint_state_publisher_gui`
   - `/_joint_states_authorized_source`
2. 过滤层
   - `trusted_joint_state_filter`
3. 可信消费层
   - `/_joint_states_trusted`
   - `robot_state_publisher`
   - `RViz`

这个版本更像系统架构，但不如版本 A 那么一眼直观。

### 配色建议

- 蓝色：ROS2 节点
- 橙色或浅红色：原始输入 topic
- 绿色：可信输出 topic
- 白色：过滤器检查说明框

这样和图 3-1 的“未防护 / 防护后系统场景图”也能形成风格呼应。

### 这张图要说明的问题

这张图最重要的不是“过滤器做了多少检查”，而是：

1. 系统不再直接信任裸 `/joint_states`
2. 信任链已经从结构上重构
3. 原始输入和可信输出被明确分层
4. 下游只消费可信 topic

换句话说，这张图要把“防护不是简单加几个 if，而是重新划分信任边界”这件事讲清楚。

### 图题建议

`图 6-2 代码级防护后消息流结构`

### 图注建议

`代码级防护实现后，原始 JointState 输入不再直接进入下游显示链，而是先进入原始输入 topic，由 trusted_joint_state_filter 执行单一 publisher、时间戳、关节名称和关节范围检查；只有通过校验的消息才会被转发到可信输出 topic，并继续供 robot_state_publisher 与 RViz 使用。`

### 适合直接抄到 PPT 里的最终文字

#### 主链
- `joint_state_publisher_gui`
- `/_joint_states_authorized_source`
- `trusted_joint_state_filter`
- `/_joint_states_trusted`
- `robot_state_publisher`
- `RViz`

#### 红色标签
- 原始输入
- 待校验

#### 绿色标签
- 可信输出
- 通过校验后转发

#### 过滤器说明框
- 单一 publisher
- 时间戳有效
- 关节名称匹配
- 关节范围合法

### 一句话最实用建议

如果你想最快画出来，就按这个思路：

**主链横向排开，原始输入用红色标，可信输出用绿色标，过滤器旁边放一个小检查框。**

## 图 8-1 草稿：后续工作路线图

这张图和前面的结构图、攻击链图不一样。

- 前面的图主要说明“我们已经做了什么”；
- 这张图要说明“在现有工作的基础上，后面还能怎么往下走”。

所以它最适合画成一张 **分层路线图**，而不是复杂的时序图或消息流图。

### 最推荐的画法

建议按 **短期可做 / 中期扩展 / 长期目标** 三层来画。

这比把五个方向平铺出来更清楚，因为它能体现：

- 哪些是基于现有成果最容易继续推进的；
- 哪些需要新环境、新平台或更高工程复杂度；
- 哪些属于更完整、更系统化的长期研究目标。

### 推荐结构

#### 第一层：短期可做

建议放 2 个框：

1. `实机闭环验证`
   - 在现有 myCobot-280-arduino 平台上完成从状态链到执行层的进一步验证
   - 核心关注：当前显示层与规则层结论能否向真实动作层延伸

实机闭环验证
在现有 myCobot-280-arduino 平台上完成从状态链到执行层的进一步验证
核心关注：当前显示层与规则层结论能否向真实动作层延伸

2. `MoveIt2 / 轨迹控制链`
   - 继续打通比 `JointState` 更高层的控制接口
   - 核心关注：从状态链扩展到轨迹链、规划链与控制链

MoveIt2 / 轨迹控制链
继续打通比 JointState 更高层的控制接口
核心关注：从状态链扩展到轨迹链、规划链与控制链

这两个方向最适合放在“短期”里，因为它们本质上是对你现有工作主线的自然延伸。

#### 第二层：中期扩展

建议放 2 个框：

1. `SROS2 / DDS Security`
   - 引入节点认证、加密通信、访问控制和 topic 级权限管理
   - 核心关注：把当前“最小应用层防护原型”升级为更正式的中间件安全机制
SROS2 / DDS Security
引入节点认证、加密通信、访问控制和 topic 级权限管理
核心关注：把当前“最小应用层防护原型”升级为更正式的中间件安全机制

2. `多机器人与更多 ROS2 接口`
   - 从单机械臂、单 `JointState` 主线扩展到多机器人协同环境和更多关键接口
   - 核心关注：不同 topic、service、action 在开放 ROS2 域中的风险传播
多机器人与更多 ROS2 接口
从单机械臂、单 JointState 主线扩展到多机器人协同环境和更多关键接口
核心关注：不同 topic、service、action 在开放 ROS2 域中的风险传播
这两个方向更像“从当前原型走向更完整系统”，放在中期最合适。

#### 第三层：长期目标

建议放 1 个大框：

1. `更高程度自动化评估`
   - 将实验复现、规则推理、策略判定、防护验证进一步联动
   - 核心关注：形成更系统的自动化机器人攻击面分析与安全评估流程

更高程度自动化评估
将实验复现、规则推理、策略判定、防护验证进一步联动
核心关注：形成更系统的自动化机器人攻击面分析与安全评估流程

这个方向最适合放在最后，因为它是对前面所有工作线的整合。

### 最适合 PPT 的布局

#### 版本 A：三层箭头式路线图

从上到下三层：

```text
短期可做
 ├─ 实机闭环验证
 └─ MoveIt2 / 轨迹控制链

中期扩展
 ├─ SROS2 / DDS Security
 └─ 多机器人与更多 ROS2 接口

长期目标
 └─ 更高程度自动化评估
```

层与层之间用向下箭头连接，表示路线逐步推进。

这是我最推荐的版本，因为最清楚，也最容易画。

#### 版本 B：中心辐射式

中间放一个中心框：

- `基于状态链的攻击复现—推理—防护闭环`

然后向外发散 5 个方向：

- 实机闭环验证
- MoveIt2 / 轨迹控制链
- SROS2 / DDS Security
- 多机器人与更多 ROS2 接口
- 更高程度自动化评估

这个版本更像“展望脑图”，但缺点是时间层次不如版本 A 清晰。

### 我更推荐的最终版本

优先选 **版本 A：三层箭头式路线图**。

因为你的第八节正文已经是按“从当前工作往后扩展”的逻辑写的，用分层路线图最贴。

### 可以直接抄到 PPT 里的文字

#### 顶部标题

`后续工作路线图`

#### 第一层：短期可做

- `实机闭环验证`
- `MoveIt2 / 轨迹控制链`

#### 第二层：中期扩展

- `SROS2 / DDS Security`
- `多机器人与更多 ROS2 接口`

#### 第三层：长期目标

- `更高程度自动化评估`

### 每个框里可以补的一句短说明

如果你想让图更完整，可以在每个框下方加一行小字：

#### 实机闭环验证
- 从显示层结论延伸到执行层验证

#### MoveIt2 / 轨迹控制链
- 从状态链扩展到规划链和控制链

#### SROS2 / DDS Security
- 从应用层原型升级到正式中间件安全机制

#### 多机器人与更多 ROS2 接口
- 扩展到更复杂协同场景和更多关键接口

#### 更高程度自动化评估
- 联动实验复现、规则推理与防护验证

### 配色建议

- 短期可做：蓝色
- 中期扩展：橙色
- 长期目标：绿色

这样一眼就能看出阶段差异。

### 图题建议

`图 8-1 后续工作路线图`

### 图注建议

`该图按照短期可做、中期扩展和长期目标三个层次，总结了本文工作在实机闭环、轨迹控制链、安全中间件、多机器人场景和自动化评估等方向上的后续推进路径。其目的在于说明本文并非一次性结论，而是可向更完整机器人安全研究持续扩展的起点。`

### 一句话最实用建议

如果你想最快画出来，就画成：

**三层分级路线图：短期两项，中期两项，长期一项。**
