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
