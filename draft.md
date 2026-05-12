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
